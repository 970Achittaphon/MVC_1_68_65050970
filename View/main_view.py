import tkinter as tk
from .project_list_view import ProjectListView
from .project_detail_view import ProjectDetailView
from .stats_view import StatsView
from .create_project_view import CreateProjectView
from .login_view import LoginView

class MainView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Crowdfunding Platform")
        self.geometry("800x600")

        self.controller = controller
        
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        menu_frame = tk.Frame(self, relief="groove", bd=2)
        menu_frame.pack(side="top", fill="x")

        # เพิ่มปุ่ม Logout ที่เมนู
        tk.Button(menu_frame, text="Home", command=lambda: self.show_frame("ProjectListView")).pack(side="left", padx=5)
        tk.Button(menu_frame, text="Statistics", command=lambda: self.show_frame("StatsView")).pack(side="left", padx=5)
        tk.Button(menu_frame, text="Logout", command=lambda: self.show_frame("LoginView")).pack(side="left", padx=5)

        self.after(100, lambda: self.show_frame("LoginView")) # เปลี่ยนให้เริ่มที่หน้า LoginView
    
    def show_frame(self, page_name, project_id=None):
        if page_name not in self.frames:
            if page_name == "ProjectListView":
                frame = ProjectListView(parent=self.container, controller=self.controller, main_view=self)
                self.frames[page_name] = frame
            elif page_name == "ProjectDetailView":
                frame = ProjectDetailView(parent=self.container, controller=self.controller, main_view=self, project_id=project_id)
            elif page_name == "StatsView":
                frame = StatsView(parent=self.container, controller=self.controller, main_view=self)
                self.frames[page_name] = frame
            elif page_name == "CreateProjectView":
                frame = CreateProjectView(parent=self.container, controller=self.controller, main_view=self)
                self.frames[page_name] = frame
            elif page_name == "LoginView": # เพิ่มเงื่อนไขนี้
                frame = LoginView(parent=self.container, controller=self.controller, main_view=self)
                self.frames[page_name] = frame
            else:
                raise ValueError("Invalid page_name")
        else:
            frame = self.frames[page_name]
        
        if page_name == "ProjectDetailView":
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()
        else:
            frame = self.frames[page_name]
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()
