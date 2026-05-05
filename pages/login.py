import customtkinter as ctk
from tkinter import messagebox
from database.db import check_login
from ui.terms import show_terms_modal

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
        ctk.CTkButton(options_frame, text="Forgot password?", font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#e65c00", fg_color="transparent", hover_color="#f9fafb", width=0, command=self._forgot_password).pack(side="right")

        # Login button
        ctk.CTkButton(inner_card, text="Sign In", command=self.handle_login, fg_color="#e65c00", hover_color="#cc5200", text_color="white", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), height=45, corner_radius=6).pack(fill="x", pady=(0, 10))

        # Terms and conditions for Login
        tc_frame = ctk.CTkFrame(inner_card, fg_color="transparent")
        tc_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(tc_frame, text="By signing in, you agree to our ", font=ctk.CTkFont(family="Segoe UI", size=11), text_color="#6b7280").pack(side="left")
        ctk.CTkButton(tc_frame, text="Terms and Conditions", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color="#e65c00", fg_color="transparent", hover_color="#f9fafb", width=0, command=self._show_terms).pack(side="left")

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
            
            # Route based on user role
            role = result.get("role")
            if role == "admin":
                self.controller.show_frame("AdminFrame")
            elif role == "staff":
                self.controller.show_frame("StaffFrame")
            else:
                self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def _show_terms(self):
        show_terms_modal(self)

    def _forgot_password(self):
        import customtkinter as ctk
        from database.db import reset_password_by_email

        modal = ctk.CTkToplevel(self)
        modal.title("Reset Password")
        modal.geometry("420x320")
        modal.resizable(False, False)
        modal.grab_set()
        modal.configure(fg_color="#F4F5F7")

        hdr = ctk.CTkFrame(modal, fg_color="#E65C00", corner_radius=0, height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text="🔑  Reset Your Password", text_color="white",
                     font=ctk.CTkFont("Segoe UI", 14, "bold")).pack(side="left", padx=20, pady=12)

        body = ctk.CTkFrame(modal, fg_color="#F4F5F7")
        body.pack(fill="both", expand=True, padx=20, pady=16)

        ctk.CTkLabel(body, text="Enter your registered email", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        email_e = ctk.CTkEntry(body, fg_color="white", border_width=1, border_color="#E5E7EB", height=36,
                               placeholder_text="your@email.com")
        email_e.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(body, text="New Password", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        pw1 = ctk.CTkEntry(body, fg_color="white", border_width=1, border_color="#E5E7EB", height=36, show="*")
        pw1.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(body, text="Confirm New Password", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        pw2 = ctk.CTkEntry(body, fg_color="white", border_width=1, border_color="#E5E7EB", height=36, show="*")
        pw2.pack(fill="x", pady=(0, 10))

        def do_reset():
            if pw1.get() != pw2.get():
                messagebox.showerror("Error", "Passwords do not match.")
                return
            if len(pw1.get()) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters.")
                return
            ok, msg = reset_password_by_email(email_e.get().strip(), pw1.get())
            if ok:
                modal.destroy()
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)

        bf = ctk.CTkFrame(modal, fg_color="#F4F5F7")
        bf.pack(fill="x", padx=20, pady=(0, 16))
        ctk.CTkButton(bf, text="Reset Password", fg_color="#E65C00", hover_color="#CC5200", text_color="white",
                      font=ctk.CTkFont("Segoe UI", 11, "bold"), height=36, corner_radius=6, command=do_reset).pack(side="left", padx=(0, 8))
        ctk.CTkButton(bf, text="Cancel", fg_color="white", hover_color="#EDEDED", text_color="#374151",
                      border_width=1, border_color="#D0D5DD", font=ctk.CTkFont("Segoe UI", 10),
                      height=36, corner_radius=6, command=modal.destroy).pack(side="left")
