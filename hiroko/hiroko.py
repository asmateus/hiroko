from collections import namedtuple
from interface.regulator import UserEntryRegulator
import numpy as np
import itertools
import random
import csv
import os


DATA_PTH = os.path.dirname(os.path.abspath(__file__)).split('hiroko')[0] + 'hiroko/data/'
Node = namedtuple('Node', ['neighborhood', 'gis', 'clients', 'day'])


def csvRead(file='', delimiter=';'):
    with open(DATA_PTH + file, newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=delimiter)
        return list(csv_data)[1:]


def loadLittleInfo(csv_reader_out):
    clients = [int(data_point[2]) for data_point in csv_reader_out]
    little_info = np.array(clients)
    return little_info


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


def generateRandomGenomePopulation(genome_alloc, clients):
    genome = list(itertools.chain(*[[i + 1] * genome_alloc[i] for i in range(len(genome_alloc))]))
    for i in range(3):
        random.shuffle(genome)
    return genome


def calculateStandardDeviation(population, cli_little_info):
    days = set(population)
    total_revisions = [
        sum(cli_little_info[i] for i in range(len(population)) if population[i] == d)
        for d in days]
    return np.std(total_revisions)


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


if __name__ == '__main__':
    entry_regulator = UserEntryRegulator()
    rule_book = entry_regulator.fetchRuleBook()

    # We need to now the number of days in which the neighborhoods will be distributed,
    # also if the snapshot date of the file is not the same as the python saved date
    # minimum deviation and minimum distance will need to be recalculated
    entry_regulator.isRuleBookUpdated()
    days = 20

    # Read neighborhood data (only clients)
    cc = csvRead('neighborhood_description.csv')
    clients = loadLittleInfo(cc)

    # Read full neighborhood data
    neighborhoods_data = loadBigInfo(cc)

    # Create location map
    per = csvRead('neighborhood_nodes.csv')
    locmap = generateLocationMap(per)

    # Days distribution
    d_distribution = len(clients) // days
    d_overhead = len(clients) - d_distribution * days

    # Genoma allocator
    genoma_alloc = [d_distribution] * days
    for i in range(d_overhead):
        genoma_alloc[i] += 1

    # Produce random genome
    population = generateRandomGenomePopulation(genoma_alloc, clients)
    print(calculateStandardDeviation(population, clients))
