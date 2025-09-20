import tkinter as tk

class ProjectDetailView(tk.Frame):
    def __init__(self, parent, controller, main_view, project_id):
        super().__init__(parent)
        self.controller = controller
        self.main_view = main_view
        self.project_id = project_id
        
        # ดึงข้อมูลโครงการและรางวัลจาก Controller
        self.project, self.rewards = self.controller.get_project_details(self.project_id)

        if not self.project:
            tk.Label(self, text="Project not found.").pack(pady=20)
            return

        # ปุ่มกลับไปหน้าหลัก
        tk.Button(self, text="<- Back", command=lambda: self.main_view.show_frame("ProjectListView")).pack(anchor="nw", padx=10, pady=10)

        # ส่วนแสดงรายละเอียดโครงการ
        tk.Label(self, text=self.project[1], font=("Helvetica", 24)).pack(pady=10)
        tk.Label(self, text=f"Goal: {self.project[2]:,.2f} THB").pack()
        
        # Progress Bar
        progress_frame = tk.Frame(self)
        progress_frame.pack(pady=10)
        
        self.progress_bar = tk.Canvas(progress_frame, width=300, height=20, bg="lightgray")
        self.progress_bar.pack(side="left")
        
        current_amount = self.project[4]
        goal_amount = self.project[2]
        progress_ratio = current_amount / goal_amount if goal_amount > 0 else 0
        progress_width = 300 * progress_ratio if progress_ratio <= 1 else 300
        
        self.progress_bar.create_rectangle(0, 0, progress_width, 20, fill="green", outline="")
        
        tk.Label(progress_frame, text=f" {current_amount:,.2f} THB").pack(side="left")

        # ส่วนแสดงระดับรางวัล
        tk.Label(self, text="Reward Tiers", font=("Helvetica", 16)).pack(pady=10)
        for reward in self.rewards:
            reward_frame = tk.Frame(self, bd=1, relief="solid", padx=10, pady=5)
            reward_frame.pack(fill="x", pady=5)
            tk.Label(reward_frame, text=f"Reward: {reward[1]}").pack(anchor="w")
            tk.Label(reward_frame, text=f"Pledge for {reward[2]:,.2f} THB").pack(anchor="w")
            tk.Label(reward_frame, text=f"Quantity: {reward[3]}").pack(anchor="w")
            
            # ปุ่มสนับสนุน
            tk.Button(reward_frame, text="Pledge", command=lambda r_id=reward[0]: self.handle_pledge(r_id)).pack(side="right")
    
    def handle_pledge(self, reward_id):
        # ฟังก์ชันนี้จะถูกเรียกเมื่อผู้ใช้คลิกปุ่ม Pledge
        # ตัวอย่างการเรียก Pledge Controller (ต้องมี UI ให้ผู้ใช้กรอกจำนวนเงินและเลือกผู้ใช้ก่อน)
        # self.controller.create_pledge(user_id, self.project_id, amount, reward_id)
        # จากนั้นก็อัปเดตหน้าจอ
        print(f"Pledge clicked for reward ID: {reward_id}")