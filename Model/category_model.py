import sqlite3
from .database import connect

class CategoryModel:
    def __init__(self):
        self.conn = connect()

    def create_category(self, name):
        """สร้างหมวดหมู่ใหม่และคืนค่า ID ที่ถูกสร้างขึ้น"""
        with self.conn as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Category (name) VALUES (?)", (name,))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None  # ชื่อหมวดหมู่ซ้ำ

    def get_all_categories(self):
        """ดึงรายการหมวดหมู่ทั้งหมด"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Category")
            return cursor.fetchall()