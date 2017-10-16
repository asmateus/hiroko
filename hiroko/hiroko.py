from core.regulator import UserEntryRegulator
from interface.buffer import OnlineBuffer
from core.representation import PetriGlass
from core.evolvement import ComposedNaturalEvolution


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

    # Open buffer
    OnlineBuffer.getInstance().open()

    # Trigger evolution process
    evolution_prc = ComposedNaturalEvolution(petri_glass=petri_glass, max_epoch_count=70)
    while not evolution_prc.isPetriGlassFreezed():
        evolution_prc.triggerEvolutionStep()

    # We finished, close buffer
    OnlineBuffer.getInstance().close(save=True)
