import tkinter as tk
from tkinter import ttk

class StatsView(tk.Frame):
    def __init__(self, parent, controller, main_view):
        super().__init__(parent)
        self.controller = controller
        self.main_view = main_view
        
        # UI Elements
        tk.Label(self, text="Platform Statistics", font=("Helvetica", 16)).pack(pady=20)

        self.stats_frame = tk.Frame(self)
        self.stats_frame.pack(pady=10)
        
        self.total_projects_label = tk.Label(self.stats_frame, text="Total Projects: 0")
        self.total_projects_label.pack(anchor="w", padx=10, pady=5)
        
        self.total_pledged_label = tk.Label(self.stats_frame, text="Total Pledged: 0.00 THB")
        self.total_pledged_label.pack(anchor="w", padx=10, pady=5)
        
        self.total_users_label = tk.Label(self.stats_frame, text="Total Users: 0")
        self.total_users_label.pack(anchor="w", padx=10, pady=5)
        
        self.successful_projects_label = tk.Label(self.stats_frame, text="Successful Projects: 0")
        self.successful_projects_label.pack(anchor="w", padx=10, pady=5)

        # เพิ่ม Label สำหรับการสนับสนุนที่สำเร็จและถูกปฏิเสธ
        self.successful_pledges_label = tk.Label(self.stats_frame, text="Successful Pledges: 0")
        self.successful_pledges_label.pack(anchor="w", padx=10, pady=5)

        self.rejected_pledges_label = tk.Label(self.stats_frame, text="Rejected Pledges: 0")
        self.rejected_pledges_label.pack(anchor="w", padx=10, pady=5)
        
        self.update_stats()

    def update_stats(self):
        stats = self.controller.get_all_stats()
        
        self.total_projects_label.config(text=f"Total Projects: {stats['total_projects']}")
        self.total_pledged_label.config(text=f"Total Pledged: {stats['total_pledged_amount']:.2f} THB")
        self.total_users_label.config(text=f"Total Users: {stats['total_users']}")
        self.successful_projects_label.config(text=f"Successful Projects: {stats['total_successful_projects']}")
        
        # อัปเดตข้อมูลการสนับสนุนที่สำเร็จและถูกปฏิเสธ
        self.successful_pledges_label.config(text=f"Successful Pledges: {stats['total_successful_pledges']}")
        self.rejected_pledges_label.config(text=f"Rejected Pledges: {stats['total_rejected_pledges']}")