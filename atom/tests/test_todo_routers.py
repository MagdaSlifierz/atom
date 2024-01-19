from atom.tests.conftest import test_app
from atom.tests.test_user_routers import create_user, get_user_by_id


# "preperetion, execute and veryfication"


# create the user that already exists
# take this user by id
# noe create the item
# execut response client
# veryfication

def test_create_todo_item_by_user(test_app):
    create_user_for_todo = create_user(test_app, "Eliza", "Rawelec", "eliza@gmail.com")
    assert create_user_for_todo.status_code == 200, "failed to create user"
    created_user_for_todo = create_user_for_todo.json()

    # now take this user id
    user_id = created_user_for_todo["user_id"]
    user_data = get_user_by_id(test_app, user_id)

    # create todo_item
    todo_item_data = {
        "todo_name": "Climbing",
        "owner_id": user_id,
        "todo_done_or_not": False,
    }

    response = test_app.post("/todos", json=todo_item_data)
    if response.status_code == 422:
        print(response.json())
    # veryfication
    assert response.status_code == 200
    assert response.json()["todo_name"] == "Climbing"
    assert response.json()["owner_id"] == user_id
    assert response.json()["todo_done_or_not"] is False
