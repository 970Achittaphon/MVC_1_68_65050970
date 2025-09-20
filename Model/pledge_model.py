import sqlite3
from .database import connect
import datetime

class PledgeModel:
    def __init__(self):
        self.conn = connect()

    def create_pledge(self, user_id, project_id, amount, reward_id=None, status="Succeeded"):
        """สร้างการสนับสนุนใหม่และคืนค่า ID ที่ถูกสร้างขึ้น"""
        timestamp = datetime.datetime.now().isoformat()
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Pledge (user_id, project_id, amount, reward_id, timestamp, status) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, project_id, amount, reward_id, timestamp, status)
            )
            conn.commit()
            return cursor.lastrowid

    def get_pledges_by_project_id(self, project_id):
        """ดึงข้อมูลการสนับสนุนทั้งหมดของโครงการ"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Pledge WHERE project_id = ?", (project_id,))
            return cursor.fetchall()
            
    def get_total_succeeded_pledges(self):
        """ดึงจำนวนการสนับสนุนที่สำเร็จทั้งหมด"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Pledge WHERE status = 'Succeeded'")
            return cursor.fetchone()[0]

    def get_total_rejected_pledges(self):
        """ดึงจำนวนการสนับสนุนที่ถูกปฏิเสธทั้งหมด"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Pledge WHERE status = 'Rejected'")
            return cursor.fetchone()[0]