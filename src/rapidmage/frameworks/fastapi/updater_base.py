from rapidmage.file_manager import PythonFileManager
from rapidmage.frameworks.fastapi.shared_configuration import SharedConfiguration
from rapidmage.spells_reader import SpellsReader
from rapidmage.text_processor import PythonTextProcessor

class UpdaterBase(PythonFileManager):

    def __init__(self, spells_reader: SpellsReader, shared_configuration: SharedConfiguration):
        self.spells_reader = spells_reader
        self.shared_configuration = shared_configuration
        self.text_processor = PythonTextProcessor()
