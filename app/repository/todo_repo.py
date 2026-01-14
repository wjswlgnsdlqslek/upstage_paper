from app.core.db import pool
from app.models.entities.todo import Todo


def create_todo(content: str) -> Todo:
    conn = pool.get_conn()
    cursor = conn.cursor()
    sql = "INSERT INTO todo (content) VALUES (%s)"
    cursor.execute(sql, (content,))
    conn.commit()
    todo_id = cursor.lastrowid
    cursor.execute("SELECT * FROM todo WHERE id = %s", (todo_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return Todo(**row)


def get_todos() -> list[Todo]:
    conn = pool.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Todo(**row) for row in rows]


def delete_todo(todo_id: int) -> int:
    conn = pool.get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todo WHERE id = %s", (todo_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected
