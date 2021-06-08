from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules

from asyncpg.exceptions import PostgresError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.application.seeds import seed_database
from src.infrastructure.database import db
from src.utils import project_root


def build_app():
    return (AppBuilder()
            .add_api_routes()
            .add_error_handlers()
            .add_events()
            .add_healthcheck()
            .create_app())


class AppBuilder:
    def __init__(self):
        self._app = FastAPI(title="Cocktail Recipes",
                            description="An API for managing your cocktails",
                            docs_url=None,
                            redoc_url="/docs")

    def add_api_routes(self):
        root_dir = project_root()
        router_dir = Path(__file__).parent / "routers"

        for submodule in iter_modules([router_dir.as_posix()]):
            if submodule.ispkg and (router_file := router_dir / submodule.name / "router.py").exists():
                module = import_module('.'.join(router_file.relative_to(root_dir).parts).replace('.py', ''))
                if hasattr(module, 'router'):
                    self._app.include_router(module.router)

        return self

    def add_error_handlers(self):
        @self._app.exception_handler(PostgresError)
        async def catch_all_handler(_: Request, exc: PostgresError):
            return JSONResponse(status_code=400, content={"error": exc.message, "detail": exc.detail})

        return self

    def add_events(self):
        @self._app.on_event("startup")
        async def startup():
            await db.connect()
            await seed_database()

        @self._app.on_event("shutdown")
        async def shutdown():
            await db.disconnect()

        return self

    def add_healthcheck(self):
        @self._app.get("/_healthcheck")
        def healthcheck():
            return JSONResponse({"status": "Okay"})

        return self

    def create_app(self):
        return self._app
