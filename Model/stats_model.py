import sqlite3
from .database import connect

class StatsModel:
    def __init__(self):
        """
        เริ่มต้นการเชื่อมต่อฐานข้อมูลโดยใช้ฟังก์ชัน connect()
        จากไฟล์ database.py
        """
        self.conn = connect()

    def get_total_projects(self):
        """นับจำนวนโครงการทั้งหมด"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Project")
        result = cursor.fetchone()
        return result[0] if result else 0

    def get_total_pledged_amount(self):
        """รวมจำนวนเงินที่ได้รับการสนับสนุนทั้งหมด (เฉพาะที่สำเร็จ)"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM Pledge WHERE status = 'success'")
        result = cursor.fetchone()
        return result[0] if result and result[0] is not None else 0.0

    def get_total_users(self):
        """นับจำนวนผู้ใช้ทั้งหมด"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM User")
        result = cursor.fetchone()
        return result[0] if result else 0

    def get_successful_projects_count(self):
        """นับจำนวนโครงการที่บรรลุเป้าหมาย (current_amount >= goal_amount)"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Project WHERE current_amount >= goal_amount")
        result = cursor.fetchone()
        return result[0] if result else 0
        
    def get_total_pledges_by_status(self, status):
        """นับจำนวนการสนับสนุนตามสถานะ (สำเร็จ/ถูกปฏิเสธ)"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Pledge WHERE status = ?", (status,))
        result = cursor.fetchone()
        return result[0] if result else 0