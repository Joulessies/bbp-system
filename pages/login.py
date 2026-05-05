import customtkinter as ctk
from tkinter import messagebox
from database.db import check_login

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#faf9f6")
        self.controller = controller

        main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)

        # Top Section (Logo and Title)
        top_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        top_frame.pack(pady=(20, 20))

        logo_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        logo_frame.pack()

        self.photo = controller.icons.get("logo.png", size=(40, 40)) or controller.icons.get("logo.jpg", size=(40, 40))
        if self.photo:
            logo_label = ctk.CTkLabel(logo_frame, text="", image=self.photo)
            logo_label.pack(side="left", padx=(0, 10))

        text_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        text_frame.pack(side="left")
        ctk.CTkLabel(text_frame, text="Barangay 183", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#111827").pack(anchor="w")
        ctk.CTkLabel(text_frame, text="Business Permit System", font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#6b7280").pack(anchor="w")

        ctk.CTkLabel(main_container, text="Welcome Back", font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), text_color="#111827").pack(pady=(10, 0))
        ctk.CTkLabel(main_container, text="Sign in to access your account", font=ctk.CTkFont(family="Segoe UI", size=14), text_color="#4b5563").pack(pady=(0, 20))

        # Card Container
        card = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10, border_width=1, border_color="#e5e7eb")
        card.pack(pady=(0, 20))

        inner_card = ctk.CTkFrame(card, fg_color="transparent")
        inner_card.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(inner_card, text="Login to Your Account", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#111827", anchor="w").pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(inner_card, text="Enter your registered email and password to continue", font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#6b7280", anchor="w").pack(fill="x", pady=(0, 20))

        # Email
        ctk.CTkLabel(inner_card, text="Email Address", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#111827", anchor="w").pack(fill="x")
        self.email_entry = ctk.CTkEntry(inner_card, font=ctk.CTkFont(family="Segoe UI", size=13), fg_color="#f4f4f5", text_color="#111827", border_width=0, width=400, height=40, corner_radius=6, placeholder_text="Enter your email")
        self.email_entry.pack(fill="x", pady=(5, 15))

        # Password
        ctk.CTkLabel(inner_card, text="Password", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#111827", anchor="w").pack(fill="x")
        self.password_entry = ctk.CTkEntry(inner_card, font=ctk.CTkFont(family="Segoe UI", size=13), fg_color="#f4f4f5", text_color="#111827", border_width=0, width=400, height=40, corner_radius=6, show="*", placeholder_text="Enter your password")
        self.password_entry.pack(fill="x", pady=(5, 10))

        # Remember me / Forgot password
        options_frame = ctk.CTkFrame(inner_card, fg_color="transparent")
        options_frame.pack(fill="x", pady=(5, 20))
        ctk.CTkCheckBox(options_frame, text="Remember me", font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#4b5563", border_color="#d1d5db", fg_color="#e65c00", hover_color="#cc5200").pack(side="left")
        ctk.CTkButton(options_frame, text="Forgot password?", font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#e65c00", fg_color="transparent", hover_color="#f9fafb", width=0).pack(side="right")

        # Login button
        ctk.CTkButton(inner_card, text="Sign In", command=self.handle_login, fg_color="#e65c00", hover_color="#cc5200", text_color="white", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), height=45, corner_radius=6).pack(fill="x", pady=(0, 20))

        # Register link
        register_frame = ctk.CTkFrame(inner_card, fg_color="transparent")
        register_frame.pack()
        ctk.CTkLabel(register_frame, text="Don't have an account?", font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#4b5563").pack(side="left", padx=(0, 5))
        ctk.CTkButton(register_frame, text="Register here", command=lambda: controller.show_frame("RegisterFrame"), font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#e65c00", fg_color="transparent", hover_color="#f9fafb", width=0).pack(side="left")

        # Footer
        ctk.CTkLabel(main_container, text="Barangay 183 Business Permit System • Caloocan City, Philippines", font=ctk.CTkFont(family="Segoe UI", size=11), text_color="#9ca3af").pack(pady=(20, 0))

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
