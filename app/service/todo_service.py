from app.repository import todo_repo
from app.models.schemas.todo import TodoCreateRequest
from app.models.entities.todo import Todo


def create_todo(todo: TodoCreateRequest) -> Todo:
    return todo_repo.create_todo(todo.content)


def get_todos() -> list[Todo]:
    return todo_repo.get_todos()


def delete_todo(todo_id: int):
    affected_rows = todo_repo.delete_todo(todo_id)
    if affected_rows == 0:
        raise ValueError(f"Todo with id {todo_id} not found")
