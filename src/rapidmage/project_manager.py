from rapidmage.frameworks.fastapi import FastAPIFWProjectManager
from rapidmage.spells_reader import SpellsReader

class ProjectManager():

    def __init__(self, spells_reader: SpellsReader):
        self.spells_reader = spells_reader
        self.set_fw_project_manager()

    def set_fw_project_manager(self):
        if self.spells_reader.framework == 'fastapi':
            self.fw_project_manager = FastAPIFWProjectManager(self.spells_reader)
        else:
            print("This framework is not available !")
            return

    def update(self):
        if self.fw_project_manager is not None:
            self.fw_project_manager.update()
