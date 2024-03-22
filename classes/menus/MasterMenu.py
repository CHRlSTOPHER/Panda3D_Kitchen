from classes.menus.AddItemsMenu import AddItemsMenu
from classes.menus.ExistingItemsMenu import ExistingItemsMenu
from classes.menus.SequenceManager import SequenceManager


class MasterMenu():

    def __init__(self, sequence):
        self.add_items_menu = AddItemsMenu()
        self.existing_items_menu = ExistingItemsMenu()
        self.sequence_manager = None
        if sequence:
            self.sequence_manager = SequenceManager(sequence)