import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from database.db import (
    get_user_applications, get_user_permits, submit_application,
    get_notifications, mark_all_notifications_read, clear_all_notifications,
)


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F4F5F7")
        self.controller = controller
        self.current_section = "My Applications"
        self.nav_buttons = {}
        self.form_vars = {}
        self.uploaded_documents = {}
        self.doc_buttons = {}
        self.total_size_label = None
        self.max_upload_bytes = 500 * 1024 * 1024
        self._build_layout()

    def _build_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_main_content()

    # ── Sidebar ──────────────────────────────────────────────
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, fg_color="#F9F9F9", width=220, corner_radius=0,
                          border_width=1, border_color="#E5E7EB")
        sb.grid(row=0, column=0, sticky="ns")
        sb.grid_propagate(False)
        sb.grid_rowconfigure(3, weight=1)

        brand = ctk.CTkFrame(sb, fg_color="#F9F9F9")
        brand.grid(row=0, column=0, sticky="ew", padx=14, pady=(16, 4))
        logo = self.controller.icons.get("lgu_logo.png", size=(34, 34))
        if logo:
            self._logo = logo
            ctk.CTkLabel(brand, text="", image=self._logo, fg_color="#F9F9F9").pack(side="left", padx=(0, 8))
        bt = ctk.CTkFrame(brand, fg_color="#F9F9F9")
        bt.pack(side="left")
        ctk.CTkLabel(bt, text="Barangay 183", text_color="#0B1A3A",
                     font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(anchor="w")
        ctk.CTkLabel(bt, text="Caloocan City", text_color="#5F6368",
                     font=ctk.CTkFont("Segoe UI", 9)).pack(anchor="w")

        ctk.CTkLabel(sb, text="👤  Business Owner", text_color="#E55A00",
                     font=ctk.CTkFont("Segoe UI", 11, "bold")).grid(
            row=1, column=0, sticky="w", padx=18, pady=(8, 12))

        nav = ctk.CTkFrame(sb, fg_color="#F9F9F9")
        nav.grid(row=2, column=0, sticky="ew", padx=10)
        for lbl in ["My Applications", "New Application", "Notifications"]:
            self._add_nav(nav, lbl, active=(lbl == "My Applications"))

        ctk.CTkButton(sb, text="Logout", command=self._logout,
                      fg_color="#F7F7F7", hover_color="#EDEDED", text_color="#111827",
                      border_width=1, border_color="#D0D5DD",
                      font=ctk.CTkFont("Segoe UI", 10), height=36, corner_radius=6,
                      ).grid(row=4, column=0, sticky="ew", padx=12, pady=12)

    def _add_nav(self, parent, title, active=False):
        fg = "#F05A00" if active else "transparent"
        tc = "white" if active else "#111827"
        hv = "#D94B00" if active else "#EDEDED"
        btn = ctk.CTkButton(parent, text=title, anchor="w",
                            command=lambda t=title: self._switch(t),
                            fg_color=fg, hover_color=hv, text_color=tc,
                            font=ctk.CTkFont("Segoe UI", 11, "bold" if active else "normal"),
                            height=36, corner_radius=6)
        btn.pack(fill="x", pady=2)
        self.nav_buttons[title] = btn

    def _switch(self, section):
        self.current_section = section
        for t, b in self.nav_buttons.items():
            act = t == section
            b.configure(fg_color="#F05A00" if act else "transparent",
                        text_color="white" if act else "#111827",
                        hover_color="#D94B00" if act else "#EDEDED",
                        font=ctk.CTkFont("Segoe UI", 11, "bold" if act else "normal"))
        self._render()

    def _logout(self):
        self.controller.logged_in_user = None
        self.controller.show_frame("LandingFrame")

    # ── Main content ─────────────────────────────────────────
    def _build_main_content(self):
        main = ctk.CTkFrame(self, fg_color="#F4F5F7", corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(main, fg_color="#F4F5F7")
        top.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 0))
        top.grid_columnconfigure(0, weight=1)
        self.top_title = ctk.CTkLabel(top, text="Welcome Back!",
                                      text_color="#101828",
                                      font=ctk.CTkFont("Segoe UI", 26, "bold"))
        self.top_title.grid(row=0, column=0, sticky="w")
        self.top_sub = ctk.CTkLabel(top, text="", text_color="#6B7280",
                                    font=ctk.CTkFont("Segoe UI", 11))
        self.top_sub.grid(row=1, column=0, sticky="w", pady=(2, 0))
        self.top_action = ctk.CTkButton(top, text="+  New Application",
                                        command=lambda: self._switch("New Application"),
                                        fg_color="#F05A00", hover_color="#D94B00",
                                        text_color="white",
                                        font=ctk.CTkFont("Segoe UI", 11, "bold"),
                                        height=38, corner_radius=6)
        self.top_action.grid(row=0, column=1, rowspan=2, sticky="e", padx=(10, 0))

        self.host = ctk.CTkScrollableFrame(main, fg_color="#F4F5F7")
        self.host.grid(row=1, column=0, sticky="nsew", padx=24, pady=(12, 0))
        self.host.grid_columnconfigure(0, weight=1)
        self._render()

    def _clear(self):
        for w in self.host.winfo_children():
            w.destroy()

    def _render(self):
        self._clear()
        s = self.current_section
        user = self.controller.logged_in_user or "User"
        if s == "My Applications":
            self.top_title.configure(text="Welcome Back!")
            self.top_sub.configure(text=f"Logged in as {user} — manage your business permit applications")
            self.top_action.configure(text="+  New Application", command=lambda: self._switch("New Application"))
            self._render_my_apps()
        elif s == "New Application":
            self.top_title.configure(text="New Business Permit Application")
            self.top_sub.configure(text="Fill out the form below accurately.")
            self.top_action.configure(text="Checklist", command=lambda: messagebox.showinfo("Checklist", "Prepare all required documents."))
            self._render_new_app()
        elif s == "Notifications":
            self.top_title.configure(text="Notifications")
            self.top_sub.configure(text="Stay updated on your application status")
            self.top_action.configure(text="⟳ Refresh", command=lambda: self._switch("Notifications"))
            self._render_notifications()
        elif s == "Track Application":
            app_id = self.tracking_app.get("id", "")
            self.top_title.configure(text=f"Track Application #{app_id}")
            self.top_sub.configure(text="Real-time status and AI risk assessment")
            self.top_action.configure(text="← Back to Applications", command=lambda: self._switch("My Applications"))
            self._render_track_app()

    def update_welcome(self):
        self._render()

    # ── Helper widgets ───────────────────────────────────────
    def _stat_card(self, parent, col, title, value, icon, icon_bg, val_color, subtitle=""):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.grid(row=0, column=col, sticky="nsew", padx=4, pady=2)
        top = ctk.CTkFrame(card, fg_color="white")
        top.pack(fill="x", padx=14, pady=(14, 2))
        ctk.CTkLabel(top, text=title, text_color="#6B7280",
                     font=ctk.CTkFont("Segoe UI", 10)).pack(side="left")
        ctk.CTkLabel(top, text=icon, fg_color=icon_bg, width=32, height=32,
                     corner_radius=8, font=ctk.CTkFont(size=14)).pack(side="right")
        ctk.CTkLabel(card, text=value, text_color=val_color,
                     font=ctk.CTkFont("Segoe UI", 24, "bold")).pack(anchor="w", padx=14)
        if subtitle:
            ctk.CTkLabel(card, text=subtitle, text_color="#9CA3AF",
                         font=ctk.CTkFont("Segoe UI", 9)).pack(anchor="w", padx=14, pady=(0, 12))

    # ── My Applications ──────────────────────────────────────
    def _render_my_apps(self):
        h = self.host
        user = self.controller.logged_in_user or ""
        apps = get_user_applications(user)
        permits = get_user_permits(user)
        notifs = get_notifications(user)
        pending = sum(1 for a in apps if a["status"] == "Pending")
        unread_n = sum(1 for n in notifs if not n["is_read"])

        # stat cards
        row = ctk.CTkFrame(h, fg_color="transparent")
        row.pack(fill="x", pady=(0, 10))
        for i in range(3):
            row.grid_columnconfigure(i, weight=1)
        self._stat_card(row, 0, "Total Applications", str(len(apps)), "📋", "#FFF4E5", "#F05A00")
        self._stat_card(row, 1, "Pending Review", str(pending), "⏳", "#FFF9E5", "#D9A100")
        self._stat_card(row, 2, "Notifications", str(unread_n), "🔔", "#FDECD0", "#F05A00")

        # applications list
        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(8, 12))
        ctk.CTkLabel(card, text="My Applications", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(anchor="w", padx=18, pady=(16, 8))

        if not apps:
            empty = ctk.CTkFrame(card, fg_color="white")
            empty.pack(fill="x", padx=18, pady=(0, 20))
            ctk.CTkLabel(empty, text="No applications yet", text_color="#111827",
                         font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(pady=(30, 4))
            ctk.CTkLabel(empty, text="Get started by creating your first application",
                         text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10)).pack()
            ctk.CTkButton(empty, text="Create Application",
                          command=lambda: self._switch("New Application"),
                          fg_color="#F05A00", hover_color="#D94B00", text_color="white",
                          font=ctk.CTkFont("Segoe UI", 10, "bold"),
                          height=34, corner_radius=6).pack(pady=12)
        else:
            hdr = ctk.CTkFrame(card, fg_color="#FAFAFA", corner_radius=0)
            hdr.pack(fill="x", padx=18)
            for col in ["ID", "Business Name", "Type", "Status", "Submitted", "Action"]:
                w = 60 if col == "ID" else 180 if col == "Business Name" else 120
                if col == "Action": w = 80
                ctk.CTkLabel(hdr, text=col, text_color="#374151",
                             font=ctk.CTkFont("Segoe UI", 10, "bold"),
                             width=w, anchor="w").pack(side="left", padx=4, pady=6)
            sc = {"Pending": "#D9A100", "Approved": "#2E7D32", "Rejected": "#E53E3E"}
            for a in apps:
                r = ctk.CTkFrame(card, fg_color="white")
                r.pack(fill="x", padx=18, pady=1)
                for val, color in [(str(a["id"]), "#374151"),
                                   (a["business_name"], "#111827"),
                                   (a.get("business_type") or "-", "#6B7280"),
                                   (a["status"], sc.get(a["status"], "#374151")),
                                   ((a["submitted_at"] or "")[:10], "#9CA3AF")]:
                    w = 60 if val == str(a["id"]) else 180 if val == a["business_name"] else 120
                    ctk.CTkLabel(r, text=val, text_color=color,
                                 font=ctk.CTkFont("Segoe UI", 10),
                                 width=w, anchor="w").pack(side="left", padx=4, pady=3)

                act_f = ctk.CTkFrame(r, fg_color="white", width=80)
                act_f.pack(side="left", padx=4, pady=3)
                act_f.pack_propagate(False)
                ctk.CTkButton(act_f, text="Track", width=70, height=24,
                              fg_color="#F3F4F6", hover_color="#E5E7EB", text_color="#F05A00",
                              font=ctk.CTkFont("Segoe UI", 10, "bold"),
                              command=lambda app_data=a: self._show_tracking(app_data)).pack(anchor="w")

        # permits section
        if permits:
            pcard = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                                 border_width=1, border_color="#E5E7EB")
            pcard.pack(fill="x", pady=(0, 12))
            ctk.CTkLabel(pcard, text=f"My Permits ({len(permits)})", text_color="#2E7D32",
                         font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(anchor="w", padx=18, pady=(16, 8))
            for p in permits:
                r = ctk.CTkFrame(pcard, fg_color="#E8F5E9", corner_radius=4)
                r.pack(fill="x", padx=18, pady=2)
                
                info_frame = ctk.CTkFrame(r, fg_color="transparent")
                info_frame.pack(side="left", padx=12, pady=8, fill="x", expand=True)
                
                ctk.CTkLabel(info_frame, text=f"✅  {p['permit_number']}  —  {p['business_name']}  |  Expires: {(p['expires_at'] or '')[:10]}",
                             text_color="#2E7D32", font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w")
                             
                ctk.CTkButton(r, text="🖨 Print Permit", width=100, height=26,
                              fg_color="#2E7D32", hover_color="#1B5E20", text_color="white",
                              font=ctk.CTkFont("Segoe UI", 10, "bold"),
                              command=lambda p_data=p: self._print_permit(p_data)).pack(side="right", padx=12)

    def _print_permit(self, permit_data):
        import os, tempfile, webbrowser
        from datetime import datetime
        
        try:
            date_str = permit_data.get('created_at', str(datetime.now()))[:10]
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = dt.strftime('%B %d, %Y')
        except:
            formatted_date = datetime.now().strftime('%B %d, %Y')

        owner_name = f"{permit_data.get('owner_first_name', '')} {permit_data.get('owner_last_name', '')}".strip()
        if not owner_name:
            owner_name = "___________________"

        html_content = f"""
        <html>
        <head>
            <title>Barangay Business Clearance - {permit_data.get('permit_number', '')}</title>
            <style>
                body {{ font-family: 'Arial', sans-serif; padding: 40px; color: #111827; }}
                .permit-box {{ padding: 20px 40px; max-width: 800px; margin: 0 auto; text-align: left; position: relative; }}
                .header {{ text-align: center; margin-bottom: 20px; line-height: 1.4; font-size: 14px; color: #374151; }}
                .header-title {{ font-weight: bold; font-size: 16px; color: #111827; }}
                .red-line {{ border-top: 3px solid #E53E3E; border-bottom: 1px solid #E53E3E; height: 2px; margin: 20px 0; }}
                .main-title {{ color: #E53E3E; text-transform: uppercase; text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 40px; letter-spacing: 2px; }}
                .content {{ font-size: 16px; line-height: 2; margin-bottom: 60px; text-align: justify; }}
                .content p {{ text-indent: 40px; margin-bottom: 15px; }}
                .footer-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 40px; }}
                .sig-box {{ text-align: center; }}
                .sig-line {{ border-top: 1px solid #111827; width: 80%; margin: 40px auto 5px auto; padding-top: 5px; }}
                .sig-name {{ font-weight: bold; font-size: 14px; text-transform: uppercase; }}
                .sig-title {{ font-size: 12px; color: #4b5563; }}
                .bottom-info {{ margin-top: 60px; display: grid; grid-template-columns: 1fr 1fr; font-size: 12px; color: #4b5563; }}
                .red-text {{ color: #E53E3E; font-weight: bold; text-transform: uppercase; }}
                @media print {{
                    body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
                }}
            </style>
        </head>
        <body onload="window.print()">
            <div class="permit-box">
                <div class="header">
                    REPUBLIC OF THE PHILIPPINES<br>
                    CITY OF CALOOCAN<br>
                    <span class="header-title">BARANGAY 183, ZONE 16, DISTRICT 1</span><br>
                    Office of the Punong Barangay
                </div>
                
                <div class="red-line"></div>
                
                <div class="main-title">BARANGAY BUSINESS CLEARANCE</div>
                
                <div class="content">
                    <b>TO WHOM IT MAY CONCERN:</b>
                    <br><br>
                    <p>This is to certify that the business establishment <b>{permit_data.get('business_name', '')}</b>, owned and operated by <b>{owner_name}</b>, with business address located at <b>{permit_data.get('business_address', '_____________________')}</b> has been granted this Barangay Business Clearance.</p>
                    
                    <p>This clearance is issued upon the request of the applicant for the purpose of securing a Business/Mayor's Permit and for whatever legal intent it may serve, provided that the business complies with all applicable laws and ordinances.</p>
                    
                    <p>The applicant has complied with the requirements of this barangay and has paid the necessary fees in accordance with the existing barangay revenue code.</p>
                    
                    <p>Issued this <b>{formatted_date}</b> at Barangay 183, Zone 16, Caloocan City.</p>
                </div>
                
                <div class="footer-grid">
                    <div class="sig-box">
                        <div style="text-align: left; font-size: 12px; color: #4b5563; padding-left: 10%;">Conforme / Signature of Applicant:</div>
                        <div class="sig-line"></div>
                        <div class="sig-name">{owner_name}</div>
                        <div class="sig-title">Applicant / Owner</div>
                    </div>
                    <div class="sig-box">
                        <div style="text-align: left; font-size: 12px; color: #4b5563; padding-left: 10%;">Approved By:</div>
                        <div class="sig-line"></div>
                        <div class="sig-name red-text">HON. MICHAEL RONALD PUNONGBAYAN</div>
                        <div class="sig-title">Punong Barangay</div>
                    </div>
                </div>
                
                <div class="bottom-info">
                    <div>
                        Clearance No: {permit_data.get('permit_number', '')}<br>
                        O.R. No: __________________<br>
                        Amount Paid: P 500.00
                    </div>
                    <div style="text-align: right;">
                        <span class="red-text">NOT VALID WITHOUT DRY SEAL</span><br>
                        Valid until: December 31, {datetime.now().year}
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        fd, path = tempfile.mkstemp(suffix=".html")
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        webbrowser.open('file://' + os.path.realpath(path))

    # ── New Application ──────────────────────────────────────
    def _render_new_app(self):
        h = self.host

        def field(parent, label, key):
            ctk.CTkLabel(parent, text=label, text_color="#111827",
                         font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w", pady=(8, 2))
            var = self.form_vars.get(key)
            if var is None:
                var = tk.StringVar()
                self.form_vars[key] = var
            ctk.CTkEntry(parent, textvariable=var, fg_color="#F3F4F6",
                         border_width=0, font=ctk.CTkFont("Segoe UI", 11),
                         height=36).pack(fill="x")

        def combo(parent, label, values, key):
            ctk.CTkLabel(parent, text=label, text_color="#111827",
                         font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w", pady=(8, 2))
            var = self.form_vars.get(key)
            if var is None:
                var = tk.StringVar(value=values[0] if values else "")
                self.form_vars[key] = var
            ctk.CTkComboBox(parent, variable=var, values=values,
                            height=36, fg_color="#F3F4F6",
                            border_width=0, dropdown_fg_color="white").pack(fill="x")

        def section_card(title):
            card = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                                border_width=1, border_color="#E5E7EB")
            card.pack(fill="x", pady=(0, 12))
            ctk.CTkLabel(card, text=title, text_color="#111827",
                         font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(
                anchor="w", padx=18, pady=(16, 4))
            inner = ctk.CTkFrame(card, fg_color="white")
            inner.pack(fill="x", padx=18, pady=(0, 16))
            return inner

        # Section 1: Business Info
        s1 = section_card("1. Business Information")
        combo(s1, "Ownership Type *", ["Select type", "Single Proprietorship", "Partnership", "Corporation"], "ownership_type")
        field(s1, "DTI/SEC/CDA Registration No. *", "registration_no")
        field(s1, "TIN Number *", "tin_number")
        field(s1, "Business / Commercial Name *", "business_name")
        field(s1, "Complete Business Address *", "business_address")

        # Section 2: Owner Info
        s2 = section_card("2. Owner / President Information")
        field(s2, "First Name *", "first_name")
        field(s2, "Last Name *", "last_name")
        combo(s2, "Gender *", ["Select gender", "Male", "Female"], "gender")
        field(s2, "Contact Number *", "contact_number")
        field(s2, "Email Address *", "email_address")

        # Section 3: Business Operation
        s3 = section_card("3. Business Operation")
        field(s3, "No. of Male Employees *", "male_employees")
        field(s3, "No. of Female Employees *", "female_employees")
        field(s3, "Capital / Asset (Php) *", "capital_asset")
        combo(s3, "Line of Business *", ["Select line of business", "Food", "Retail", "Services", "Manufacturing", "Other"], "line_of_business")

        # Section 4: Documents
        s4 = section_card("Required Documents")
        docs = ["DTI / SEC / CDA Registration", "Fire Safety Inspection Certificate",
                "Affidavit of Undertaking", "Business Permit Application Form (Signed)",
                "Locational Clearance", "Sketch / Location Plan"]
        for doc in docs:
            row = ctk.CTkFrame(s4, fg_color="white")
            row.pack(fill="x", pady=2)
            status = "✓ Uploaded" if doc in self.uploaded_documents else "No file"
            ctk.CTkLabel(row, text=doc, text_color="#374151",
                         font=ctk.CTkFont("Segoe UI", 10)).pack(side="left")
            ctk.CTkButton(row, text=status if doc in self.uploaded_documents else "Upload",
                          width=80, height=26, corner_radius=4,
                          fg_color="#E8F5E9" if doc in self.uploaded_documents else "#F3F4F6",
                          hover_color="#EDEDED",
                          text_color="#2E7D32" if doc in self.uploaded_documents else "#6B7280",
                          font=ctk.CTkFont("Segoe UI", 9),
                          command=lambda d=doc: self._upload_doc(d)).pack(side="right")

        # Actions
        acts = ctk.CTkFrame(h, fg_color="transparent")
        acts.pack(fill="x", pady=(4, 20))
        ctk.CTkButton(acts, text="Submit Application", command=self._submit_application,
                      fg_color="#F05A00", hover_color="#D94B00", text_color="white",
                      font=ctk.CTkFont("Segoe UI", 11, "bold"),
                      height=40, corner_radius=6).pack(side="right")
        ctk.CTkButton(acts, text="Cancel", command=lambda: self._switch("My Applications"),
                      fg_color="white", hover_color="#EDEDED", text_color="#111827",
                      border_width=1, border_color="#D0D5DD",
                      font=ctk.CTkFont("Segoe UI", 10),
                      height=38, corner_radius=6).pack(side="right", padx=8)

    def _upload_doc(self, doc_name):
        path = filedialog.askopenfilename(title=f"Upload: {doc_name}")
        if not path:
            return
        try:
            size = os.path.getsize(path)
        except OSError:
            messagebox.showerror("Error", "Cannot read file.")
            return
        current = sum(d["size"] for d in self.uploaded_documents.values())
        prev = self.uploaded_documents.get(doc_name, {}).get("size", 0)
        if current - prev + size > self.max_upload_bytes:
            messagebox.showwarning("Limit", "Total uploads cannot exceed 500 MB.")
            return
        self.uploaded_documents[doc_name] = {"path": path, "size": size}
        self._render()

    def _submit_application(self):
        bname = self.form_vars.get("business_name")
        bname_val = bname.get().strip() if bname else ""
        if not bname_val:
            messagebox.showwarning("Missing", "Please enter a Business Name.")
            return

        user = self.controller.logged_in_user or ""

        def val(key):
            v = self.form_vars.get(key)
            return v.get().strip() if v else ""

        submit_application(
            user_email=user,
            business_name=bname_val,
            business_type=val("line_of_business"),
            ownership_type=val("ownership_type"),
            business_address=val("business_address"),
            capital_investment=val("capital_asset"),
            employees_male=val("male_employees"),
            employees_female=val("female_employees"),
            owner_first_name=val("first_name"),
            owner_last_name=val("last_name"),
            contact_number=val("contact_number"),
            email=val("email_address"),
            tin_number=val("tin_number"),
            dti_sec_cda_reg_no=val("registration_no"),
            gender=val("gender")
        )

        messagebox.showinfo("Submitted", "Your application has been submitted successfully!")
        self.form_vars.clear()
        self.uploaded_documents.clear()
        self._switch("My Applications")

    # ── Notifications ────────────────────────────────────────
    def _render_notifications(self):
        h = self.host
        user = self.controller.logged_in_user or ""
        notifs = get_notifications(user)
        total = len(notifs)
        unread = sum(1 for n in notifs if not n["is_read"])
        read_ = total - unread

        row = ctk.CTkFrame(h, fg_color="transparent")
        row.pack(fill="x", pady=(0, 10))
        for i in range(3):
            row.grid_columnconfigure(i, weight=1)
        self._stat_card(row, 0, "Total Notifications", str(total), "🔔", "#FDECD0", "#111827")
        self._stat_card(row, 1, "Unread", str(unread), "🔔", "#FDE8E8", "#E53E3E")
        self._stat_card(row, 2, "Read", str(read_), "✓", "#EBF5FF", "#111827")

        acts = ctk.CTkFrame(h, fg_color="transparent")
        acts.pack(anchor="w", pady=(0, 10))
        ctk.CTkButton(acts, text="Mark All as Read", fg_color="white",
                      hover_color="#EDEDED", text_color="#374151",
                      border_width=1, border_color="#D0D5DD",
                      font=ctk.CTkFont("Segoe UI", 10), height=32, corner_radius=6,
                      command=self._mark_read).pack(side="left", padx=(0, 8))
        ctk.CTkButton(acts, text="🗑  Clear All", fg_color="white",
                      hover_color="#FDE8E8", text_color="#E53E3E",
                      border_width=1, border_color="#D0D5DD",
                      font=ctk.CTkFont("Segoe UI", 10), height=32, corner_radius=6,
                      command=self._clear_notifs).pack(side="left")

        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x")
        ctk.CTkLabel(card, text="All Notifications", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(anchor="w", padx=18, pady=(16, 8))
        if not notifs:
            ctk.CTkLabel(card, text="🔔", text_color="#C4C9D4",
                         font=ctk.CTkFont(size=42)).pack(pady=(30, 6))
            ctk.CTkLabel(card, text="No notifications yet", text_color="#9CA3AF",
                         font=ctk.CTkFont("Segoe UI", 12)).pack(pady=(0, 40))
        else:
            for n in notifs:
                bg = "#FFF9F0" if not n["is_read"] else "white"
                r = ctk.CTkFrame(card, fg_color=bg, corner_radius=4)
                r.pack(fill="x", padx=16, pady=2)
                dot = "#F05A00" if not n["is_read"] else "#C4C9D4"
                ctk.CTkLabel(r, text="●", text_color=dot,
                             font=ctk.CTkFont(size=8)).pack(side="left", padx=(8, 6))
                tf = ctk.CTkFrame(r, fg_color=bg)
                tf.pack(side="left", fill="x", expand=True, pady=6)
                ctk.CTkLabel(tf, text=n.get("title", ""), text_color="#111827",
                             font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w")
                ctk.CTkLabel(tf, text=n.get("message", ""), text_color="#6B7280",
                             font=ctk.CTkFont("Segoe UI", 9)).pack(anchor="w")
                ctk.CTkLabel(r, text=n.get("created_at", "")[:16], text_color="#9CA3AF",
                             font=ctk.CTkFont("Segoe UI", 8)).pack(side="right", padx=8)

    def _mark_read(self):
        user = self.controller.logged_in_user or ""
        mark_all_notifications_read(user)
        self._render()

    def _clear_notifs(self):
        user = self.controller.logged_in_user or ""
        clear_all_notifications(user)
        self._render()

    # ── Application Tracking ─────────────────────────────────
    def _show_tracking(self, app_data):
        self.current_section = "Track Application"
        self.tracking_app = app_data
        for t, b in self.nav_buttons.items():
            b.configure(fg_color="transparent", text_color="#111827", font=ctk.CTkFont("Segoe UI", 11))
        self._render()

    def _render_track_app(self):
        h = self.host
        app = self.tracking_app

        # Details Header
        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(card, text=app.get("business_name", "Unknown Business"), text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 16, "bold")).pack(anchor="w", padx=18, pady=(16, 2))
        ctk.CTkLabel(card, text=f"Type: {app.get('business_type', '-')} | Ownership: {app.get('ownership_type', '-')}",
                     text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 11)).pack(anchor="w", padx=18, pady=(0, 16))

        # Timeline
        tl = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        tl.pack(fill="both", expand=True)
        ctk.CTkLabel(tl, text="Application Timeline", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(16, 12))

        def add_step(title, desc, time_str, is_done, is_current=False, color="#F05A00"):
            row = ctk.CTkFrame(tl, fg_color="white")
            row.pack(fill="x", padx=24, pady=0)

            icon_c = color if is_done else "#E5E7EB"
            icon_text = "✓" if is_done else "○"
            if is_current: icon_text = "●"

            icon_f = ctk.CTkFrame(row, fg_color="white", width=30)
            icon_f.pack(side="left", fill="y")
            ctk.CTkLabel(icon_f, text=icon_text, text_color=icon_c, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(4,0))

            content_f = ctk.CTkFrame(row, fg_color="white")
            content_f.pack(side="left", fill="x", expand=True, padx=(10, 0), pady=(0, 16))

            title_color = "#111827" if is_done or is_current else "#9CA3AF"
            desc_color = "#6B7280" if is_done or is_current else "#D1D5DB"

            ctk.CTkLabel(content_f, text=title, text_color=title_color, font=ctk.CTkFont("Segoe UI", 11, "bold")).pack(anchor="w")
            if desc:
                ctk.CTkLabel(content_f, text=desc, text_color=desc_color, font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w")
            if time_str:
                ctk.CTkLabel(content_f, text=time_str, text_color="#9CA3AF", font=ctk.CTkFont("Segoe UI", 9)).pack(anchor="w", pady=(2,0))

        status = app.get("status", "Pending")
        sub_time = app.get("submitted_at", "")
        rev_time = app.get("reviewed_at", "")
        rev_by = app.get("reviewed_by", "")
        notes = app.get("notes", "")
        risk = app.get("risk_level", "Low")

        # Step 1: Submitted
        add_step("Application Submitted", "Documents and forms uploaded successfully.", sub_time, True)

        # Step 2: ML Assessment
        ml_desc = f"AI Risk Assessment: {risk} Risk. Passed initial automated checks."
        add_step("Machine Learning Assessment", ml_desc, sub_time, True)

        # Step 3: Under Review
        is_rev = status in ["Approved", "Rejected"]
        rev_desc = f"Reviewed by {rev_by}" if is_rev else "Barangay officials are currently reviewing your documents."
        add_step("Barangay Review", rev_desc, rev_time if is_rev else "In Progress", is_rev, is_current=(status=="Pending"))

        # Step 4: Final Decision
        dec_color = "#2E7D32" if status == "Approved" else "#E53E3E"
        dec_title = "Permit Approved" if status == "Approved" else "Application Rejected" if status == "Rejected" else "Final Decision"
        dec_desc = f"Remarks: {notes}" if notes else ""
        add_step(dec_title, dec_desc, rev_time, is_rev, color=dec_color)
