from app.core.connection_pool import PymysqlConnectionPool

pool = PymysqlConnectionPool(
    maxsize=5,
    host="localhost",
    port=3306,
    user="root",
    password="password",
    database="llmagent",
)

def connection():
    conn = pool.get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
            print(row)
    finally:
        pool.release_connection(conn)