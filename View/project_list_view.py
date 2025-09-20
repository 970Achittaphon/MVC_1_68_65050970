import tkinter as tk
from tkinter import ttk
import datetime

class ProjectListView(tk.Frame):
    def __init__(self, parent, controller, main_view):
        super().__init__(parent)
        self.controller = controller
        self.main_view = main_view
        self.projects = self.controller.get_all_projects()

        # ส่วนหัว (Header) และส่วนควบคุม
        header_frame = tk.Frame(self)
        header_frame.pack(fill="x", pady=10)
        
        tk.Label(header_frame, text="All Projects", font=("Helvetica", 16)).pack(side="left", padx=10)
        tk.Button(header_frame, text="Create New Project", command=lambda: self.main_view.show_frame("CreateProjectView")).pack(side="left", padx=10)

        # ส่วนค้นหาและกรอง
        search_frame = tk.Frame(header_frame)
        search_frame.pack(side="right", padx=10)
        
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.handle_search).pack(side="left")

        # Dropdown สำหรับกรองตามหมวดหมู่
        categories_from_db = [cat[1] for cat in self.controller.get_all_categories()]
        category_options = ["All Categories"] + categories_from_db
        
        self.category_var = tk.StringVar(self)
        self.category_var.set("All Categories")
        self.category_var.trace("w", self.handle_filter)
        
        category_menu = ttk.OptionMenu(search_frame, self.category_var, "All Categories", *category_options)
        category_menu.pack(side="left", padx=5)
        
        # Dropdown สำหรับเรียงลำดับ
        sort_options = {
            "Newest": "newest",
            "Ending Soon": "ending_soon",
            "Most Funded": "most_funded",
        }
        self.sort_var = tk.StringVar(self)
        self.sort_var.set("Sort By")
        self.sort_var.trace("w", self.handle_sort)
        
        sort_menu = ttk.OptionMenu(search_frame, self.sort_var, "Sort By", *sort_options.keys())
        sort_menu.pack(side="left", padx=5)
        
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # สร้าง Frame ภายใน Canvas เพื่อใช้เป็น container สำหรับรายการโครงการ
        self.project_list_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.project_list_frame, anchor="nw")
        
        # เชื่อมโยงการปรับขนาดของ frame กับ scrollbar
        self.project_list_frame.bind("<Configure>", self.on_frame_configure)
        
        self.display_projects()
    
    def on_frame_configure(self, event):
        """ปรับขนาด scroll region ของ canvas เมื่อ frame ภายในถูกปรับขนาด"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def display_projects(self, projects=None):
        """แสดงรายการโครงการบนหน้าจอ"""
        
        # ลบ widgets เก่าทั้งหมดใน project_list_frame
        for widget in self.project_list_frame.winfo_children():
            widget.destroy()

        if projects is None:
            projects = self.projects
            
        if not projects:
            tk.Label(self.project_list_frame, text="No projects found.").pack(pady=20)
            # อัปเดต scroll region แม้ไม่มีโครงการ
            self.on_frame_configure(None)
            return

        for project in projects:
            project_frame = tk.Frame(self.project_list_frame, bd=1, relief="solid", padx=10, pady=5)
            project_frame.pack(fill="x", pady=5)
            
            tk.Label(project_frame, text=f"Project: {project[1]}", font=("Helvetica", 12)).pack(anchor="w")
            tk.Label(project_frame, text=f"Pledged: {project[4]:.2f} / Goal: {project[2]:.2f}").pack(anchor="w")
            
            tk.Button(project_frame, text="View Details", command=lambda p_id=project[0]: self.main_view.show_frame("ProjectDetailView", p_id)).pack(side="right")
        
        # อัปเดต scroll region หลังการเพิ่มโครงการทั้งหมด
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def handle_search(self):
        query = self.search_entry.get()
        if query:
            projects = self.controller.search_projects(query)
            self.display_projects(projects)
        else:
            self.display_projects(self.projects)
            
    def handle_filter(self, *args):
        category_name = self.category_var.get()
        if category_name == "All Categories":
            self.display_projects(self.projects)
        else:
            categories = self.controller.get_all_categories()
            category_id = next((cat[0] for cat in categories if cat[1] == category_name), None)
            if category_id:
                projects = self.controller.filter_projects(category_id)
                self.display_projects(projects)

    def handle_sort(self, *args):
        sort_by = self.sort_var.get()
        
        sort_map = {
            "Newest": "newest",
            "Ending Soon": "ending_soon",
            "Most Funded": "most_funded",
            "Sort By": None
        }
        
        sort_key = sort_map.get(sort_by)
        
        if sort_key:
            sorted_projects = self.controller.sort_projects(self.projects, sort_key)
            self.display_projects(sorted_projects)
        else:
            self.display_projects(self.projects)