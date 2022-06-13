from rapidmage.frameworks.fastapi.updater_base import UpdaterBase

class ServicesUpdater(UpdaterBase):
    def update(self):
        print(self.spells_reader.version)
