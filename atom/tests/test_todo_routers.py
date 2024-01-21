from atom.tests.conftest import test_app
from atom.tests.test_user_routers import create_user, get_user_by_id


# "preperetion, execute and veryfication"
# create the user that already exists
# take this user by id
# noe create the item
# execut response client
# veryfication


def create_user_and_todo(
    test_app, first_name, last_name, email, todo_name, todo_done_or_not
):
    create_user_for_todo = create_user(test_app, first_name, last_name, email)
    assert create_user_for_todo.status_code == 200, "failed to create user"
    created_user_for_todo = create_user_for_todo.json()

    # now take this user id
    user_id = created_user_for_todo["user_id"]

    # create todo_item
    todo_item_data = {
        "todo_name": todo_name,
        "owner_id": user_id,
        "todo_done_or_not": todo_done_or_not,
    }
    response = test_app.post("/todos", json=todo_item_data)
    return user_id, response


def test_read_users_todo(test_app):
    user_id, _ = create_user_and_todo(
        test_app, "Paulina", "Nowakowska", "nowakowska@gmail.com", "gardening", False
    )
    # now take the id of the user

    all_todos_response = test_app.get(f"/users/{user_id}/todos")

    assert all_todos_response.status_code == 200
    assert isinstance(all_todos_response.json(), list)


def test_read_todo_item_by_user(test_app):
    # test create user and create the todo item
    user_id, todo_create = create_user_and_todo(
        test_app, "Anna", "Krolewska", "krolewska@gmail.com", "drinking a water", False
    )
    # check if that was created and is good
    assert todo_create.status_code == 200, "failed to create user"
    todo_created = todo_create.json()
    # take todo_id
    todo_id = todo_created["todo_id"]  # Assuming the ID field is named 'todo_id'
    response = test_app.get("/users/{user_id}/todos/{todo_id}")
    assert response.status_code == 200, "failed to retrive todo item"


def test_create_todo_item_by_user(test_app):
    user_id, created_todo_response = create_user_and_todo(
        test_app, "Maria", "Dunalewicz", "dunalewicz@gmail.com", "go to the gym", False
    )
    assert created_todo_response.status_code == 200, "failed to create user"
    todo_item = created_todo_response.json()
    # veryfication
    assert todo_item["todo_name"] == "go to the gym"
    assert todo_item["owner_id"] == user_id
    assert todo_item["todo_done_or_not"] is False


def test_update_todo_item_by_user(test_app):
    user_id, todo_response = create_user_and_todo(
        test_app, "Danuta", "Polaczek", "dpolaczek00@gmail.com", "cooking", False
    )
    assert todo_response.status_code == 200, "Failed to create todo item"

    todo_created_json = todo_response.json()
    todo_id = todo_created_json["todo_id"]

    updated_data = {
        "todo_name": "doing the dishes",
        "owner_id": user_id,
        "todo_done_or_not": True,
    }

    try:
        # Update the todo item
        update_response = test_app.put(
            f"/users/{user_id}/todos/{todo_id}", json=updated_data
        )
        assert update_response.status_code == 200, "Failed to update todo item"

        # Assert updated data
        updated_todo = update_response.json()
        assert updated_todo["todo_name"] == "doing the dishes"
        assert updated_todo["todo_done_or_not"] is True

    finally:
        # Cleanup: delete the todo item
        test_app.delete(f"/users/{user_id}/todos/{todo_id}")


def test_delete_todo_item_by_user(test_app):
    # First create the user and todo
    user_id, todo_response = create_user_and_todo(
        test_app, "Karol", "Wolowski", "wolowski12443@gmail.com", "driving", False
    )

    # Assert for todo item creation
    assert todo_response.status_code == 200, "Failed to create todo item"
    todo_created_json = todo_response.json()

    # Get todo ID from the created todo item
    todo_id = todo_created_json["todo_id"]

    # Check the response to delete
    delete_response = test_app.delete(f"/users/{user_id}/todos/{todo_id}")
    assert delete_response.status_code == 200, "Failed to delete todo item"
