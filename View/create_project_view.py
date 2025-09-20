import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class CreateProjectView(tk.Frame):
    def __init__(self, parent, controller, main_view):
        super().__init__(parent)
        self.controller = controller
        self.main_view = main_view
        
        # ปุ่มกลับไปหน้าหลัก
        tk.Button(self, text="<- Back", command=lambda: self.main_view.show_frame("ProjectListView")).pack(anchor="nw", padx=10, pady=10)
        
        tk.Label(self, text="Create New Project", font=("Helvetica", 16)).pack(pady=10)
        
        form_frame = tk.Frame(self)
        form_frame.pack(padx=20, pady=10)

        # ชื่อโครงการ
        tk.Label(form_frame, text="Project Name:").grid(row=0, column=0, sticky="e", pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=10)

        # จำนวนเงินเป้าหมาย
        tk.Label(form_frame, text="Goal Amount (THB):").grid(row=1, column=0, sticky="e", pady=5)
        self.goal_entry = tk.Entry(form_frame)
        self.goal_entry.grid(row=1, column=1, sticky="ew", padx=10)
        
        # วันที่สิ้นสุด (Deadline)
        tk.Label(form_frame, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0, sticky="e", pady=5)
        self.deadline_entry = tk.Entry(form_frame)
        self.deadline_entry.grid(row=2, column=1, sticky="ew", padx=10)
        
        # หมวดหมู่
        tk.Label(form_frame, text="Category:").grid(row=3, column=0, sticky="e", pady=5)
        categories = self.controller.get_all_categories()
        self.category_map = {cat[1]: cat[0] for cat in categories}
        self.category_names = list(self.category_map.keys())
        
        self.category_var = tk.StringVar(self)
        if self.category_names:
            self.category_var.set(self.category_names[0])
        
        category_menu = ttk.OptionMenu(form_frame, self.category_var, *self.category_names)
        category_menu.grid(row=3, column=1, sticky="ew", padx=10)
        
        # ปุ่มยืนยัน
        tk.Button(self, text="Create Project", command=self.handle_create_project).pack(pady=20)
        
    def handle_create_project(self):
        name = self.name_entry.get()
        goal_amount_str = self.goal_entry.get()
        deadline = self.deadline_entry.get()
        category_name = self.category_var.get()
        
        if not all([name, goal_amount_str, deadline, category_name]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            goal_amount = float(goal_amount_str)
            datetime.datetime.strptime(deadline, '%Y-%m-%d')
            category_id = self.category_map.get(category_name)
            
            # TODO: ต้องหา user_id ของผู้ใช้ที่เข้าสู่ระบบจริง
            user_id = 1  # ใช้ user_id 1 เป็นค่าเริ่มต้น
            
            success, message = self.controller.create_project(name, goal_amount, deadline, category_id, user_id)
            
            if success:
                messagebox.showinfo("Success", "Project created successfully!")
                self.main_view.show_frame("ProjectListView")
            else:
                messagebox.showerror("Error", message)

        except ValueError:
            messagebox.showerror("Error", "Invalid Goal Amount or Deadline format.")