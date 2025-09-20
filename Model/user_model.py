import sqlite3
from .database import connect

class UserModel:
    def __init__(self):
        self.conn = connect()

    def create_user(self, username, email):
        """สร้างผู้ใช้ใหม่และคืนค่า ID ที่ถูกสร้างขึ้น"""
        with self.conn as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO User (username, email) VALUES (?, ?)", (username, email))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None  # ชื่อผู้ใช้หรืออีเมลซ้ำ

    def get_user_by_id(self, user_id):
        """ดึงข้อมูลผู้ใช้จาก user_id"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE user_id = ?", (user_id,))
            return cursor.fetchone()

    def get_all_users(self):
        """ดึงข้อมูลผู้ใช้ทั้งหมด"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User")
            return cursor.fetchall()
        
    def get_user_by_username(self, username):
        """ดึงข้อมูลผู้ใช้จากชื่อผู้ใช้ รวมถึงรหัสผ่าน"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, password FROM User WHERE username = ?", (username,))
            return cursor.fetchone()