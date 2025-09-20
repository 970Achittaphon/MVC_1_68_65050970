import sqlite3
from .database import connect

class RewardModel:
    def __init__(self):
        self.conn = connect()

    def create_reward_tier(self, name, min_pledge_amount, quantity, project_id):
        """สร้างระดับรางวัลใหม่สำหรับโครงการและคืนค่า ID ที่ถูกสร้างขึ้น"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO RewardTier (name, min_pledge_amount, quantity, project_id) VALUES (?, ?, ?, ?)",
                (name, min_pledge_amount, quantity, project_id)
            )
            conn.commit()
            return cursor.lastrowid

    def get_rewards_by_project_id(self, project_id):
        """ดึงรายการรางวัลทั้งหมดของโครงการ"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM RewardTier WHERE project_id = ?", (project_id,))
            return cursor.fetchall()

    def get_reward_by_id(self, reward_id):
        """ดึงข้อมูลรางวัลจาก reward_id"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM RewardTier WHERE reward_id = ?", (reward_id,))
            return cursor.fetchone()
    
    def update_reward_quantity(self, reward_id, new_quantity):
        """อัปเดตจำนวนคงเหลือของรางวัล"""
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE RewardTier SET quantity = ? WHERE reward_id = ?",
                (new_quantity, reward_id)
            )
            conn.commit()