from rapidmage.frameworks.fastapi.updater_base import UpdaterBase

class RoutesUpdater(UpdaterBase):
    def update(self):
        print("update routes")
        pass

    def _update(self):
        """Update route and controller files

        """
        print(self.spells_reader.version)
        
        routes = self.spells_reader.routes
        routes_path = "{}/src/routers".format(self.spells_reader.project_path)
        controllers_path = "{}/src/controllers".format(self.spells_reader.project_path)
        self.create_module(routes_path)
        self.create_module(controllers_path)

        route_names = []

        added_controller_groups = []

        for route in routes:
            is_write_file = False

            if 'routes_group' in route:
                is_write_file = True

                http_method = None
                route_path = None

                if "get" in route:
                    http_method = "get"
                    route_path = route["get"]
                elif "post" in route:
                    http_method = "post"
                    route_path = route["post"]
                elif "put" in route:
                    http_method = "put"
                    route_path = route["put"]
                elif "delete" in route:
                    http_method = "delete"
                    route_path = route["delete"]

                if http_method is not None:

                    controller_group_name = route['routes_group']

                    controller_path = "{}/{}_controller" \
                        .format(controllers_path, controller_group_name)

                    self.create_module(controller_path)

                    route_name = "{}_route".format(controller_group_name)
                    route_names.append(route_name)

                    route_file = "{}/{}_route.py" \
                        .format(routes_path, controller_group_name)

                    if controller_group_name not in added_controller_groups:
                        added_controller_groups.append(controller_group_name)
                        self.touch(route_file, [
                            "from fastapi import Request, APIRouter, Response, status\n",
                            "\n",
                            "router = APIRouter()\n",
                            "\n",
                            "\n",
                            "class {}Route:\n"
                            .format(self.text_processor.camel(controller_group_name)),
                        ])

                    self.touch(route_file, [
                        "\n",
                        "    @router.{}(\"{}\")\n".format(http_method, route_path),
                        "    async def {}():\n".format(http_method),
                        "        return {'message': 'default message'}\n",
                    ], "a")

                    print("create controller_group", controller_group_name)

            elif 'repository' in route:
                is_write_file = True
                controller_group_name = route['repository']['name']

                if controller_group_name not in added_controller_groups:
                    added_controller_groups.append(controller_group_name)

                    controller_path = "{}/{}_controller"\
                        .format(controllers_path, controller_group_name)
                    print("controller path", controller_path)
                    self.create_module(controller_path)
                    self.touch("{}/__init__.py".format(controller_path))

                    route_name = "{}_route".format(controller_group_name)
                    route_names.append(route_name)

                    route_file = "{}/{}_route.py"\
                        .format(routes_path, controller_group_name)

                    # Generate route file
                    self.touch(route_file, [
                        "from fastapi import Request, APIRouter, Response, status\n",
                        "from controllers import {}_controller\n".format(controller_group_name),
                        "from models.{}_model import {}\n".format(controller_group_name, self.text_processor.camel(controller_group_name)),
                        "\n",
                        "router = APIRouter()\n",
                        "\n",
                        "\n",
                        "class {}Route:\n"
                        .format(self.text_processor.camel(controller_group_name)),
                    ])

                    # GET route
                    self.touch(route_file, [
                        "\n",
                        "    @router.{}(\"{}\")\n".format("get", ""),
                        "    async def {}():\n".format("get"),
                        "        return {}_controller.get()\n".format(controller_group_name),
                    ], "a")
                    # GET controller
                    self.touch("{}/get.py".format(controller_path), [
                        "from fastapi.encoders import jsonable_encoder\n",
                        "from fastapi.responses import JSONResponse\n",
                        "from pydantic import BaseModel, parse_obj_as\n",
                        "from pydantic.types import UUID4\n",
                        "from utils.db_connection import db_execute\n",
                        "from repositories import {}_repository\n".format(controller_group_name),
                        "\n",
                        "class GreetingDTO(BaseModel):\n",
                        "    message: str\n"
                        "\n"
                        "def get():\n",
                        "    result = db_execute(\"\"\"SELECT 'hello world !' AS message\"\"\", {})\n",
                        "    greetings = parse_obj_as(list[GreetingDTO], result.fetchall())\n",
                        "    return JSONResponse(content=jsonable_encoder(greetings), status_code=200)\n",
                    ])
                    self.touch("{}/__init__.py".format(controller_path), [
                        "from .get import get\n",
                    ], "a")

                    # GET BY UUID
                    self.touch(route_file, [
                        "\n",
                        "    @router.{}(\"{}\")\n".format("get", "/{uuid}"),
                        "    async def {}():\n".format("get_by_uuid"),
                        "        return {'message': 'default message get_by_uuid'}\n",
                    ], "a")
                    self.touch("{}/get_by_uuid.py".format(controller_path), [
                        "def get_by_uuid():\n",
                        "    return {'message': 'get'}\n",
                    ])
                    self.touch("{}/__init__.py".format(controller_path), [
                        "from .get_by_uuid import get_by_uuid\n",
                    ], "a")

                    # POST route
                    self.touch(route_file, [
                        "\n",
                        "    @router.{}(\"{}\")\n".format("post", ""),
                        "    async def {}({}: {}):\n".format("post", controller_group_name, self.text_processor.camel(controller_group_name)),
                        "        return {}_controller.post({})\n".format(controller_group_name, controller_group_name),
                    ], "a")
                    # POST controller
                    self.touch("{}/post.py".format(controller_path), [
                        "from fastapi.encoders import jsonable_encoder\n",
                        "from fastapi.responses import JSONResponse\n",
                        "from pydantic import BaseModel, parse_obj_as\n",
                        "from pydantic.types import UUID4\n",
                        "from utils.db_connection import db_execute\n",
                        "from repositories import {}_repository\n".format(controller_group_name),
                        "from models.{}_model import {}\n".format(controller_group_name, self.text_processor.camel(controller_group_name)),
                        "\n",
                        "def post({}: {}):\n".format(controller_group_name, self.text_processor.camel(controller_group_name)),
                        "    {}_repository.add({})\n".format(controller_group_name, controller_group_name),
                        "    return JSONResponse(content=jsonable_encoder({}), status_code=200)\n",
                    ])
                    self.touch("{}/__init__.py".format(controller_path), [
                        "from .post import post\n",
                    ], "a")

                    self.touch(route_file, [
                        "\n",
                        "    @router.{}(\"{}\")\n".format("put", "/{uuid}"),
                        "    async def {}():\n".format("put"),
                        "        return {'message': 'default message put'}\n",
                    ], "a")

                    self.touch("{}/put.py".format(controller_path))

                    self.touch(route_file, [
                        "\n",
                        "    @router.{}(\"{}\")\n".format("delete", "/{uuid}"),
                        "    async def {}():\n".format("delete"),
                        "        return {'message': 'default message delete'}\n",
                    ], "a")

                    self.touch("{}/delete.py".format(controller_path))

                    print("create controller_group", controller_group_name)
            else:
                pass

            if is_write_file:
                pass


        print("route names", route_names)
        fn = lambda x: "app.include_router({}.router, prefix=\"/{}\", tags=[\"{}\"])\n".format(x, x.replace("_route", ""), x.replace("_route", ""))

        main_file = "{}/src/main.py".format(self.spells_reader.project_path)
        self.touch(main_file, [
            "from fastapi import FastAPI\n",
            "from routers import {}\n".format(", ".join(route_names)),
            "\n",
            "app = FastAPI(\n",
            "   title='Jabar Geotagging'\n",
            ")\n",
            "\n",
        ] + list(map(fn, route_names)))

        print("update routes")
