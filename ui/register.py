import tkinter as tk
from tkinter import messagebox
from database.db import register_user

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e1e")
        self.controller = controller
        
        container = tk.Frame(self, bg="#1e1e1e")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(container, text="Register", fg="white", bg="#1e1e1e", font=controller.header_font).pack(pady=(0, 30))
        
        tk.Label(container, text="Email Address", fg="#aaaaaa", bg="#1e1e1e", font=controller.custom_font).pack(anchor="w")
        self.email_entry = tk.Entry(container, font=controller.custom_font, bg="#2d2d2d", fg="white", insertbackground="white", relief="flat", width=25)
        self.email_entry.pack(pady=(5, 15), ipady=5)
        
        tk.Label(container, text="Password", fg="#aaaaaa", bg="#1e1e1e", font=controller.custom_font).pack(anchor="w")
        self.password_entry = tk.Entry(container, font=controller.custom_font, bg="#2d2d2d", fg="white", insertbackground="white", relief="flat", width=25, show="*")
        self.password_entry.pack(pady=(5, 20), ipady=5)
        
        tk.Button(container, text="Register", command=self.handle_register, bg="#28a745", fg="white", font=controller.custom_font, relief="flat", width=20, pady=5).pack(pady=10)
        tk.Button(container, text="Already have an account? Login", command=lambda: controller.show_frame("LoginFrame"), bg="#1e1e1e", fg="#28a745", font=controller.custom_font, relief="flat", activebackground="#1e1e1e").pack()

    def handle_register(self):
        email = self.email_entry.get()
        pwd = self.password_entry.get()
        
        if not email or not pwd:
            messagebox.showwarning("Warning", "Fields cannot be empty")
            return
        
        if "@" not in email or "." not in email:
            messagebox.showwarning("Warning", "Please enter a valid email address")
            return
        
        success, message = register_user(email, pwd)
        
        if success:
            messagebox.showinfo("Success", message + " You can now login.")
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Error", message)
