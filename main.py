# D:\CS\MVC\1-68\main.py

from Controller.project_controller import ProjectController
from Controller.pledge_controller import PledgeController
from Controller.stats_controller import StatsController
from Controller.user_controller import UserController # เพิ่มการนำเข้า UserController
from Model.database import initialize_database
from Model.user_model import UserModel
from Model.category_model import CategoryModel
from View.main_view import MainView

def main():
    # 1. เริ่มต้นฐานข้อมูล
    initialize_database()

    # 2. สร้าง Model และ Controller ทั้งหมด
    user_model = UserModel()
    category_model = CategoryModel()
    
    # เพิ่มการสร้าง UserController
    user_controller = UserController()
    
    project_controller = ProjectController()
    pledge_controller = PledgeController()
    stats_controller = StatsController()

    # 3. สร้างแอปพลิเคชัน View และส่ง Controller ที่จำเป็นไปให้
    class AppController:
        def __init__(self):
            self.user_controller = user_controller 
            self.project_controller = project_controller
            self.pledge_controller = pledge_controller
            self.stats_controller = stats_controller
            self.current_user_id = None 
            
        def get_all_projects(self):
            return self.project_controller.get_all_projects()
        
        def get_all_categories(self):
            return self.project_controller.get_all_categories()
            
        def search_projects(self, query):
            return self.project_controller.search_projects(query)

        def filter_projects(self, category_id):
            return self.project_controller.filter_projects(category_id)
            
        def get_project_details(self, project_id):
            return self.project_controller.get_project_details(project_id)
            
        def get_all_stats(self):
            return self.stats_controller.get_all_stats()
        
        def sort_projects(self, projects, sort_by):
            return self.project_controller.sort_projects(projects, sort_by)
    
        # เพิ่มเมธอดสำหรับล็อกอิน
        def login_user(self, username, password):
            user_id = self.user_controller.login_user(username, password)
            if user_id:
                self.current_user_id = user_id
            return user_id

        # เพิ่มเมธอดสำหรับรับค่า user_id
        def set_current_user(self, user_id):
            self.current_user_id = user_id
        
        # เพิ่มเมธอดสำหรับ logout
        def logout_user(self):
            self.current_user_id = None

    app_controller = AppController()
    app = MainView(controller=app_controller)

    # 4. เริ่มรันแอปพลิเคชัน
    app.mainloop()

if __name__ == "__main__":
    main()