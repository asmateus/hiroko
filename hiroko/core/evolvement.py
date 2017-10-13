import itertools
import numpy as np
import random


class ComposedNaturalEvolution:
    def __init__(self, petri_glass, max_epoch_count=100):
        self.epoch_count = max_epoch_count
        self.petri_glass = petri_glass

    @staticmethod
    def _calculateStandardDeviation(population, cli_little_info):
        days = set(population)
        total_revisions = [
            sum(cli_little_info[i] for i in range(len(population)) if population[i] == d)
            for d in days]
        return np.std(total_revisions)

    @staticmethod
    def calculateIndividualDistance(individual):
        '''
            An individual is a list of points (x, y). The distance is calculated via maximum
            criteria. Select a node, search for the most distant member and repeat
        '''

        def distance(p1, p2):
            return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        total_distance = 0

        curr_point = individual.pop()
        while len(individual):
            max_local_distance = 0
            max_local_distance_idx = 0
            for i in range(len(individual)):
                if max_local_distance < distance(curr_point, individual[i]):
                    max_local_distance = distance(curr_point, individual[i])
                    max_local_distance_idx = i
            total_distance += max_local_distance
            curr_point = individual.pop(max_local_distance_idx)

        return int(total_distance)

    def _createMutants(self):
        genome = list(
            itertools.chain(*[
                [i + 1] * self.petri_glass.getParticleShape()[i]
                for i in range(len(self.petri_glass.getParticleShape()))
            ])
        )
        for i in range(3):
            random.shuffle(genome)
        return genome

    def _fitGeneration(self, generation):
        pass

    def _crossIndividuals(self, generation):
        pass

    def _purgeGeneration(self, generation, required_fitness=0):
        pass

    def isPetriGlassFreezed(self):
        return self.epoch_count == self.petri_glass.getCurrentGeneration()

    def triggerEvolutionStep(self):
        pass
