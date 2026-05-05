import customtkinter as ctk
from tkinter import messagebox
from database.db import check_login


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        self.controller = controller

        container = ctk.CTkFrame(self, fg_color="white")
        container.place(relx=0.5, rely=0.5, anchor="center")

        self.photo = controller.icons.get("logo.jpg", size=(120, 120))
        if self.photo:
            import tkinter as tk
            logo_label = tk.Label(container, image=self.photo, bg="white")
            logo_label.pack(pady=(0, 20))

        ctk.CTkLabel(
            container, text="Login", text_color="#333333",
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
            container, text="Login", command=self.handle_login,
            fg_color="#007acc", hover_color="#005f9e", text_color="white",
            font=ctk.CTkFont(family="Segoe UI", size=13), width=300, height=40,
            corner_radius=8,
        ).pack(pady=10)

        ctk.CTkButton(
            container, text="Back",
            command=lambda: controller.show_frame("LandingFrame"),
            fg_color="transparent", hover_color="#f0f0f0", text_color="#999999",
            font=ctk.CTkFont(family="Segoe UI", size=12),
        ).pack()

    def handle_login(self):
        email = self.email_entry.get()
        pwd = self.password_entry.get()

        result = check_login(email, pwd)

        if result:
            self.controller.logged_in_user = email
            if email.lower() == "admin@bbp.com":
                self.controller.show_frame("AdminFrame")
            else:
                self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Error", "Invalid email or password")
