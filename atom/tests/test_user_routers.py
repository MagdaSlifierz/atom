from fastapi.testclient import TestClient
import os
import sys
import json

sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from atom.main import app

client = TestClient(app)


def test_create_user(test_app):
    # create data later convert to json
    data = {"first_name": "Ola", "last_name": "Jezierska", "email": "ola.jez@gmail.com"}
    # I have to hit this endpoint from routers
    response = test_app.post("/", json=data)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Ola"
    assert response.json()["last_name"] == "Jezierska"
    assert response.json()["email"] == "ola.jez@gmail.com"

# def test_create_user():
#     sample_payload = {
#         "first_name": "Ola",
#         "last_name": "Jezierska",
#         "email": "ola.jez@gmail.com"
#     }
#     response = client.post("/", json=sample_payload)
#     assert response.status_code == 200
#     assert response.json() == {
#         "Status": "Success",
#         "User": {
#             "first_name": "Ola",
#             "last_name": "Jezierska",
#             "email": "ola.jez@gmail.com"
#         },
#     }
#
# from atom.core import config
# print(f"Using DATABASE_URL: {config.settings.DATABASE_URL}")
# def test_root():
#     response = client.get("/user/all")
#     assert response.status_code == 200
#     assert response.json() == {"message": "The API is LIVE!!"}
