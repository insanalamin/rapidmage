from rapidmage.frameworks.fastapi.project_structure_updater import ProjectStructureUpdater
from rapidmage.frameworks.fastapi.repositories_updater import RepositoriesUpdater
from rapidmage.frameworks.fastapi.routes_updater import RoutesUpdater
from rapidmage.frameworks.fastapi.services_updater import ServicesUpdater
from rapidmage.frameworks.fastapi.shared_configuration import SharedConfiguration
from rapidmage.frameworks.fw_project_manager_base import FWProjectManagerBase

class FastAPIFWProjectManager(FWProjectManagerBase):

    def update(self):
        print("update fastapi source !")

        shared_configuration = SharedConfiguration()

        project_structure_updater = ProjectStructureUpdater(self.spells_reader, shared_configuration)
        project_structure_updater.update()

        repositories_updater = RepositoriesUpdater(self.spells_reader, shared_configuration)
        repositories_updater.update()

        # services_updater = ServicesUpdater(self.spells_reader, shared_configuration)
        # services_updater.update()

        # routes_updater = RoutesUpdater(self.spells_reader, shared_configuration)
        # routes_updater.update()

