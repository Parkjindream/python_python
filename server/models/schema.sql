-- สร้างตารางเก็บข้อมูลนักเรียน
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    face_encoding BLOB NOT NULL
);

-- สร้างตารางบันทึกเวลาเข้าเรียน
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES students(student_id)
);

-- เพิ่ม index เพื่อให้ค้นหาข้อมูลเร็วขึ้น
CREATE INDEX IF NOT EXISTS idx_attendance_student_time
ON attendance(student_id, timestamp);
