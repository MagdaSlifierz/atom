from fastapi.testclient import TestClient
from fastapi import FastAPI
import json
import os
import sys

sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from atom.main import app

client = TestClient(app)


def test_create_user():
    # create data later convert to json
    data = {"first_name": "Ola", "last_name": "Jezierska", "email": "ola.jez@gmail.com"}
    # I have to hit this endpoint from routers
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Ola"
    assert response.json()["last_name"] == "Jezierska"
    assert response.json()["email"] == "ola.jez@gmail.com"
