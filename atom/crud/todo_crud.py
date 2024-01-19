from sqlalchemy.orm import Session
from atom.models.todo_model import Todo
from atom.models.user_model import User
from atom.schemas.todo_schema import ToDoCreate, ToDoUpdate
from datetime import datetime
import datetime


def get_all_todos_by_owner(user_id: str, db: Session):
    items = (db.query(Todo).filter(Todo.owner_id == user_id).all())
    return items


# def get


def create_todo_by_owner(item_data: ToDoCreate, db: Session):
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
    item_owner = db.query(Todo).filter(Todo.owner_id == user_id, Todo.todo_id == todo_id).first()
    return item_owner


def update_todo_item_by_owner(user_id: str, todo_id: str, item_data: ToDoUpdate, db: Session):
    # take the task with specific id and check with the user id
    todo_item = db.query(Todo).filter(Todo.todo_id == todo_id, Todo.owner_id == user_id).first()
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
    todo_item_do_delete = get_todo_item_and_owner(user_id, todo_id, db)
    if todo_item_do_delete:
        db.delete(todo_item_do_delete)
        db.commit()
    return todo_item_do_delete
