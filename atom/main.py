from fastapi import FastAPI
from atom.core import config
from models.database import Base
from atom.models.database import engine
from atom.routers.base import api_router


def create_tables():
    Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI()
    create_tables()
    include_router(app)
    return app


app = start_application()

# @app.get("/getenvvar")
# def get_env():
#     print(config.settings.DATABASE_URL)
#     return {"database": config.settings.DATABASE_URL}
