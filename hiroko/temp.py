from core.regulator import UserEntryRegulator
from interface.buffer import OfflineBuffer
from core.representation import PetriGlass


if __name__ == '__main__':
    entry_regulator = UserEntryRegulator()
    rule_book = entry_regulator.fetchRuleBook()

    # Initialize the petri glass with a random population
    petri_glass = PetriGlass.getInstance()
    petri_glass.setPersistentRuleBook(rule_book)
    petri_glass.spawnNewPopulation()

    bf = OfflineBuffer.getInstance()
    bf.open('1508172652.dump')
    bf.setPetriGlass(petri_glass)
    best_gen = bf.getOverallBest()[2]

    best_gen_population = [bf.getNodeData(i) for i in range(len(best_gen))]

    day_people = [0] * len(set(best_gen))

    for i in range(len(best_gen)):
        day_people[best_gen[i] - 1] += best_gen_population[i]

    print(day_people)
