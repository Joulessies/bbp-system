import customtkinter as ctk
from tkinter import messagebox
from database.db import register_user

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#faf9f6")
        self.controller = controller

        main_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)

        # Top Section (Logo and Title)
        top_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        top_frame.pack(pady=(20, 10))

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

        ctk.CTkLabel(main_container, text="Create Your Account", font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), text_color="#111827").pack(pady=(5, 0))
        ctk.CTkLabel(main_container, text="Register to start your business permit application", font=ctk.CTkFont(family="Segoe UI", size=14), text_color="#4b5563").pack(pady=(0, 15))

        # Card Container
        card = ctk.CTkFrame(main_container, fg_color="white", corner_radius=10, border_width=1, border_color="#e5e7eb")
        card.pack(pady=(0, 15))

        inner_card = ctk.CTkFrame(card, fg_color="transparent")
        inner_card.pack(padx=30, pady=25, fill="both", expand=True)

        ctk.CTkLabel(inner_card, text="Registration Form", font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), text_color="#111827", anchor="w").pack(fill="x", pady=(0, 2))
        ctk.CTkLabel(inner_card, text="Create your applicant account to apply for business permits in Barangay 183", font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#6b7280", anchor="w").pack(fill="x", pady=(0, 15))

        # Form fields
        # First Name & Last Name row
        name_frame = ctk.CTkFrame(inner_card, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 10))
        
        fname_frame = ctk.CTkFrame(name_frame, fg_color="transparent")
        fname_frame.pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkLabel(fname_frame, text="First Name", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#111827", anchor="w").pack(fill="x")
        self.fname_entry = ctk.CTkEntry(fname_frame, font=ctk.CTkFont(family="Segoe UI", size=13), fg_color="#f4f4f5", text_color="#111827", border_width=0, height=38, corner_radius=6, placeholder_text="Juan", width=195)
        self.fname_entry.pack(fill="x", pady=(5, 0))

        lname_frame = ctk.CTkFrame(name_frame, fg_color="transparent")
        lname_frame.pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(lname_frame, text="Last Name", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#111827", anchor="w").pack(fill="x")
        self.lname_entry = ctk.CTkEntry(lname_frame, font=ctk.CTkFont(family="Segoe UI", size=13), fg_color="#f4f4f5", text_color="#111827", border_width=0, height=38, corner_radius=6, placeholder_text="Dela Cruz", width=195)
        self.lname_entry.pack(fill="x", pady=(5, 0))

        # Email
        ctk.CTkLabel(inner_card, text="Email Address *", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#111827", anchor="w").pack(fill="x")
        self.email_entry = ctk.CTkEntry(inner_card, font=ctk.CTkFont(family="Segoe UI", size=13), fg_color="#f4f4f5", text_color="#111827", border_width=0, width=400, height=38, corner_radius=6, placeholder_text="your.email@example.com")
        self.email_entry.pack(fill="x", pady=(5, 10))

        # Contact Number
        ctk.CTkLabel(inner_card, text="Contact Number", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#111827", anchor="w").pack(fill="x")
        self.contact_entry = ctk.CTkEntry(inner_card, font=ctk.CTkFont(family="Segoe UI", size=13), fg_color="#f4f4f5", text_color="#111827", border_width=0, width=400, height=38, corner_radius=6, placeholder_text="09XX XXX XXXX")
        self.contact_entry.pack(fill="x", pady=(5, 10))

        # Complete Address
        ctk.CTkLabel(inner_card, text="Complete Address *", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#111827", anchor="w").pack(fill="x")
        self.address_entry = ctk.CTkEntry(inner_card, font=ctk.CTkFont(family="Segoe UI", size=13), fg_color="#f4f4f5", text_color="#111827", border_width=0, width=400, height=38, corner_radius=6, placeholder_text="Block, Lot, Street, Barangay 183, Caloocan City")
        self.address_entry.pack(fill="x", pady=(5, 10))

        # Password
        ctk.CTkLabel(inner_card, text="Password *", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#111827", anchor="w").pack(fill="x")
        
        pwd_frame = ctk.CTkFrame(inner_card, fg_color="#f4f4f5", corner_radius=6, height=38)
        pwd_frame.pack(fill="x", pady=(5, 10))
        
        self.password_entry = ctk.CTkEntry(pwd_frame, font=ctk.CTkFont(family="Segoe UI", size=13), fg_color="transparent", text_color="#111827", border_width=0, show="*", placeholder_text="Create password")
        self.password_entry.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        self.pwd_btn = ctk.CTkButton(pwd_frame, text="Show", width=40, fg_color="transparent", hover_color="#e5e7eb", text_color="#6b7280", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), command=self.toggle_pwd)
        self.pwd_btn.pack(side="right", padx=(0, 5))

        # Password Requirements Checklist
        self.req_frame = ctk.CTkFrame(inner_card, fg_color="#f8fafc", corner_radius=6, border_width=1, border_color="#e2e8f0")
        self.req_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(self.req_frame, text="Password Requirements:", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#1e293b", anchor="w").pack(fill="x", padx=15, pady=(10, 5))

        self.req_labels = []
        self.req_rules = [
            ("length", "At least 8 characters long"),
            ("upper", "Contains at least one uppercase letter (A-Z)"),
            ("lower", "Contains at least one lowercase letter (a-z)"),
            ("number", "Contains at least one number (0-9)"),
            ("special", "Contains at least one special character (!@#$%^&*)")
        ]
        
        for key, text in self.req_rules:
            row = ctk.CTkFrame(self.req_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=2)
            icon = ctk.CTkLabel(row, text="○", font=ctk.CTkFont(size=14), text_color="#94a3b8", width=20)
            icon.pack(side="left")
            label = ctk.CTkLabel(row, text=text, font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#64748b")
            label.pack(side="left", padx=(5, 0))
            self.req_labels.append({"key": key, "icon": icon, "label": label})
            
        ctk.CTkFrame(self.req_frame, fg_color="transparent", height=10).pack()
        self.password_entry.bind("<KeyRelease>", self._check_password_requirements)

        # Confirm Password
        ctk.CTkLabel(inner_card, text="Confirm Password *", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#111827", anchor="w").pack(fill="x")
        
        cpwd_frame = ctk.CTkFrame(inner_card, fg_color="#f4f4f5", corner_radius=6, height=38)
        cpwd_frame.pack(fill="x", pady=(5, 15))
        
        self.confirm_password_entry = ctk.CTkEntry(cpwd_frame, font=ctk.CTkFont(family="Segoe UI", size=13), fg_color="transparent", text_color="#111827", border_width=0, show="*", placeholder_text="Confirm password")
        self.confirm_password_entry.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        self.cpwd_btn = ctk.CTkButton(cpwd_frame, text="Show", width=40, fg_color="transparent", hover_color="#e5e7eb", text_color="#6b7280", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), command=self.toggle_cpwd)
        self.cpwd_btn.pack(side="right", padx=(0, 5))

        # Terms and conditions checkbox
        tc_frame = ctk.CTkFrame(inner_card, fg_color="transparent")
        tc_frame.pack(fill="x", pady=(0, 15))
        self.tc_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(tc_frame, text="", variable=self.tc_var, width=20, border_color="#d1d5db", fg_color="#e65c00", hover_color="#cc5200").pack(side="left")
        ctk.CTkLabel(tc_frame, text="I agree to the ", font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#4b5563").pack(side="left")
        ctk.CTkLabel(tc_frame, text="Terms and Conditions", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#e65c00").pack(side="left")
        ctk.CTkLabel(tc_frame, text=" and ", font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#4b5563").pack(side="left")
        ctk.CTkLabel(tc_frame, text="Privacy Policy", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#e65c00").pack(side="left")

        # Create account button
        ctk.CTkButton(inner_card, text="Create Account", command=self.handle_register, fg_color="#e65c00", hover_color="#cc5200", text_color="white", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), height=45, corner_radius=6).pack(fill="x", pady=(0, 15))

        # Sign in link
        login_frame = ctk.CTkFrame(inner_card, fg_color="transparent")
        login_frame.pack()
        ctk.CTkLabel(login_frame, text="Already have an account?", font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#4b5563").pack(side="left", padx=(0, 5))
        ctk.CTkButton(login_frame, text="Sign in here", command=lambda: controller.show_frame("LoginFrame"), font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#e65c00", fg_color="transparent", hover_color="#f9fafb", width=0).pack(side="left")

        # Footer
        ctk.CTkLabel(main_container, text="Barangay 183 Business Permit System • Caloocan City, Philippines", font=ctk.CTkFont(family="Segoe UI", size=11), text_color="#9ca3af").pack(pady=(10, 0))

    def toggle_pwd(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
            self.pwd_btn.configure(text="Hide")
        else:
            self.password_entry.configure(show="*")
            self.pwd_btn.configure(text="Show")

    def toggle_cpwd(self):
        if self.confirm_password_entry.cget("show") == "*":
            self.confirm_password_entry.configure(show="")
            self.cpwd_btn.configure(text="Hide")
        else:
            self.confirm_password_entry.configure(show="*")
            self.cpwd_btn.configure(text="Show")

    def _check_password_requirements(self, event=None):
        pwd = self.password_entry.get()
        import re
        checks = {
            "length": len(pwd) >= 8,
            "upper": bool(re.search(r'[A-Z]', pwd)),
            "lower": bool(re.search(r'[a-z]', pwd)),
            "number": bool(re.search(r'[0-9]', pwd)),
            "special": bool(re.search(r'[!@#$%^&*]', pwd))
        }
        
        for req in self.req_labels:
            if checks[req["key"]]:
                req["icon"].configure(text="✓", text_color="#16a34a")
                req["label"].configure(text_color="#16a34a")
            else:
                req["icon"].configure(text="○", text_color="#94a3b8")
                req["label"].configure(text_color="#64748b")

    def handle_register(self):
        email = self.email_entry.get()
        pwd = self.password_entry.get()
        confirm_pwd = self.confirm_password_entry.get()
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()

        if not email or not pwd or not confirm_pwd:
            messagebox.showwarning("Warning", "Required fields cannot be empty")
            return

        import re
        if len(pwd) < 8 or not re.search(r'[A-Z]', pwd) or not re.search(r'[a-z]', pwd) or not re.search(r'[0-9]', pwd) or not re.search(r'[!@#$%^&*]', pwd):
            messagebox.showwarning("Warning", "Password does not meet all security requirements")
            return

        if pwd != confirm_pwd:
            messagebox.showwarning("Warning", "Passwords do not match")
            return

        if not self.tc_var.get():
            messagebox.showwarning("Warning", "You must agree to the Terms and Conditions")
            return

        if "@" not in email or "." not in email:
            messagebox.showwarning("Warning", "Please enter a valid email address")
            return

        success, message = register_user(email, pwd, fname, lname)

        if success:
            messagebox.showinfo("Success", message + " You can now login.")
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Error", message)
