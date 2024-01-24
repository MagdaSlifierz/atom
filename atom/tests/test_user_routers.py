from atom.tests.conftest import test_app


def create_user(test_app, first_name, last_name, email):
    """
    Helper function to create a user.

    Parameters: test_app: The test client instance, first_name: User's first name,
    last_name: User's last name, email: User's email.

    Return: The response from the user creation request.
    """
    data = {"first_name": first_name, "last_name": last_name, "email": email}
    # sends a POST request to the endpoint /api/v1/users using the test_app object.
    # The request includes the data dictionary in JSON format.
    new_user_response = test_app.post("/api/v1/users", json=data)
    return new_user_response


def test_all_users(test_app):
    """
    Test the endpoint to get all users.

    This test ensures that the endpoint for retrieving all users is functioning correctly.
    It sends a GET request to the '/api/v1/user/all' route and checks that the response status is 200 (OK)
    and the response content is a list, which should contain the user data in JSON format.
    """
    response = test_app.get("/api/v1/users/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def get_user_by_id(test_app, user_id):
    """
    Helper function to retrieve a user by ID and assert the response.
    Parameters: test_app: The test client instance, user_id: The ID of the user to retrieve.
    Return: The user data from the response.
    """
    response = test_app.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200, f"Failed to retrieve user with id {user_id}"
    # This line parses the JSON content of the response and stores it in the variable user_id_data.
    # This should be the data of the user that was retrieved.
    user_id_data = response.json()
    # This line asserts that the unique_user_id field in the user_id_data matches
    # the user_id passed to the function.
    assert user_id_data["unique_user_id"] == user_id, "Retrieved user ID does not match"
    return user_id_data


def test_create_user(test_app):
    """
    Test the endpoint for creating a new user.

    This test sends a POST request to the '/api/v1/users' route with JSON payload containing user data (first name, last name, email).
    The test asserts that the response status code is 200 (OK) and the response JSON matches the data sent in the request.
    """

    created_user_response = create_user(test_app, "Karolina", "Pasi", "kpasi@gmail.com")
    assert created_user_response.status_code == 200
    # This line asserts that the first_name field in the JSON response matches the first name sent in the request
    assert created_user_response.json()["first_name"] == "Karolina"
    assert created_user_response.json()["last_name"] == "Pasi"
    assert created_user_response.json()["email"] == "kpasi@gmail.com"

    # Extract the user_id from the created user response
    user_id = created_user_response.json()["unique_user_id"]
    # Delete the user
    delete_response = test_app.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 200


def test_update_user_by_id(test_app):
    """
    Test the endpoint for updating user.

    This test sends a PUT request to the '/api/v1/user/update/{user_id}' route with JSON payload containing user data (first name, last name, email).
    The test asserts that the response status code is 200 (OK) and the response JSON matches the data sent in the request.
    """
    # Create a new user, use helper method
    create_user_response = create_user(
        test_app, "Joanna", "Skiba", "skibajoanna@gmail.com"
    )
    # check if the created user status is 200 successfully created
    assert create_user_response.status_code == 200, "Fail do create user"
    # takes JSON content of created data and stored in created_user variable as dictionary
    created_user = create_user_response.json()
    # take user by unique id that will be pass to the endpoint
    user_id = created_user["unique_user_id"]
    # update the user
    updated_data = {
        "first_name": "Joanna",
        "last_name": "Skibinska",
        "email": "skibinskajoanna@gmail.com",
    }
    update_response = test_app.put(f"/api/v1/users/{user_id}", json=updated_data)
    assert update_response.status_code == 200
    # Assert updated data
    # This line asserts that the first_name field in the JSON response matches the values sent in the request
    assert update_response.json()["first_name"] == "Joanna"
    assert update_response.json()["last_name"] == "Skibinska"
    assert update_response.json()["email"] == "skibinskajoanna@gmail.com"
    test_app.delete(f"/api/v1/users/{user_id}")


def test_delete_user_by_id(test_app):
    """
    This is a test to delete the user
    Firstly the user has been created and the response status has been checked
    Next the user data has been convert to json type
    The  deleted request to the endpoint /user/delete/{user_id} was sent and is checked if
    the response status code is 200, indicating successful deletion.
    """
    create_response = create_user(test_app, "Ola", "Zerek", "zerek@gmail.com")
    # asserts that the creation was successful (status code 200)
    assert create_response.status_code == 200, "Failed to create user"
    # converting the JSON content from the response of a request into a Python dictionary.
    created_user = create_response.json()
    # extracts the user ID from the creation response
    user_id = created_user["unique_user_id"]  # Assuming 'id' is the key in the response
    # delete the user after test
    delete_response = test_app.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 200, "Failed to delete user"
