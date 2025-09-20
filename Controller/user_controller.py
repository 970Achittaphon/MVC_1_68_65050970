from Model.user_model import UserModel

class UserController:
    def __init__(self):
        self.user_model = UserModel()

    def login_user(self, username, password):
        """ตรวจสอบชื่อผู้ใช้และรหัสผ่าน"""
        user_data = self.user_model.get_user_by_username(username)
        if user_data:
            user_id, stored_password = user_data
            # ตรวจสอบรหัสผ่านตรงๆ
            if password == stored_password:
                return user_id # ล็อกอินสำเร็จ
        return None # ล็อกอินไม่สำเร็จ