from rapidmage.frameworks.fastapi.updater_base import UpdaterBase


class ProjectStructureUpdater(UpdaterBase):
        
    def update(self):

        src_path = "{}/src".format(self.spells_reader.project_path)
        self.create_module(src_path)

        utils_path = "{}/utils".format(src_path)
        self.create_module(utils_path)

        models_path = "{}/models".format(src_path)
        self.create_module(models_path)

        repositories_path = "{}/repositories".format(src_path)
        self.create_module(repositories_path)

        routes_path = "{}/routers".format(src_path)
        self.create_module(routes_path)

        controllers_path = "{}/controllers".format(src_path)
        self.create_module(controllers_path)

        services_path = "{}/controllers".format(src_path)
        self.create_module(services_path)

        self.copy_if_not_exist("./bootstrap_files/db_connection.py", "{}/db_connection.py".format(utils_path))
