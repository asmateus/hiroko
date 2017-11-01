from core.regulator import UserEntryRegulator
from graphics.minimal import MinimalApplication
from interface.buffer import OnlineBuffer
from core.representation import PetriGlass
from core.evolvement import ComposedNaturalEvolution
import time


if __name__ == '__main__':
    entry_regulator = UserEntryRegulator()
    rule_book = entry_regulator.fetchRuleBook()

    # Initialize the petri glass with a random population
    petri_glass = PetriGlass.getInstance()
    petri_glass.setPersistentRuleBook(rule_book)
    petri_glass.spawnNewPopulation()

    # If the snapshot date of the file is not the same as the python saved date
    # minimum deviation and minimum distance will need to be recalculated,
    # same with maximum values
    if not entry_regulator.isRuleBookUpdated():
        petri_glass.reassignMaxValues()
        entry_regulator.updateRuleBook(petri_glass.getPersistentRuleBook())

    if rule_book['interface'] == 'terminal':
        # Open buffer
        OnlineBuffer.getInstance().open()

        # Trigger evolution process
        t1 = time.time()
        evolution_prc = ComposedNaturalEvolution(petri_glass=petri_glass, max_epoch_count=200)
        while not evolution_prc.isPetriGlassFreezed():
            if petri_glass.getPersistentRuleBook()['method'] == 'genetic':
                evolution_prc.triggerEvolutionStep()
            elif petri_glass.getPersistentRuleBook()['method'] == 'random':
                evolution_prc.randomEvolutionStep()
        print('Elapsed time:', time.time() - t1)

        # We finished, close buffer
        OnlineBuffer.getInstance().close(save=True)
    elif rule_book['interface'] == 'ui':
        application = MinimalApplication(petri_glass)
        application.startApplication()
