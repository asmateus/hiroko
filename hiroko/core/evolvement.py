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
    def _calculateIndividualDistance(individual):
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

    def _calculatePopulationDistance(self, population):
        population_types = set(population)

        total_distance = 0
        for pt in population_types:
            total_distance += ComposedNaturalEvolution._calculateIndividualDistance(
                [self.petri_glass.getMapLocation(i)
                    for i in range(len(population)) if population[i] == pt]
            )

        return total_distance

    def _createMutant(self):
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
        def normalizeDistance(distance):
            return distance / self.petri_glass.getPersistentRuleBook()['max-distance']

        def normalizeDeviation(deviation):
            return deviation / self.petri_glass.getPersistentRuleBook()['max-deviation']

        population_fitness = list()
        for population in generation:
            population_fitness.append(
                0.6 * normalizeDeviation(
                    self._calculateStandardDeviation(
                        population,
                        self.petri_glass.getInputPopulationSmall())) +
                0.4 * normalizeDistance(self._calculatePopulationDistance(population))
            )

        return population_fitness

    def _crossIndividuals(self, generation):
        pass

    def _purgeGeneration(self, generation, generation_fitness, allow_up_to=4):
        generation_copy = generation.copy()
        generation_fitness_copy = generation_fitness.copy()
        while len(generation_copy) > allow_up_to:
            del generation_copy[generation_fitness_copy.index(max(generation_fitness_copy))]
            generation_fitness_copy.remove(max(generation_fitness_copy))

        return generation_copy

    def isPetriGlassFreezed(self):
        return self.epoch_count == self.petri_glass.getCurrentGenerationCount()

    def triggerEvolutionStep(self):
        generation = self.petri_glass.getCurrentGeneration()
        if generation is None:
            generation = list()
            while len(generation) != self.petri_glass.getOutputPopulationSize():
                generation.append(self._createMutant())

        # Obtain the fitness of each population
        generation_fitness = self._fitGeneration(generation)
        survivors = self._purgeGeneration(generation, generation_fitness)

        self.petri_glass.advanceCurrentGenerationCount()
