from Model.stats_model import StatsModel

class StatsController:
    def __init__(self):
        self.stats_model = StatsModel()

    def get_all_stats(self):
        total_projects = self.stats_model.get_total_projects()
        total_pledged_amount = self.stats_model.get_total_pledged_amount()
        total_users = self.stats_model.get_total_users()
        total_successful_projects = self.stats_model.get_successful_projects_count()

        # เพิ่มโค้ดสำหรับดึงข้อมูลการสนับสนุนที่สำเร็จและถูกปฏิเสธ
        total_successful_pledges = self.stats_model.get_total_pledges_by_status('success')
        total_rejected_pledges = self.stats_model.get_total_pledges_by_status('rejected')

        return {
            'total_projects': total_projects,
            'total_pledged_amount': total_pledged_amount,
            'total_users': total_users,
            'total_successful_projects': total_successful_projects,
            'total_successful_pledges': total_successful_pledges, 
            'total_rejected_pledges': total_rejected_pledges 
        }
