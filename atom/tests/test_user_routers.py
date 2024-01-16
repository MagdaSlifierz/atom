import os
import sys

# sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from atom.tests.conftest import test_app


def test_create_user(test_app):
    """
    Test the endpoint for creating a new user.

    This test sends a POST request to the '/' route with JSON payload containing user data (first name, last name, email).
    The test asserts that the response status code is 200 (OK) and the response JSON matches the data sent in the request.
    """
    # create data later convert to json
    data = {
        "first_name": "Paulina",
        "last_name": "Jurek",
        "email": "paulina.ewa@gmail.com",
    }
    # I have to hit this endpoint from routers
    response = test_app.post("/", json=data)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Paulina"
    assert response.json()["last_name"] == "Jurek"
    assert response.json()["email"] == "paulina.ewa@gmail.com"


#
# def test_all_users(test_app):
#     """
#     Test the endpoint to get all users.
#
#     This test ensures that the endpoint for retrieving all users is functioning correctly.
#     It sends a GET request to the '/user/all' route and checks that the response status is 200 (OK)
#     and the response content is a list, which should contain the user data in JSON format.
#     """
#     response = test_app.get("/user/all")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
#
#
# def test_get_user_by_id(test_app):
#     """
#     Test the endpoint to get a user by ID.
#     This test checks the functionality of the endpoint for retrieving a specific user by their user ID.
#     """
#     user_id = "d4f610a4-b484-435c-9b64-5ae216f887b3"
#     response = test_app.get(f"/user/{user_id}")
#     assert response.status_code == 200
#     assert response.json()["user_id"] == user_id
#     # Test for non-existent user
#     response = test_app.get("/user/cc088a45-8c56-45c2-8ff8-c42a88580d8b")
#     assert response.status_code == 404
#
#
# def test_update_user_by_id(test_app):
#     """
#     Test the endpoint to update a user by ID.
#
#     This test sends a PUT request to the '/user/update/{user_id}' route with a known user ID and new user data.
#     The test asserts that the response status is 200 and the updated information in the response matches
#     the data sent in the request.
#     """
#     user_id = "d4f610a4-b484-435c-9b64-5ae216f887b3"
#     data = {"first_name": "Karol", "last_name": "Kielc", "email": "kielc@example.com"}
#     response = test_app.put(f"/user/update/{user_id}", json=data)
#     print(response.text)
#     assert response.status_code == 200
#     assert response.json()["first_name"] == "Karol"
#     assert response.json()["last_name"] == "Kielc"
#     assert response.json()["email"] == "kielc@example.com"
#     #
#     response = test_app.put("/user/update/dd088a45-8c56-45c2-8ff8-c42a88580d8b", json=data)
#     assert response.status_code == 404
#
#
# def test_delete_user_by_id(test_app):
#     """
#     Test the endpoint to delete a user by ID.
#
#     This test ensures the functionality of the endpoint for deleting a user based on their user ID.
#     It sends a DELETE request to the '/user/delete/{user_id}' route and checks that the response status
#     is 200 and the response message confirms successful deletion of the user.
#     """
#     user_id = "bca47c75-6418-4f5d-ae2c-6871b7714100"
#     response = test_app.delete(f"/user/delete/{user_id}")
#     assert response.status_code == 200
#     assert response.json()["message"] == "User was successfully deleted"
def test_get_user_by_id(test_app):
    # Create a new user
    new_user_data = {"first_name": "Test", "last_name": "User", "email": "test.user@example.com"}
    response = test_app.post("/user/create", json=new_user_data)
    assert response.status_code == 200
    created_user = response.json()
    user_id = created_user['id']  # Get the ID of the newly created user

    # Test getting the user by ID
    response = test_app.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id

    # Optionally delete the user after test
    test_app.delete(f"/user/delete/{user_id}")