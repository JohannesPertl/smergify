import sqlite3

CONST_DB_FILE = "data.db"


def get_connection():
    """Return the connection to the given database file"""
    conn = None
    try:
        conn = sqlite3.connect(CONST_DB_FILE)
    except Error as e:
        print(e)

    return conn


def get_user_id(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM user WHERE user_name = ?", (username,))
    user_id = cursor.fetchone()
    cursor.close()
    return user_id[0]
