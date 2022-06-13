import os
import shutil
from importlib.resources import path
from typing import List

class FileManager:

    def touch(self, file_route: str, content: List[str]=[], write_method: str="w"):
        """Create or append file from array content

        Args:
            file_route (str): File path 
            content (str): List of content line 
            write_method (str): w for write a new file, a for append to existing file
        """

        print("touch", file_route)
        f = open(file_route, write_method)
        f.writelines(content)
        f.close()

    def copy_if_not_exist(self, src: str, dst: str):
        """Copy file if not exist

        Args:
            src (str): File source 
            dst (str): File destination 

        """

        if os.path.isfile(dst):
            print(dst, "exist")
        else:
            print("copy {} to {}".format(src, dst))
            with path("rapidmage.frameworks.fastapi.bootstrap_files", "db_connection.py") as src_file:
                shutil.copy(src_file, dst)

class PythonFileManager(FileManager):

    def create_module(self, path: str):
        """Create Python module if not exist

        Args:
            path (str): Module path

        """

        is_exist = os.path.exists(path)

        if not is_exist:
            os.makedirs(path)

            init_file = "{}/__init__.py".format(path)
            self.touch(init_file)

            print("create module ", path, init_file)

