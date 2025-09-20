import tkinter as tk
from tkinter import messagebox

class LoginView(tk.Frame):
    def __init__(self, parent, controller, main_view):
        super().__init__(parent)
        self.controller = controller
        self.main_view = main_view
        
        tk.Label(self, text="Login", font=("Helvetica", 16)).pack(pady=20)
        
        username_label = tk.Label(self, text="Username:")
        username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        
        password_label = tk.Label(self, text="Password:")
        password_label.pack()
        self.password_entry = tk.Entry(self, show="*") # ซ่อนรหัสผ่าน
        self.password_entry.pack()
        
        tk.Button(self, text="Login", command=self.handle_login).pack(pady=10)
        
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        user_id = self.controller.login_user(username, password)
        if user_id:
            messagebox.showinfo("Success", "Login successful!")
            self.controller.set_current_user(user_id)
            self.main_view.show_frame("ProjectListView")
        else:
            messagebox.showerror("Error", "Invalid username or password.")