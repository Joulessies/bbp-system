import customtkinter as ctk
from tkinter import messagebox
from database.db import register_user


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        self.controller = controller

        container = ctk.CTkFrame(self, fg_color="white")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            container, text="Register", text_color="#333333",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
        ).pack(pady=(0, 30))

        ctk.CTkLabel(
            container, text="Email Address", text_color="#666666",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        ).pack(anchor="w")
        self.email_entry = ctk.CTkEntry(
            container, font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color="#f5f5f5", text_color="#333333", border_width=0, width=300, height=38,
        )
        self.email_entry.pack(pady=(5, 15))

        ctk.CTkLabel(
            container, text="Password", text_color="#666666",
            font=ctk.CTkFont(family="Segoe UI", size=13),
        ).pack(anchor="w")
        self.password_entry = ctk.CTkEntry(
            container, font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color="#f5f5f5", text_color="#333333", border_width=0, width=300, height=38, show="*",
        )
        self.password_entry.pack(pady=(5, 20))

        ctk.CTkButton(
            container, text="Register", command=self.handle_register,
            fg_color="#28a745", hover_color="#1e7e34", text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13), width=300, height=40,
            corner_radius=8,
        ).pack(pady=10)

        ctk.CTkButton(
            container, text="Back",
            command=lambda: controller.show_frame("LandingFrame"),
            fg_color="transparent", hover_color="#f0f0f0", text_color="#999999",
            font=ctk.CTkFont(family="Segoe UI", size=12),
        ).pack()

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
