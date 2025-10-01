import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "db.sqlite3")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """โหลด schema.sql มาสร้าง DB"""
    schema_path = os.path.join(os.path.dirname(__file__), "models", "schema.sql")
    with get_connection() as conn, open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
        conn.commit()

def add_student(student_id, name, face_encoding_bytes):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO students (student_id, name, face_encoding) VALUES (?, ?, ?)",
            (student_id, name, face_encoding_bytes),
        )
        conn.commit()

def get_student_by_id(student_id):
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        )
        return cur.fetchone()

def add_attendance(student_id):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO attendance (student_id) VALUES (?)", (student_id,)
        )
        conn.commit()

def get_attendance():
    with get_connection() as conn:
        cur = conn.execute("""
            SELECT a.id, a.student_id, s.name, a.timestamp
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            ORDER BY a.timestamp DESC
        """)
        return cur.fetchall()
