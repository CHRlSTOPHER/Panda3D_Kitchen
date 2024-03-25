from classes.menus.EntitiesMenu import EntitiesMenu
from classes.menus.SequenceManager import SequenceManager


class MasterMenu():

    def __init__(self, sequence):
        self.entities_mode = EntitiesMenu()

        self.sequence_manager = None
        if sequence:
            self.sequence_manager = SequenceManager(sequence)