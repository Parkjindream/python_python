from flask import Flask, request, jsonify
import os

from database import init_db, add_student, get_student_by_id, add_attendance, get_attendance
import config

# ---------- Setup ----------
app = Flask(__name__)

# สร้าง DB ถ้ายังไม่มี
if not os.path.exists(os.path.join("..", "data", "db.sqlite3")):
    os.makedirs(os.path.join("..", "data"), exist_ok=True)
    init_db()

# ---------- Middleware ----------
def require_api_key(func):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if auth_header != f"Bearer {config.API_KEY}":
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# ---------- Routes ----------
@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "server running"})

@app.route("/api/students", methods=["POST"])
@require_api_key
def enroll_student():
    """
    ลงทะเบียนนักเรียนใหม่
    data = {student_id, name, face_encoding (bytes base64)}
    """
    data = request.json
    if not all(k in data for k in ("student_id", "name", "face_encoding")):
        return jsonify({"error": "Missing fields"}), 400
    try:
        face_bytes = bytes.fromhex(data["face_encoding"])  # เก็บเป็น BLOB
        add_student(data["student_id"], data["name"], face_bytes)
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/attendance", methods=["POST"])
@require_api_key
def mark_attendance():
    """
    บันทึกเวลาเข้าเรียน
    data = {student_id}
    """
    data = request.json
    if "student_id" not in data:
        return jsonify({"error": "Missing student_id"}), 400

    student = get_student_by_id(data["student_id"])
    if not student:
        return jsonify({"error": "Student not found"}), 404

    add_attendance(data["student_id"])
    return jsonify({"status": "success"}), 201

@app.route("/api/attendance", methods=["GET"])
@require_api_key
def list_attendance():
    """
    ดึงรายการเช็กชื่อทั้งหมด
    """
    rows = get_attendance()
    return jsonify([dict(r) for r in rows])

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)

print("hello word")


