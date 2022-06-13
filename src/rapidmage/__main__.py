from rapidmage import SpellsReader
from rapidmage import DBMigrationManager
from rapidmage import ProjectManager

class RapidMage:

    def __init__(self, spells_file: str):
        self.spells_reader = SpellsReader(spells_file)

    def cast(self):
        print("Cast spells !") 

        db_migration_manager = DBMigrationManager(self.spells_reader)
        db_migration_manager.update_ddl()

        project_manager = ProjectManager(self.spells_reader)
        project_manager.update()

# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
if __name__ == "__main__":
    mage = RapidMage('./spells.yml')
    mage.cast()
