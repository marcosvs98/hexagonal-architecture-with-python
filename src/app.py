from fastapi import FastAPI
from fastapi_pagination import add_pagination
from settings import APPLICATION_NAME
from rest import init_routes  # , init_middlewares


def create_app():
    # fileConfig('logging.ini')

    app = FastAPI(
        title=APPLICATION_NAME,
        description='Aplicação FastAPI utilizando arquitetura hexagonal',
    )

    # init_middlewares(app)
    init_routes(app)
    add_pagination(app)

    return app
