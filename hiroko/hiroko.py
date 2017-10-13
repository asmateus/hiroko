from core.regulator import UserEntryRegulator
from core.representation import PetriGlass
import numpy as np
import itertools
import random


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


if __name__ == '__main__':
    entry_regulator = UserEntryRegulator()
    rule_book = entry_regulator.fetchRuleBook()

    # We need to now the number of days in which the neighborhoods will be distributed,
    # also if the snapshot date of the file is not the same as the python saved date
    # minimum deviation and minimum distance will need to be recalculated
    rule_book['day-count'] = 20
    if not entry_regulator.isRuleBookUpdated():
        entry_regulator.updateRuleBook(rule_book)

    petri_glass = PetriGlass.getInstance()
    petri_glass.setPersistentRuleBook(rule_book)
    petri_glass.spawnNewPopulation()
