import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import random

BASE_DIR = Path(__file__).resolve().parent
DATABASE_NAME = BASE_DIR / "crowdfunding.db"

def connect():
    """เชื่อมต่อกับฐานข้อมูลและคืนค่า connection object"""
    return sqlite3.connect(DATABASE_NAME)

def initialize_database():
    """สร้างตารางที่จำเป็นทั้งหมดหากยังไม่มี"""
    with connect() as conn:
        cursor = conn.cursor()
        
        # ตาราง User (แก้ไขคอลัมน์ password ให้ตรงกับโค้ดที่เหลือ)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS User (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)

        # ตาราง Category ใหม่
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Category (
                category_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );
        """)

        # ตาราง Project ที่ถูกปรับแก้
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Project (
                project_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                goal_amount REAL NOT NULL CHECK(goal_amount > 0),
                deadline TEXT NOT NULL,
                current_amount REAL NOT NULL DEFAULT 0.0,
                category_id INTEGER NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES User(user_id),
                FOREIGN KEY (category_id) REFERENCES Category(category_id)
            );
        """)
        
        # ตาราง RewardTier
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS RewardTier (
                reward_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                min_pledge_amount REAL NOT NULL,
                quantity INTEGER,
                project_id INTEGER NOT NULL,
                FOREIGN KEY (project_id) REFERENCES Project(project_id)
            );
        """)
        
        # ตาราง Pledge
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pledge (
                pledge_id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                reward_id INTEGER,
                status TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES User(user_id),
                FOREIGN KEY (project_id) REFERENCES Project(project_id),
                FOREIGN KEY (reward_id) REFERENCES RewardTier(reward_id)
            );
        """)

        # สร้างข้อมูลผู้ใช้ 25 ราย
        users_to_add = [f'user{i}' for i in range(1, 26)]
        for username in users_to_add:
            try:
                # แก้ไขจาก password เป็น password ให้ตรงกับชื่อคอลัมน์ใน CREATE TABLE
                cursor.execute("INSERT INTO User (username, email, password) VALUES (?, ?, ?)", 
                            (username, f'{username}@example.com', '1234'))
            except sqlite3.IntegrityError:
                pass # ผู้ใช้มีอยู่แล้ว
        
        # เพิ่มข้อมูลหมวดหมู่ 8 หมวด
        categories_to_add = ['Technology', 'Art', 'Food', 'Gaming', 'Music', 'Fashion', 'Film', 'Health']
        for category_name in categories_to_add:
            try:
                cursor.execute("INSERT INTO Category (name) VALUES (?)", (category_name,))
            except sqlite3.IntegrityError:
                pass # หมวดหมู่มีอยู่แล้ว
        
        conn.commit()

        # สร้างข้อมูลโครงการและระดับรางวัล
        category_ids = [row[0] for row in cursor.execute("SELECT category_id FROM Category")]
        user_ids = [row[0] for row in cursor.execute("SELECT user_id FROM User")]
        
        projects_data = [
            ("AI-Powered Robot", 50000.0, "Technology"),
            ("Handmade Pottery", 10000.0, "Art"),
            ("Gourmet Coffee Beans", 5000.0, "Food"),
            ("Indie RPG Video Game", 25000.0, "Gaming"),
            ("Vinyl Album of the Month Club", 15000.0, "Music"),
            ("Smart Plant Monitor", 30000.0, "Technology"),
            ("Digital Art Prints", 8000.0, "Art"),
            ("Local Bakery Expansion", 20000.0, "Food"),
            ("Retro Platformer Game", 18000.0, "Gaming"),
            ("Custom Songwriting Service", 12000.0, "Music"),
            ("Sustainable Clothing Line", 22000.0, "Fashion"),
            ("Documentary Film Project", 35000.0, "Film"),
            ("Smart Water Bottle", 17000.0, "Health"),
            ("High-Performance Drone", 60000.0, "Technology"),
            ("Mobile Puzzle Game", 9000.0, "Gaming"),
            ("Acoustic Guitar EP", 11000.0, "Music"),
        ]

        # ทำความสะอาดข้อมูลเก่าก่อนเพิ่มใหม่
        cursor.execute("DELETE FROM Pledge")
        cursor.execute("DELETE FROM RewardTier")
        cursor.execute("DELETE FROM Project")
        conn.commit()

        projects = []
        for name, goal, category_name in projects_data:
            category_id = cursor.execute("SELECT category_id FROM Category WHERE name = ?", (category_name,)).fetchone()[0]
            owner_id = random.choice(user_ids)
            deadline = (datetime.now() + timedelta(days=random.randint(30, 90))).strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO Project (name, goal_amount, deadline, category_id, user_id) VALUES (?, ?, ?, ?, ?)",
                        (name, goal, deadline, category_id, owner_id))
            project_id = cursor.lastrowid
            projects.append({'id': project_id, 'goal': goal, 'user_ids': user_ids, 'owner_id': owner_id})

            # เพิ่มระดับรางวัล 2-3 ระดับ
            min_pledge_1 = goal * 0.05
            min_pledge_2 = goal * 0.15
            min_pledge_3 = goal * 0.3
            cursor.execute("INSERT INTO RewardTier (name, min_pledge_amount, project_id) VALUES (?, ?, ?)",
                        ("Digital Thank You", min_pledge_1, project_id))
            cursor.execute("INSERT INTO RewardTier (name, min_pledge_amount, project_id) VALUES (?, ?, ?)",
                        ("Exclusive Access", min_pledge_2, project_id))
            if random.random() > 0.5: # 50% มีระดับรางวัลที่ 3
                 cursor.execute("INSERT INTO RewardTier (name, min_pledge_amount, project_id) VALUES (?, ?, ?)",
                            ("Physical Item", min_pledge_3, project_id))

        conn.commit()

        # สร้างข้อมูลการสนับสนุน (Pledge)
        all_rewards = [row for row in cursor.execute("SELECT reward_id, min_pledge_amount, project_id FROM RewardTier")]

        for p in projects:
            num_pledges = random.randint(5, 10)
            for _ in range(num_pledges):
                user_id = random.choice([u for u in p['user_ids'] if u != p['owner_id']]) 
                pledge_reward = random.choice([r for r in all_rewards if r[2] == p['id']])
                pledge_amount = pledge_reward[1] * random.uniform(1.0, 2.0)
                status = "success"
                
                if random.random() < 0.2: 
                    status = "rejected"
                    pledge_amount = pledge_reward[1] * random.uniform(0.5, 0.9) 
                
                timestamp = datetime.now().isoformat()
                
                cursor.execute("INSERT INTO Pledge (user_id, project_id, timestamp, amount, reward_id, status) VALUES (?, ?, ?, ?, ?, ?)",
                            (user_id, p['id'], timestamp, pledge_amount, pledge_reward[0], status))
                
                if status == "success":
                    cursor.execute("UPDATE Project SET current_amount = current_amount + ? WHERE project_id = ?",
                                (pledge_amount, p['id']))
        
        conn.commit()
    print("Database initialized successfully with extensive test data.")

if __name__ == '__main__':
    initialize_database()