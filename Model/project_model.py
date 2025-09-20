import sqlite3
from .database import connect
import datetime

from .database import connect
import datetime

class ProjectModel:
    def __init__(self):
        self.conn = connect()

    def create_project(self, name, goal_amount, deadline, category_id, user_id):
        if datetime.datetime.strptime(deadline, '%Y-%m-%d') < datetime.datetime.now():
            return None

        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Project (name, goal_amount, deadline, current_amount, category_id, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                (name, goal_amount, deadline, 0.0, category_id, user_id)
            )
            conn.commit()
            return cursor.lastrowid

    def get_project_by_id(self, project_id):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Project WHERE project_id = ?", (project_id,))
            return cursor.fetchone()

    def get_all_projects(self):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Project")
            return cursor.fetchall()
            
    def update_current_amount(self, project_id, amount):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Project SET current_amount = current_amount + ? WHERE project_id = ?", (amount, project_id))
            conn.commit()

    def search_projects_by_name(self, query):
        with self.conn as conn:
            cursor = conn.cursor()
            search_query = f"%{query}%"
            cursor.execute("SELECT * FROM Project WHERE name LIKE ?", (search_query,))
            return cursor.fetchall()
            
    def filter_projects_by_category(self, category_id):
        with self.conn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Project WHERE category_id = ?", (category_id,))
            return cursor.fetchall()