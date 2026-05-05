import tkinter as tk
from tkinter import messagebox
from database.db import check_login

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e1e")
        self.controller = controller
        
        # UI Elements
        container = tk.Frame(self, bg="#1e1e1e")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(container, text="Login", fg="white", bg="#1e1e1e", font=controller.header_font).pack(pady=(0, 30))
        
        tk.Label(container, text="Email Address", fg="#aaaaaa", bg="#1e1e1e", font=controller.custom_font).pack(anchor="w")
        self.email_entry = tk.Entry(container, font=controller.custom_font, bg="#2d2d2d", fg="white", insertbackground="white", relief="flat", width=25)
        self.email_entry.pack(pady=(5, 15), ipady=5)
        
        tk.Label(container, text="Password", fg="#aaaaaa", bg="#1e1e1e", font=controller.custom_font).pack(anchor="w")
        self.password_entry = tk.Entry(container, font=controller.custom_font, bg="#2d2d2d", fg="white", insertbackground="white", relief="flat", width=25, show="*")
        self.password_entry.pack(pady=(5, 20), ipady=5)
        
        tk.Button(container, text="Login", command=self.handle_login, bg="#007acc", fg="white", font=controller.custom_font, relief="flat", width=20, pady=5).pack(pady=10)
        tk.Button(container, text="Don't have an account? Register", command=lambda: controller.show_frame("RegisterFrame"), bg="#1e1e1e", fg="#007acc", font=controller.custom_font, relief="flat", activebackground="#1e1e1e").pack()

    def handle_login(self):
        email = self.email_entry.get()
        pwd = self.password_entry.get()
        
        result = check_login(email, pwd)
        
        if result:
            self.controller.logged_in_user = email
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Error", "Invalid email or password")
