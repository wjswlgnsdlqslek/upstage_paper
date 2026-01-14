from app.core.db import pool
from app.models.entities.chat import Chat, Role


def add_conversation(user_id: int, role: Role, message: str) -> Chat:
    conn = pool.get_conn()
    cursor = conn.cursor()
    sql = "INSERT INTO conversations (user_id, role, message) VALUES (%s, %s, %s)"
    cursor.execute(sql, (user_id, role.value, message))
    conn.commit()
    chat_id = cursor.lastrowid
    cursor.execute("SELECT * FROM conversations WHERE id = %s", (chat_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return Chat(**row)


def get_recent_conversations(user_id: int, limit: int = 20) -> list[Chat]:
    conn = pool.get_conn()
    cursor = conn.cursor()
    sql = """
            SELECT id, user_id, role, message, created_at
            FROM conversations
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s
            """
    cursor.execute(sql, (user_id, limit))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [Chat(**row) for row in rows]


def save_chat_transaction(user_id: int, user_msg: str, assistant_msg: str):
    conn = pool.get_conn()
    try:
        with conn.cursor() as cursor:
            # 1) 사용자 메시지 저장
            sql1 = "INSERT INTO conversations (user_id, role, message) VALUES (%s, 'user', %s)"
            cursor.execute(sql1, (user_id, user_msg))

            # 2) 어시스턴트 메시지 저장
            sql2 = "INSERT INTO conversations (user_id, role, message) VALUES (%s, 'assistant', %s)"
            cursor.execute(sql2, (user_id, assistant_msg))

        conn.commit()  # 두 개가 모두 성공한 경우에만 commit

    except Exception as e:
        conn.rollback()  # 하나라도 실패하면 전체 취소
        raise e
    finally:
        pool.release_connection(conn)


def find_by_id(chat_id: int) -> Chat | None:
    conn = pool.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversations WHERE id = %s", (chat_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return Chat(**row) if row else None