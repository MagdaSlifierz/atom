import os
import sys

# sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from atom.tests.conftest import test_app


def create_user(test_app, first_name, last_name, email):
    """
    Helper function to create a user.

    :param test_app: The test client instance.
    :param first_name: User's first name.
    :param last_name: User's last name.
    :param email: User's email.
    :return: The response from the user creation request.
    """
    data = {"first_name": first_name, "last_name": last_name, "email": email}
    # I have to hit this endpoint from routers
    response = test_app.post("/", json=data)
    return response


def get_user_by_id(test_app, user_id):
    """
    Helper function to retrieve a user by ID and assert the response.

    :param test_app: The test client instance.
    :param user_id: The ID of the user to retrieve.
    :return: The user data from the response.
    """
    response = test_app.get(f"/user/{user_id}")
    assert response.status_code == 200, f"Failed to retrieve user with id {user_id}"
    user_data = response.json()
    assert user_data["user_id"] == user_id, "Retrieved user ID does not match"
    return user_data


def test_create_user(test_app):
    """
    Test the endpoint for creating a new user.

    This test sends a POST request to the '/' route with JSON payload containing user data (first name, last name, email).
    The test asserts that the response status code is 200 (OK) and the response JSON matches the data sent in the request.
    """
    # create data later convert to json

    response = create_user(test_app, "Karolina", "Jas", "jas@gmail.com")
    assert response.status_code == 200
    assert response.json()["first_name"] == "Karolina"
    assert response.json()["last_name"] == "Jas"
    assert response.json()["email"] == "jas@gmail.com"


def test_update_user_by_id(test_app):
    """
    Test the endpoint for updating user.

    This test sends a PUT request to the '/user/update/{user_id}' route with JSON payload containing user data (first name, last name, email).
    The test asserts that the response status code is 200 (OK) and the response JSON matches the data sent in the request.
    """
    # Create a new user
    create_user_response = create_user(
        test_app, "Joanna", "Skiba", "skibajoanna@gmail.com"
    )
    assert create_user_response.status_code == 200, "Fail do create user"
    created_user = create_user_response.json()
    # take this user by id
    user_id = created_user["user_id"]
    user_data = get_user_by_id(test_app, user_id)

    # Update the user
    updated_data = {
        "first_name": "Joanna",
        "last_name": "Skiba",
        "email": "skibajoanna@gmail.com",
    }
    update_response = test_app.put(f"/user/update/{user_id}", json=updated_data)
    assert update_response.status_code == 200
    # Assert updated data

    assert update_response.json()["first_name"] == "Joanna"
    assert update_response.json()["last_name"] == "Skiba"
    assert update_response.json()["email"] == "skibajoanna@gmail.com"

    test_app.delete(f"/user/delete/{user_id}")


def test_delete_user_by_id(test_app):
    """
    This is a test to delete the user
    Firstly the user has been created and the response status has been checked
    Next the user data has been convert to json type
    The  deleted request to the endpoint /user/delete/{user_id} was sent and is checked if
    the response status code is 200, indicating successful deletion.
    """
    create_response = create_user(test_app, "Ola", "Zerek", "zerek@gmail.com")
    assert create_response.status_code == 200, "Failed to create user"
    created_user = create_response.json()
    user_id = created_user["user_id"]  # Assuming 'id' is the key in the response
    user_data = get_user_by_id(test_app, user_id)
    # Optionally delete the user after test
    delete_response = test_app.delete(f"/user/delete/{user_id}")
    assert delete_response.status_code == 200, "Failed to delete user"


def test_all_users(test_app):
    """
    Test the endpoint to get all users.

    This test ensures that the endpoint for retrieving all users is functioning correctly.
    It sends a GET request to the '/user/all' route and checks that the response status is 200 (OK)
    and the response content is a list, which should contain the user data in JSON format.
    """
    response = test_app.get("/user/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
