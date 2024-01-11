# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from atom.tests.conftest import test_app
#
# from atom.models.database import Base, get_db
# import pytest
# import os
# import sys
#
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base.metadata.create_all(bind=engine)
#
#
# # now I have to override get_db function for testing
#
# def override_get_db():
#     # connection = engine.connect()
#     #
#     # # begin a non-ORM transaction
#     # transaction = connection.begin()
#     #
#     # # bind an individual Session to the connection
#     # db = Session(bind=connection)
#     # # db = Session(engine)
#     #
#     # yield db
#     #
#     # db.close()
#     # transaction.rollback()
#     # connection.close()
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()
#
#
# test_app.dependency_overrides[get_db] = override_get_db
