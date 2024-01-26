from atom.tests.conftest import test_app
from atom.tests.test_user_routers import create_user, get_user_by_id

"""
This module is to tests the endpoints related to todo item. 
"""


def create_user_and_todo(test_app, first_name, last_name, email, title, completed):
    """
    Helper function to create a user and associate created item to the user .

    Parameters: test_app: The test client instance.
    Return: The user_id, and response from the creation request of todo item.
    """
    create_user_for_todo = create_user(test_app, first_name, last_name, email)
    assert create_user_for_todo.status_code == 201, "failed to create user"
    created_user_for_todo = create_user_for_todo.json()

    # now take this user_id_unique
    user_id = created_user_for_todo["unique_id"]

    # create todo_item
    todo_item_data = {
        "title": title,
        "completed": completed,
    }
    response = test_app.post(f"/api/v1/users/{user_id}/todos", json=todo_item_data)
    return user_id, response


def test_create_todo_item_by_user(test_app):
    """
    This is a test to create todo item by a user.
    The test first create the user as well as todo item, next it checks if the response status of created todo is correct.
    """
    user_id, created_todo_response = create_user_and_todo(
        test_app, "Maria", "Dunalewicz", "dunalewicz@gmail.com", "go to the gym", False
    )
    assert created_todo_response.status_code == 201, "failed to create user"
    todo_item = created_todo_response.json()
    assert todo_item["title"] == "go to the gym"
    assert todo_item["completed"] is False
    delete_response = test_app.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 204, "Failed to delete user"


def test_create_todo_item_by_non_existing_user(test_app):
    """
    Negative Test Case
    This is a test to check if not existing user can create todo item.
    """
    non_existing_user_id = "abcdeefghijklmnorst"
    todo_data = {"title": "go to the gym", "completed": False}

    create_todo_response = test_app.post(
        f"/api/v1/users/{non_existing_user_id}/todos", json=todo_data
    )
    assert (
        create_todo_response.status_code != 201
    ), "Expected failure when creating todo for non-existing user"


def test_read_users_todo(test_app):
    """
    This is endpoint to test the items that the user has created it. This test send the get response to route
    /api/v1/users/{user_id}/todos and check the response 200 as well as the response content the list that has a data in JSON format
    """

    user_id, _ = create_user_and_todo(
        test_app, "Paulina", "Powlikowska", "powlikowsa@gmail.com", "gardening", False
    )

    all_todos_response = test_app.get(f"/api/v1/users/{user_id}/todos")
    assert all_todos_response.status_code == 200
    assert isinstance(all_todos_response.json(), list)
    delete_response = test_app.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 204, "Failed to delete user"


def test_read_todo_item_by_user(test_app):
    """
    This is endpoint to test the specific item that the user has created it.
    This test function perform steps:
    1. creates a new user and todo item associate with the user
    2. sends the get request to the endpoint ("api/v1/users/{user_id}/todos/{todo_id}")
    3. verifies that the status code is 200 and that the response content matches the expected data format
    """
    user_id, todo_create = create_user_and_todo(
        test_app, "Anna", "Kielich", "kiehghghh@gmail.com", "drinking a water", False
    )
    assert todo_create.status_code == 201, "failed to create todo item"
    todo_created = todo_create.json()
    todo_id = todo_created["unique_id"]

    # Test the specific endpoint
    response = test_app.get(f"/api/v1/users/{user_id}/todos/{todo_id}")
    assert response.status_code == 200, "failed to retrieve todo item"
    delete_response = test_app.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 204, "Failed to delete user"


def test_update_todo_item_by_user(test_app):
    """
    This is a test to update a specific todo item created by user
    First the new user and todo item is created, and the response status is checked.
    Next the response is convert into JSON format and  sent request put to the endpoint;
    The response status is verified to be 200 and at the end the user and todo item is being deleted
    """
    user_id, todo_response = create_user_and_todo(
        test_app, "Danuta", "Polaczek", "dpolasczek909000@gmail.com", "cooking", False
    )
    assert todo_response.status_code == 201, "Failed to create todo item"

    todo_created_json = todo_response.json()
    todo_id = todo_created_json["unique_id"]

    updated_data = {
        "title": "doing the dishes",
        "completed": True,
    }

    try:
        # Update the todo item
        update_response = test_app.put(
            f"/api/v1/users/{user_id}/todos/{todo_id}", json=updated_data
        )
        assert update_response.status_code == 200, "Failed to update todo item"

        # Assert updated data
        updated_todo = update_response.json()
        assert updated_todo["title"] == "doing the dishes"
        assert updated_todo["completed"] is True

    finally:
        # Cleanup: delete the todo item
        test_app.delete(f"/api/v1/users/{user_id}/todos/{todo_id}")
        delete_response = test_app.delete(f"/api/v1/users/{user_id}")
        assert delete_response.status_code == 204, "Failed to delete user"


