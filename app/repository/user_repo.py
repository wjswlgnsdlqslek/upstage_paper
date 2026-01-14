from typing import Optional
from app.core.db import pool
from app.models.entities.user import User


def save(name: str, email: str) -> User:
    conn = pool.get_conn()
    cursor = conn.cursor()
    sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
    cursor.execute(sql, (name, email))
    conn.commit()
    user_id = cursor.lastrowid
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return User(**row)


def find_by_id(user_id: int) -> Optional[User]:
    conn = pool.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return User(**row) if row else None


def find_by_email(email: str) -> Optional[User]:
    conn = pool.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return User(**row) if row else None


def find_all() -> list[User]:
    conn = pool.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [User(**row) for row in rows]


def delete(user_id: int) -> bool:
    conn = pool.get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected > 0
