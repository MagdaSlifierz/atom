from sqlalchemy.orm import Session
from atom.models.todo_model import Todo
from atom.models.user_model import User
from atom.schemas.todo_schema import ToDoCreate, ToDoUpdate
from datetime import datetime
import datetime


def create_todo_by_user(user_id: str, item_data: ToDoCreate, db: Session):
    """
    Create a new todo item for a specific user .
    The function first check if the user_id pass to function has equivalent in database
    Next checks if the user exists and if yes,
    then creates a new todo instance and saves it to database with associate owner_id.

    Return: a new created todo model instance
    """

    # so the user_id 'aaaa' is pass to endpoint and first is checks if matches database
    user = db.query(User).filter(User.unique_user_id == user_id).first()
    if not user:
        return None
    new_item = Todo(todo_name=item_data.todo_name, owner_id=user.id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def get_all_todos_by_owner(user_id: str, db: Session):
    """
    Retrive all todo items belonging to a specific user

    Parameters user_id:  the unique identifier of the user whose todo items are to be retrieved
    db: db session instance from database interactions
    Return: a list of todo model instances representing todo item belonging to the specific user
    """
    # user = db.query(User).filter(User.unique_user_id == user_id).first()
    # items = db.query(Todo).filter(Todo.owner_id == user.id).all()

    items = db.query(Todo).join(User).filter(User.unique_user_id == user_id).all()
    return items


def get_todo_item_by_owner(user_id: str, todo_id: str, db: Session):
    """
    Retrieve a specific todo item belong to the owner.

    user_id: The unique identifier of the user who owns the todo item.
    todo_id: The unique identifier of the todo item to retrieve.
    db: A SQLAlchemy Session instance for database interaction.
    Returns: A Todo model instance representing the requested todo item if found, or None otherwise.
    """
    user = db.query(User).filter(User.unique_user_id == user_id).first()
    if user is None:
        # Handle the case where the user does not exist
        return None
    get_item = (
        db.query(Todo).filter(Todo.owner_id == user.id, Todo.unique_todo_id == todo_id).first()
    )
    return get_item


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
    # user = db.query(User).filter(User.user_id == user_id).first()
    # todo_item = (
    #     db.query(Todo).filter(Todo.todo_id == todo_id, Todo.owner_id == user.id).first()
    # )
    todo_item_to_be_update = get_todo_item_by_owner(user_id, todo_id, db)
    if not todo_item_to_be_update:
        return None

    if item_data.todo_name is not None:
        todo_item_to_be_update.todo_name = item_data.todo_name
    if item_data.todo_done_or_not is not None:
        todo_item_to_be_update.todo_done_or_not = item_data.todo_done_or_not

    todo_item_to_be_update.todo_updated_at = datetime.datetime.now()
    db.commit()
    return todo_item_to_be_update


def delete_todo_item_by_owner(user_id: str, todo_id: str, db: Session):
    """
    Delete a specific todo item owned by a user.
    This function retrieves the todo item based on the provided user ID and todo ID. If the item is found, it deletes the item from the database.
    The deleted Todo model instance if the item was found and deleted, or None otherwise.
    """
    todo_item_to_be_delete = get_todo_item_by_owner(user_id, todo_id, db)
    if todo_item_to_be_delete:
        db.delete(todo_item_to_be_delete)
        db.commit()
    return todo_item_to_be_delete
