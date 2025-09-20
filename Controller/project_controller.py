from Model.project_model import ProjectModel
from Model.reward_model import RewardModel
from Model.category_model import CategoryModel
import datetime

class ProjectController:
    def __init__(self):
        self.project_model = ProjectModel()
        self.reward_model = RewardModel()
        self.category_model = CategoryModel()

    def get_all_projects(self):
        return self.project_model.get_all_projects()

    def get_project_details(self, project_id):
        project = self.project_model.get_project_by_id(project_id)
        rewards = self.reward_model.get_rewards_by_project_id(project_id)
        return project, rewards

    def create_project(self, name, goal_amount, deadline, category_id, user_id):
        if not all([name, goal_amount, deadline, category_id, user_id]):
            return False, "All fields are required."
        
        new_project_id = self.project_model.create_project(name, goal_amount, deadline, category_id, user_id)
        if new_project_id is None:
            return False, "Project deadline must be in the future."
        
        return True, "Project created successfully."

    def search_projects(self, query):
        return self.project_model.search_projects_by_name(query)

    def filter_projects(self, category_id):
        return self.project_model.filter_projects_by_category(category_id)
    
    def get_all_categories(self):
        return self.category_model.get_all_categories()

    def sort_projects(self, projects, sort_by):
        """เรียงลำดับรายการโครงการตามตัวเลือก"""
        if sort_by == 'newest':
            # เรียงตาม ID โครงการจากมากไปน้อย (ใหม่สุด)
            return sorted(projects, key=lambda p: p[0], reverse=True)
        elif sort_by == 'ending_soon':
            # เรียงตาม deadline จากน้อยไปมาก (ใกล้หมดเวลาที่สุด)
            return sorted(projects, key=lambda p: datetime.datetime.strptime(p[3], '%Y-%m-%d'))
        elif sort_by == 'most_funded':
            # เรียงตามยอดระดมทุนปัจจุบันจากมากไปน้อย
            return sorted(projects, key=lambda p: p[4], reverse=True)
        else:
            return projects