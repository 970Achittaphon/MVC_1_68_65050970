from Model.pledge_model import PledgeModel
from Model.project_model import ProjectModel
from Model.reward_model import RewardModel
import datetime

class PledgeController:
    def __init__(self):
        self.pledge_model = PledgeModel()
        self.project_model = ProjectModel()
        self.reward_model = RewardModel()

    def create_pledge(self, user_id, project_id, amount, reward_id=None):
        """สร้างการสนับสนุนใหม่พร้อมตรวจสอบความถูกต้องตาม Business Rules"""
        project = self.project_model.get_project_by_id(project_id)
        if not project:
            return False, "Project not found."

        # Rule 1: วันสิ้นสุดต้องอยู่ในอนาคต
        if datetime.datetime.strptime(project[3], '%Y-%m-%d') < datetime.datetime.now():
            self.pledge_model.create_pledge(user_id, project_id, amount, reward_id, status="Rejected")
            return False, "Project has already ended."

        # Rule 2 & 3: ตรวจสอบรางวัลและจำนวนเงิน
        if reward_id:
            reward = self.reward_model.get_reward_by_id(reward_id)
            if not reward:
                return False, "Reward tier not found."
            
            # Rule 2: จำนวนเงินที่สนับสนุน >= ยอดขั้นต่ำ
            if amount < reward[2]:
                self.pledge_model.create_pledge(user_id, project_id, amount, reward_id, status="Rejected")
                return False, "Pledge amount is less than the minimum for this reward."

            # Rule 3: จำนวนคงเหลือ > 0 (ถ้ามีโควตา)
            if reward[3] is not None and reward[3] <= 0:
                self.pledge_model.create_pledge(user_id, project_id, amount, reward_id, status="Rejected")
                return False, "Reward tier is out of stock."
            
        # ถ้าผ่านการตรวจสอบทั้งหมด
        self.pledge_model.create_pledge(user_id, project_id, amount, reward_id, status="Succeeded")
        
        # Rule 4: อัปเดตยอดรวมและลดโควตา
        self.project_model.update_current_amount(project_id, amount)
        if reward_id and reward[3] is not None:
            self.reward_model.update_reward_quantity(reward_id, reward[3] - 1)
            
        return True, "Pledge successful!"