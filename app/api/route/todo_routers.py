from fastapi import APIRouter, HTTPException
from app.service import todo_service
from app.models.schemas.todo import TodoCreateRequest, TodoResponse

router = APIRouter()


@router.post("/todos", response_model=TodoResponse)
async def create_todo(todo: TodoCreateRequest):
    new_todo = todo_service.create_todo(todo)
    return TodoResponse(
        id=new_todo.id,
        content=new_todo.content,
        created_at=str(new_todo.created_at)
    )


@router.get("/todos", response_model=list[TodoResponse])
def get_todos():
    todos = todo_service.get_todos()
    return [
        TodoResponse(
            id=todo.id,
            content=todo.content,
            created_at=str(todo.created_at)
        ) for todo in todos
    ]


@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    try:
        todo_service.delete_todo(todo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Todo deleted"}
