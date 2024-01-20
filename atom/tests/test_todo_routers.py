from atom.tests.conftest import test_app
from atom.tests.test_user_routers import create_user, get_user_by_id


# "preperetion, execute and veryfication"


# create the user that already exists
# take this user by id
# noe create the item
# execut response client
# veryfication


def create_user_and_todo(test_app, first_name, last_name, email, todo_name, todo_done_or_not):
    create_user_for_todo = create_user(
        test_app, first_name, last_name, email
    )
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


def test_update_todo_item_by_user(test_app):
    # first create the user and todo item
    user_id, todo = create_user_and_todo(test_app, "Olga", "Jurek", "jurek@gmail.com", "cleaning", False)
    # check the user with asser
    assert todo.status_code == 200
    # convert to json
    todo_created_json = todo.json()
    # take the todoitem id
    todo_id = todo_created_json["todo_id"]
    # prepere updated data
    updated_data = {
        "todo_name": "doing the laundry",
        "owner_id": user_id,
        "todo_done_or_not": True,
    }
    update_response = test_app.put(f"/users/{user_id}/todos/{todo_id}", json=updated_data)
    assert update_response.status_code == 200
    # Assert updated data
    # update_todo = update_response.json()
    # assert update_todo["todo_name"] == "doing the dishes"
    # assert update_todo["owner_id"] == user_id
    # assert update_todo["todo_done_or_not"] is True
    update_message = update_response.json()
    assert update_message["message"] == "Task was successfully updated"

    test_app.delete(f"/users/{user_id}/todos/{todo_id}")

# def test_read_todo_item_by_user(test_app):
#     # test create user and create the todo item
#     user_id, todo_create = create_user_and_todo(test_app, "Anna", "Krolewicz", "ak@gmail.com", "drink", False)
#     # check if that was created and is good
#     assert todo_create.status_code == 200, "failed to create user"
#     todo_created = todo_create.json()
#     # take todo_id
#     todo_id = todo_created["todo_id"]  # Assuming the ID field is named 'todo_id'
#     response = test_app.get("/users/{user_id}/todos/{todo_id}")
#     assert response.status_code == 200, "failed to retrive todo item"


# def test_create_todo_item_by_user(test_app):
#     user_id, created_todo_response = create_user_and_todo(
#         test_app, "Jola", "Dulek", "dulek_jol@gmail.com", "walk", False
#     )
#     assert created_todo_response.status_code == 200, "failed to create user"
#     todo_item = created_todo_response.json()
#     # veryfication
#     assert todo_item["todo_name"] == "walk"
#     assert todo_item["owner_id"] == user_id
#     assert todo_item["todo_done_or_not"] is False


# def test_read_users_todo(test_app):
#     user_id, _ = create_user_and_todo(test_app, "Paulina", "Krol", "krol_p12@gmail.com", "horses", False
#                                       )
#     # now take the id of the user
#
#     all_todos_response = test_app.get(f"/users/{user_id}/todos")
#
#     assert all_todos_response.status_code == 200
#     assert isinstance(all_todos_response.json(), list)
# print(all_todos_response.json())
