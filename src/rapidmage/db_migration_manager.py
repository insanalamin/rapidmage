from typing import Dict
from rapidmage.file_manager import FileManager
from rapidmage.spells_reader import SpellsReader


class DBMigrationManager:

    sql_statement = []
    migration_map = {} 
    
    def __init__(self, spells_reader: SpellsReader):
        self.spells_reader = spells_reader
        self.file_manager = FileManager()

    def update_ddl(self):
        sr = self.spells_reader
        print("migrate repositories", sr.repositories_migrations)

        geom_columns = []

        for table_index, table in enumerate(sr.repositories_migrations):
            self.migration_map[table['name']] = table

            if table_index > 0:
                self.sql_statement.append("\n")

            self.sql_statement.append("CREATE TABLE IF NOT EXISTS {} (\n".format(table['name']))

            table_columns: Dict = table['columns']
            column_index = 0

            for column_key, column_value in table_columns.items():

                if column_key == 'geom':
                    geom_columns.append({
                        'table_name': table['name'],
                        'column_name': column_key,
                        'srid': 4326,
                        'type': 'POINT',
                        'dimension': 2,
                    })
                else:
                    self.sql_statement.append("  {}{} {}\n".format("," if column_index > 0 else "", column_key, column_value.upper(),))

                column_index += 1

            if 'constraints' in table:
                constraints = table['constraints']
                print("constraints", constraints)

                for constraint in constraints:
                    if 'primary' in constraint:
                        print("primary", constraint['primary'])
                        if isinstance(constraint['primary'], list):
                            primary_keys = ','.join(constraint['primary'])
                        else:
                            primary_keys = constraint['primary']

                        self.sql_statement.append("  {}PRIMARY KEY ({})\n".format(",", primary_keys,))

            self.sql_statement.append(");\n")

        print("geom columns", geom_columns)

        self.sql_statement.append("\n")

        for geom_column in geom_columns:
            # https://postgis.net/docs/AddGeometryColumn.html
            self.sql_statement.append("SELECT AddGeometryColumn ('{}', '{}', {}, '{}', {});\n".format(
                geom_column['table_name'],
                geom_column['column_name'],
                geom_column['srid'],
                geom_column['type'],
                geom_column['dimension'],
            ))

            self.sql_statement.append("CREATE INDEX {}_{}_idx\n".format(geom_column['table_name'], geom_column['column_name']))
            self.sql_statement.append("ON {}\n".format(geom_column['table_name']))
            self.sql_statement.append("USING GIST ({});\n".format(geom_column['column_name']))
            self.sql_statement.append("\n")

        self.create_table_from_relations()

        self.file_manager.touch("./migrations.sql", self.sql_statement, "w")

    def create_table_from_relations(self):

        # Iterate all relations
        for relation in self.spells_reader.repositories_relations:

            # Check source & destionation table availability 
            if relation['from'] in self.migration_map and relation['to'] in self.migration_map:

                # Get table migration 
                source_migration = self.migration_map[relation['from']]
                destination_migration = self.migration_map[relation['to']]

                # Create table name
                rel_table_name = "rel_{}_{}".format(relation['from'], relation['to'])

                # Begin of DDL
                self.sql_statement.append("CREATE TABLE IF NOT EXISTS {} (\n".format(rel_table_name))

                # Get primary keys from source & destination migrations
                source_primary_keys_from_migration = self.get_primary_keys_from_migrations(source_migration)
                print("source_primary_keys_from_migration", source_primary_keys_from_migration)

                destination_primary_keys_from_migration = self.get_primary_keys_from_migrations(destination_migration)
                print("destination_primary_keys_from_migration", destination_primary_keys_from_migration)

                primary_keys_from_migration = source_primary_keys_from_migration + destination_primary_keys_from_migration

                # Build SQL statement line
                for primary_key_index, primary_key in enumerate(primary_keys_from_migration):
                    self.sql_statement.append("  {}{}_{} {}\n".format("," if primary_key_index > 0 else "", primary_key[0], primary_key[1], primary_key[2].upper(),))
                    
                
                # Iterate primary keys and build SQL

                # End of DDL
                self.sql_statement.append(");\n")

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