def test_update_never_created_item_by_user(test_app):
    """
    Negative scenario
    This is a test to check if user can update the item that was never created
    First the new user and todo item is created, and the response status is checked.
    Next the response is convert into JSON format and  sent request put to the endpoint;
    The response status is verified to be 404 Not Found response for non-existent todo item"
    The user is successfully deleted
    """
    user_id, todo_response = create_user_and_todo(
        test_app, "Danuta", "Pola", "dp0pssso@gmail.com", "cooking", False
    )
    assert todo_response.status_code == 201, "Failed to create todo item"

    todo_created_json = todo_response.json()
    todo_id = todo_created_json["unique_id"]
    non_existent_todo_item = todo_id + "abcd"

    updated_data = {
        "title": "doing the dishes",
        "completed": True,
    }
    update_response = test_app.put(
        f"/api/v1/users/{user_id}/todos/{non_existent_todo_item}", json=updated_data
    )
    assert (
        update_response.status_code == 404
    ), "Expected a 404 Not Found response for non-existent todo item"
    # Assert updated data
    error_response = update_response.json()
    assert "detail" in error_response, "Expected an error detail in the response"
    assert (
        "not found" in error_response["detail"].lower()
    ), "Expected a 'not found' message in the error detail"

    # Cleanup: delete the todo item
    delete_response = test_app.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 204, "Failed to delete user"


def test_update_todo_item_by_wrong_user(test_app):
    """
    Negative scenario
    This is a test to update a specific todo item by user that has a wrong id
    First the new user and todo item is created, and the response status is checked.
    Next the response is convert into JSON format and  sent request put to the endpoint;
    The response status is verified to be "Expected a 404 Not Found response for non-existent todo item"
    """
    user_id, todo_response = create_user_and_todo(
        test_app, "Danuta", "Pola", "lsls@gmail.com", "cooking", False
    )
    assert todo_response.status_code == 201, "Failed to create todo item"

    todo_created_json = todo_response.json()
    todo_id = todo_created_json["unique_id"]
    non_existent_user = user_id + "abcd"

    updated_data = {
        "title": "doing the dishes",
        "completed": True,
    }
    update_response = test_app.put(
        f"/api/v1/users/{non_existent_user}/todos/{todo_id}", json=updated_data
    )
    assert (
        update_response.status_code == 404
    ), "Expected a 404 Not Found response for non-existent todo item"
    delete_response = test_app.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 204, "Failed to delete user"


def test_delete_todo_item_by_user(test_app):
    """
    Test the deletion of a specific todo item created by a user.

    This test function ensures that a todo item can be deleted successfully by:
    1. Creating a new user and associated todo item.
    2. Sending a DELETE request to the endpoint '/api/v1/users/{user_id}/todos/{todo_id}'.
    3. Verifying that the response status code is 204, indicating successful deletion.
    """
    user_id, todo_response = create_user_and_todo(
        test_app, "Karol", "Wolowski", "wolowski123@gmail.com", "driving", False
    )

    # Assert for todo item creation
    assert todo_response.status_code == 201, "Failed to create todo item"
    todo_created_json = todo_response.json()

    # Get todo ID from the created todo item
    todo_id = todo_created_json["unique_id"]

    # Check the response to delete
    delete_response = test_app.delete(f"/api/v1/users/{user_id}/todos/{todo_id}")
    assert delete_response.status_code == 204, "Failed to delete todo item"
    delete_response = test_app.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 204, "Failed to delete user"


def test_delete_never_created_item_by_user(test_app):
    """
    Negative test case
    Test the deletion of never created todo item by a user.

    This test function ensures that a todo item can be deleted successfully by:
    1. Creating a new user and associated todo item.
    2. Sending a DELETE request to the endpoint '/api/v1/users/{user_id}/todos/{todo_id}'.
    3. Verifying that the response status code is 404, "Failed to delete todo item".
    """
    user_id, todo_response = create_user_and_todo(
        test_app, "Karol", "Wolowski", "wolowski@gmail.com", "driving", False
    )

    # Assert for todo item creation
    assert todo_response.status_code == 201, "Failed to create todo item"
    todo_created_json = todo_response.json()

    # Get todo ID from the created todo item
    todo_id = todo_created_json["unique_id"]
    non_existing_todo_id = todo_id + " abcdefgd"

    # Check the response to delete
    delete_response = test_app.delete(
        f"/api/v1/users/{user_id}/todos/{non_existing_todo_id}"
    )
    assert delete_response.status_code == 404, "Failed to delete todo item"
    delete_response = test_app.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 204, "Failed to delete user"


def test_delete_todo_item_by_wrong_user(test_app):
    """
    Negative test case
    Test the deletion of a specific todo item by a wrong user.

    This test function ensures that a todo item can be deleted successfully by:
    1. Creating a new user and associated todo item.
    2. Sending a DELETE request to the endpoint '/api/v1/users/{user_id}/todos/{todo_id}'.
    3. Verifying that the response status code is 404, "Failed to delete todo item".
    """
    user_id, todo_response = create_user_and_todo(
        test_app, "Karol", "Wolkanowski", "wolkanowski@gmail.com", "driving", False
    )

    # Assert for todo item creation
    assert todo_response.status_code == 201, "Failed to create todo item"
    todo_created_json = todo_response.json()

    # Get todo ID from the created todo item
    todo_id = todo_created_json["unique_id"]
    non_existing_user_id = todo_id + " abcdefgd"

    # Check the response to delete
    delete_response = test_app.delete(
        f"/api/v1/users/{non_existing_user_id}/todos/{todo_id}"
    )
    assert delete_response.status_code == 404, "Failed to delete todo item"
    delete_response = test_app.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 204, "Failed to delete user"
