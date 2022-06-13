from typing import Dict
from rapidmage.frameworks.fastapi.updater_base import UpdaterBase

class RepositoriesUpdater(UpdaterBase):

    sql_statement = []
    migration_map = {} 

    def update(self):
        """Update repository files

        """
        print(self.spells_reader.version)

        self.update_from_migrations()
        self.update_from_relations()

    def update_from_migrations(self):

        repositories_path = "{}/src/repositories".format(self.spells_reader.project_path)
        models_path = "{}/src/models".format(self.spells_reader.project_path)

        for migration in self.spells_reader.repositories_migrations:
            table_name = migration['name']
            class_name = self.text_processor.camel(table_name) 
            table_columns: Dict = migration['columns']

            self.migration_map[table_name] = migration 

            # Generate model file
            model_file = "{}/{}_model.py".format(models_path, table_name)

            model_columns = []
            model_column_names = []

            for column_key, column_value in table_columns.items():
                model_column_names.append(column_key)
                pydantic_column_type = self.text_processor.pydantic_column(column_value.split()[0].split("(")[0])
                model_columns.append("    {}: {}\n".format(column_key, pydantic_column_type))

            self.touch(model_file, [
                "import datetime\n",
                "from pydantic import BaseModel, parse_obj_as\n",
                "from pydantic.types import UUID4\n",
                "\n",
                "\n",
                "class {}(BaseModel):\n".format(self.text_processor.camel(table_name)),
            ] + model_columns)

            # Generate repositories
            repository_folder = "{}/{}_repository".format(repositories_path, table_name)

            methods = ['find', 'add', 'save', 'remove']

            self.shared_configuration.registered_repositories.append(table_name)
            print("Repository folder", repository_folder)
            self.create_module(repository_folder)

            # Import methods from __init__.py
            map(lambda x: "from .{} import {}\n".format(x, x), methods)

            # Generate file for each repository method 
            for method in methods:

                method_body = []

                model_bind_column_names = map(lambda x: ":{}".format(x).replace(":geom", "ST_GeomFromText(:geom, 4326)"), model_column_names)

                if method == 'add':
                    method_body = [
                        "def {}({}:{}):\n".format(method, table_name, class_name),
                        "    result = db_execute(\"\"\"INSERT INTO app.{}({}) VALUES({})\"\"\", {})\n".
                        format(table_name, ",\n".
                            join(model_column_names), ",\n".
                            join(model_bind_column_names), "{}.dict()".format(table_name)),
                        "    return []\n",
                    ]


                if method == 'find':
                    print("model_columns", model_columns)
                    method_body = [
                        "def {}():\n".format(method,),
                        "    result = db_execute(\"\"\"SELECT {} FROM {}\"\"\", {})\n".format(", ".join(model_column_names), table_name, "{}"),
                        "    {}s = parse_obj_as(list[{}], result.fetchall())\n".format(table_name, class_name),
                        "    return {}s\n".format(table_name),
                    ]

                self.touch("{}/{}.py".format(repository_folder, method), [
                    "from pydantic import BaseModel, parse_obj_as\n",
                    "from pydantic.types import UUID4\n",
                    "from utils.db_connection import db_execute\n",
                    "from models.{}_model import {}\n".format(table_name, self.text_processor.camel(table_name)),
                    "\n\n",
                ] + method_body)

        print("update repositories", self.spells_reader.repositories_configs)

        print("self.shared_configuration.registered_repositories", self.shared_configuration.registered_repositories)

    def update_from_relations(self):

        # Iterate all relations
        for relation in self.spells_reader.repositories_relations:

            # Check source & destionation table availability 
            if relation['from'] in self.migration_map and relation['to'] in self.migration_map:

                # Get table migration 
                source_migration = self.migration_map[relation['from']]
                destination_migration = self.migration_map[relation['to']]

                # Create table name
                rel_table_name = "rel_{}_{}".format(relation['from'], relation['to'])


    def get_primary_keys_from_migrations(self, migration):
        print("get_primary_keys_from_migrations", self.migration_map)

        # Initiate output
        output = []

        # Get primary keys
        primary_keys = []

        for constraint in migration['constraints']:
            if 'primary' in constraint:
                if isinstance(constraint['primary'], list):
                    for primary_key in constraint['primary']:
                        primary_keys.append(primary_keys)
                else:
                    primary_keys.append(constraint['primary'])
        
        # Populate SQL statement
        for primary_key in primary_keys:
            primary_key_desc = self.migration_map[migration['name']]['columns'][primary_key]
            output.append([migration['name'], primary_key, primary_key_desc])

        return output
