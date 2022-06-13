from rapidmage.file_manager import FileManager
from rapidmage.spells_reader import SpellsReader

class FWProjectManagerBase():

    def __init__(self, spells_reader: SpellsReader):
        self.spells_reader = spells_reader
        self.file_manager = FileManager()
