from sqlalchemy.orm import Session
from atom.models.todo_model import Todo
from atom.models.user_model import User
from atom.schemas.todo_schema import ToDoCreate, ToDoUpdate
from datetime import datetime
import datetime


def get_all_todos_by_owner(user_id: str, db: Session):
    """
    Retrive all todo items belonging to a specific user

    :param user_id:  the uniqe identifier of the user whose todo items are to be retrieved
    :param db: db session instance from database interactions
    :return: a list of todo model instances representing todo item belonging to the specific user
    """
    items = db.query(Todo).filter(Todo.owner_id == user_id).all()
    return items


def create_todo_by_owner(item_data: ToDoCreate, db: Session):
    """
    Create a new todo item for a specific user .
    The function first check if the user exists and if yes,
    then creates a new todo instance and saves it to database.
    :param item_data:
    :param db:
    :return: a new created todo model instance
    """
    # check if the user exists
    user = db.query(User).filter(User.user_id == item_data.owner_id).first()
    if not user:
        return None

    new_item = Todo(todo_name=item_data.todo_name, owner_id=item_data.owner_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def get_todo_item_and_owner(user_id: str, todo_id: str, db: Session):
    """
    Retrieve a specific todo item along with its owner's information.

    user_id: The unique identifier of the user who owns the todo item.
    todo_id: The unique identifier of the todo item to retrieve.
    db: A SQLAlchemy Session instance for database interaction.
     Returns:
        A Todo model instance representing the requested todo item if found, or None otherwise.
    """
    item_owner = (
        db.query(Todo).filter(Todo.owner_id == user_id, Todo.todo_id == todo_id).first()
    )
    return item_owner


def update_todo_item_by_owner(
    user_id: str, todo_id: str, item_data: ToDoUpdate, db: Session
):
    """
    Update a specific todo item owned by a user.

    This function first retrieves the todo item based on the provided user ID and todo ID. If the todo item is found, it updates the item with the provided data.

    Args:
        user_id: The unique identifier of the user who owns the todo item.
        todo_id: The unique identifier of the todo item to update.
        item_data: An instance of ToDoUpdate schema containing the updated data for the todo item.
        db: A SQLAlchemy Session instance for database interaction.

    Returns:
        The updated Todo model instance, or None if the todo item is not found.
    """

    # take the task with specific id and check with the user id
    todo_item = (
        db.query(Todo).filter(Todo.todo_id == todo_id, Todo.owner_id == user_id).first()
    )
    if not todo_item:
        return None

    if item_data.todo_name is not None:
        todo_item.todo_name = item_data.todo_name
    if item_data.todo_done_or_not is not None:
        todo_item.todo_done_or_not = item_data.todo_done_or_not

    todo_item.todo_updated_at = datetime.datetime.now()
    db.commit()
    return todo_item


def delete_todo_item_by_owner(user_id: str, todo_id: str, db: Session):
    """
    Delete a specific todo item owned by a user.
    This function retrieves the todo item based on the provided user ID and todo ID. If the item is found, it deletes the item from the database.
    The deleted Todo model instance if the item was found and deleted, or None otherwise.
    """
    todo_item_do_delete = get_todo_item_and_owner(user_id, todo_id, db)
    if todo_item_do_delete:
        db.delete(todo_item_do_delete)
        db.commit()
    return todo_item_do_delete
