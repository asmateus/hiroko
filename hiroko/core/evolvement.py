from interface.buffer import OnlineBuffer
import itertools
import numpy as np
import random


class ComposedNaturalEvolution:
    def __init__(self, petri_glass, max_epoch_count=100):
        self.epoch_count = max_epoch_count
        self.checkpoint_data = dict()
        self.petri_glass = petri_glass

    @staticmethod
    def _calculateStandardDeviation(population, cli_little_info):
        days = set(population)
        total_revisions = [
            sum(cli_little_info[i] for i in range(len(population)) if population[i] == d)
            for d in days]
        return np.std(total_revisions)

    @staticmethod
    def _calculateAverageRevisions(population, cli_little_info):
        days = set(population)
        total_revisions = [
            sum(cli_little_info[i] for i in range(len(population)) if population[i] == d)
            for d in days]
        return np.mean(total_revisions)

    @staticmethod
    def _getCountsPerDay(population, cli_little_info):
        days = set(population)
        total_revisions = [
            sum(cli_little_info[i] for i in range(len(population)) if population[i] == d)
            for d in days]
        return total_revisions

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

    def _calculatePopulationDistance(self, population):
        population_types = set(population)

        total_distance = 0
        for pt in population_types:
            total_distance += ComposedNaturalEvolution.calculateIndividualDistance(
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
        for i in range(5):
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
                0 * normalizeDeviation(
                    self._calculateStandardDeviation(
                        population,
                        self.petri_glass.getInputPopulationSmall())) +
                1 * normalizeDistance(self._calculatePopulationDistance(population))
            )

        return population_fitness

    def _crossIndividuals(self, generation, fitness):
        '''
            The cross over process is as follows:
             * Choose random pairs from generation
             * Get the average of clients per day for each member of the population
             * Select the day furthest from this average
             * Exchange neighborhoods randomly for this days
             * repeat N times
        '''
        N = 2

        gen = sorted(zip(generation, fitness), key=lambda t: t[1])

        gen = list(list(zip(*gen))[0])
        gen_save = gen[0:4]
        gen = gen[4:]
        input_small = self.petri_glass.getInputPopulationSmall()
        avg = [self._calculateAverageRevisions(g, input_small) for g in gen]

        # Pair selection
        pairs = list(range(len(gen)))
        random.shuffle(pairs)
        group1, group2 = pairs[0:len(pairs) // 2], pairs[len(pairs) // 2: len(pairs)]
        pairs = list(zip(group1, group2))

        for i in range(N):
            # Exchange information
            for idx1, idx2 in pairs:
                # Get worst days
                counts_1 = self._getCountsPerDay(gen[idx1], input_small)
                counts_2 = self._getCountsPerDay(gen[idx2], input_small)

                counts_1_std = [int(abs(avg[idx1] - c)) for c in counts_1]
                counts_2_std = [int(abs(avg[idx2] - c)) for c in counts_2]

                worst_1 = counts_1_std.index(max(counts_1_std)) + 1
                worst_2 = counts_2_std.index(max(counts_2_std)) + 1

                # Get neighborhoods that belong to each worst day
                neighbor_worst_1 = [i for i in range(len(gen[idx1])) if gen[idx1][i] == worst_1]
                neighbor_worst_2 = [i for i in range(len(gen[idx2])) if gen[idx2][i] == worst_2]

                random.shuffle(neighbor_worst_1)
                random.shuffle(neighbor_worst_2)

                # Get the smallest len
                l_neighbor_worst_1 = len(neighbor_worst_1)
                l_neighbor_worst_2 = len(neighbor_worst_2)

                min_len = min([l_neighbor_worst_1, l_neighbor_worst_2])
                s_size = min_len // 3
                s_start = 0

                # Exchange
                n_w_1 = neighbor_worst_1[s_start: s_start + s_size]
                n_w_2 = neighbor_worst_2[s_start: s_start + s_size]

                for i, j in zip(n_w_1, n_w_2):
                    temp = gen[idx1][i]
                    gen[idx1][i] = gen[idx2][j]
                    gen[idx2][j] = temp

        gen.extend(gen_save)
        return gen

    def _purgeGeneration(self, generation, generation_fitness, allow_up_to=6):
        generation_copy = generation.copy()
        generation_fitness_copy = generation_fitness.copy()
        while len(generation_copy) > allow_up_to:
            del generation_copy[generation_fitness_copy.index(max(generation_fitness_copy))]
            generation_fitness_copy.remove(max(generation_fitness_copy))

        return generation_copy, generation_fitness_copy

    def _writeToBuffer(self, generation_count, generation, fitness, sur_idxs):
        obuffer = OnlineBuffer.getInstance()
        obuffer.writeBuffer(generation_count, [generation, fitness, sur_idxs])

    def isPetriGlassFreezed(self):
        return self.epoch_count == self.petri_glass.getCurrentGenerationCount()

    def triggerEvolutionStep(self):
        generation = self.petri_glass.getCurrentGeneration()
        if generation is None:
            generation = list()
            while len(generation) != self.petri_glass.getOutputPopulationSize():
                generation.append(self._createMutant())
            self.petri_glass.setCurrentGeneration(generation)

        # Obtain the fitness of each population
        generation_fitness = self._fitGeneration(generation)
        survivors, survivors_fitness = self._purgeGeneration(generation, generation_fitness)

        # Pretty print of generation fitness
        print('Generation:', self.petri_glass.getCurrentGenerationCount() + 1)
        print('Best seeds:', ['%.4f' % round(f, 4) for f in survivors_fitness])

        # Get indices of survivors
        survivors_idx = [generation.index(s) for s in survivors]

        # Write information to buffer
        self._writeToBuffer(
            self.petri_glass.getCurrentGenerationCount(),
            generation,
            generation_fitness,
            survivors_idx)

        # Generate next generation via cross over of its individuals (the population)
        next_gen_base = self._crossIndividuals(survivors, survivors_fitness)

        # Fill the remaining space with mutants
        mutants_to_generate = self.petri_glass.getOutputPopulationSize() - len(next_gen_base)

        mutants = list()
        for i in range(mutants_to_generate):
            mutants.append(self._createMutant())

        next_gen_base.extend(mutants)
        self.petri_glass.setCurrentGeneration(next_gen_base)

        # Advance to the next generation
        self.petri_glass.advanceCurrentGenerationCount()

    def randomEvolutionStep(self):
        generation = list()
        while len(generation) != self.petri_glass.getOutputPopulationSize():
            generation.append(self._createMutant())

        # Obtain the fitness of each population
        generation_fitness = self._fitGeneration(generation)
        survivors, survivors_fitness = self._purgeGeneration(generation, generation_fitness)

        # Pretty print of generation fitness
        print('Generation:', self.petri_glass.getCurrentGenerationCount() + 1)
        print('Best seeds:', ['%.4f' % round(f, 4) for f in survivors_fitness])

        # Get indices of survivors
        survivors_idx = [generation.index(s) for s in survivors]

        # Write information to buffer
        self._writeToBuffer(
            self.petri_glass.getCurrentGenerationCount(),
            generation,
            generation_fitness,
            survivors_idx)

        self.petri_glass.setCurrentGeneration(generation)

        # Advance to the next generation
        self.petri_glass.advanceCurrentGenerationCount()
