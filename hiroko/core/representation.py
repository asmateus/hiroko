'''
    This file handles the data representation, it has the graph and population data.
    You can specify the desired output type.
'''
from collections import namedtuple
from core.evolvement import ComposedNaturalEvolution
from interface.CSVManager import csvRead
import numpy as np

Node = namedtuple('Node', ['neighborhood', 'gis', 'clients', 'day'])


class Parser:
    @staticmethod
    def loadLittleInfo(csv_reader_out):
        clients = [int(data_point[2]) for data_point in csv_reader_out]
        little_info = np.array(clients)
        return little_info

    @staticmethod
    def loadBigInfo(csv_reader_out):
        neighborhoods_data = list()
        for data_point in csv_reader_out:
            neighborhoods_data.append(Node(
                neighborhood=data_point[0],
                gis=data_point[1],
                clients=data_point[2],
                day=data_point[3]
            ))

        return neighborhoods_data

    @staticmethod
    def generateLocationMap(perimeter_info):
        alist = list()
        blist = list()
        for info in perimeter_info:
            if info[0] in alist:
                blist[alist.index(info[0])].append([int(info[1]), int(info[2])])
            else:
                alist.append(info[0])
                blist.append([[int(info[1]), int(info[2])]])
        locmap = [np.array(i) for i in blist]
        locmap = [(
            np.sum(i.transpose()[0]) // len(i.transpose()[0]),
            np.sum(i.transpose()[1]) // len(i.transpose()[1])) for i in locmap]

        relational_locmap = {k: v for k, v in zip(alist, locmap)}
        return relational_locmap


class PetriGlass:
    '''
        PetriGlass is the Genomic pool representation of the data. It will be just one
        system wide, so implement singleton design pattern.
    '''
    instance = None

    @staticmethod
    def getInstance():
        if not PetriGlass.instance:
            PetriGlass.instance = PetriGlass()
        return PetriGlass.instance

    def __init__(self):
        # Data input representation, directly from CSV files
        self.input_population_data_big = None
        self.input_population_data_small = None
        self.input_location_map = None

        self.output_population_size = 0

        # The representation of a random member of the genome, used for initialization
        # and random mutations. It holds the number of neighborhoods per day
        self._genome_particle_shape = None

        # The current genome pool for fitness classification
        self.current_genome_pool = None

        # The current genome pool with extra data, it displays whether the member is born via
        # random initialization, cross over or mutation, if it will be discarded and the fitness
        # value, separated by objectives. It is saves as follows:
        # [individual-data-chain],<birth-method>,<life-expectation>,<(fitness-tuple)>
        self.current_genome_pool_registry = None

        # Current fitness of overall population
        self.current_fitness = None

        # The generation number of current population
        self.population_generations = 0

        # Save and retreival information. Indicates if the PetriGlass is ready for usage
        self.petriglass_stamp = None

        # Persistent system wide rule book
        self._persistent_rule_book = None

    def getInputPopulationSmall(self):
        return self.input_population_data_small

    def getCurrentGeneration(self):
        return self.current_genome_pool

    def getOutputPopulationSize(self):
        return self.output_population_size

    def getCurrentGenerationCount(self):
        return self.population_generations

    def setCurrentGenerationCount(self, generation_num):
        self.population_generations = generation_num

    def advanceCurrentGenerationCount(self):
        self.population_generations += 1

    def getParticleShape(self):
        return self._genome_particle_shape

    def setPersistentRuleBook(self, rule_book):
        self._persistent_rule_book = rule_book

    def getPersistentRuleBook(self):
        return self._persistent_rule_book

    def getMapLocation(self, index):
        return self.input_location_map[self.input_population_data_big[index].gis]

    def reassignMaxValues(self):
        self._persistent_rule_book['max-deviation'] = int(sum(self.input_population_data_small))
        self._persistent_rule_book['max-distance'] = \
            ComposedNaturalEvolution.calculateIndividualDistance(
                list(self.input_location_map.values()))

    def spawnNewPopulation(self):
        if not self._persistent_rule_book:
            print('ERROR: Petri Glass requires a persistent rule book for execution')
            return

        # *********
        # Read files
        # *********

        # Read neighborhood data (only clients) and neighborhood perimeters data
        cc = csvRead('neighborhood_description.csv')
        per = csvRead('neighborhood_nodes.csv')

        # Minimum representation of neighborhoods -> <neighborhood-number: client's count>
        self.input_population_data_small = Parser.loadLittleInfo(cc)

        # Full neighborhoods data -> <name, GIS, client's amount, days>
        self.input_population_data_big = Parser.loadBigInfo(cc)

        # Location map information -> <GIS, xy-position>
        self.input_location_map = Parser.generateLocationMap(per)

        # Retreive output population size
        self.output_population_size = self._persistent_rule_book['output-population-size']

        # ********************************
        # Create the genome particle shape
        # ********************************

        # Days distribution
        days = self._persistent_rule_book['day-count']
        d_distribution = len(self.input_population_data_small) // days
        d_overhead = len(self.input_population_data_small) - d_distribution * days

        # Genoma allocator
        genoma_alloc = [d_distribution] * days
        for i in range(d_overhead):
            genoma_alloc[i] += 1

        self._genome_particle_shape = genoma_alloc
