import sqlite3
import os


def execute_query(query, param=tuple()):
    db_path = os.path.join(os.getcwd(), 'chinook.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query, param)
    records = cur.fetchall()
    return records