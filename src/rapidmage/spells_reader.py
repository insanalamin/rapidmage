from typing import Dict
import yaml


class SpellsReader:
    def __init__(self, spells_file: str):
        with open(spells_file, 'r') as stream:
            try:
                self.parsed_yaml: Dict = yaml.safe_load(stream)
                self.version: str = self.parsed_yaml['version']
                self.framework: str = self.parsed_yaml['framework']
                self.project_path: str = self.parsed_yaml['project_path']
                self.title: str = self.parsed_yaml['title']

                self.configs_jwt_auth: Dict = self.parsed_yaml['configs']['jwt_auth']

                self.repositories_configs: Dict = self.parsed_yaml['repositories']['configs']
                self.repositories_migrations: Dict = self.parsed_yaml['repositories']['migrations']
                self.repositories_relations: Dict = self.parsed_yaml['repositories']['relations']
                self.routes: Dict = self.parsed_yaml['routes']

            except yaml.YAMLError as exc:
                print(exc)
