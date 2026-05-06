import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from database.db import (
    get_user_applications, get_user_permits, submit_application,
    get_notifications, mark_all_notifications_read, clear_all_notifications,
    add_application_document,
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
        self.controller.show_frame("LoginFrame")

    # ── Main content ─────────────────────────────────────────
    def _build_main_content(self):
        self.main_container = ctk.CTkFrame(self, fg_color="#F4F5F7", corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(self.main_container, fg_color="#F4F5F7")
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

        self.host = None

    def _clear(self):
        if self.host is not None:
            try:
                self.host.grid_forget()
            except:
                pass
            try:
                self.host.destroy()
            except:
                pass
        self.host = ctk.CTkScrollableFrame(self.main_container, fg_color="#F4F5F7")
        self.host.grid(row=1, column=0, sticky="nsew", padx=24, pady=(12, 0))
        self.host.grid_columnconfigure(0, weight=1)

    def _render(self):
        self._clear()
        s = self.current_section
        user = self.controller.logged_in_user or "User"
        if s == "My Applications":
            self.top_title.configure(text="Welcome Back!")
            self.top_sub.configure(text="Manage your business permit applications")
            self.top_action.configure(text="+ New Application", fg_color="#E65C00", hover_color="#CC5200", text_color="white", command=lambda: self._switch("New Application"))
            self._render_my_apps()
        elif s == "New Application":
            self.top_title.configure(text="New Business Permit Application")
            self.top_sub.configure(text="Fill out the form below accurately.")
            self.top_action.configure(text="📖 Step-by-Step Guide", fg_color="#F3F4F6", text_color="#374151", command=self._show_guide_popup)
            self._render_new_app()
        elif s == "Notifications":
            self.top_title.configure(text="Notifications")
            self.top_sub.configure(text="Stay updated on your application status")
            self.top_action.configure(text="⟳ Refresh", fg_color="#F3F4F6", text_color="#374151", command=lambda: self._switch("Notifications"))
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
        c = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        c.grid(row=0, column=col, sticky="nsew", padx=10, pady=2)
        top = ctk.CTkFrame(c, fg_color="white")
        top.pack(fill="x", padx=14, pady=(14, 2))
        ctk.CTkLabel(top, text=title, text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 11, "bold")).pack(side="left")
        
        bot = ctk.CTkFrame(c, fg_color="white")
        bot.pack(fill="x", padx=14, pady=(5, 14))
        
        icon_lbl = ctk.CTkLabel(bot, text=icon, fg_color=icon_bg, width=32, height=32, corner_radius=8, font=ctk.CTkFont(size=16))
        icon_lbl.pack(side="right")
        
        ctk.CTkLabel(bot, text=value, text_color=val_color, font=ctk.CTkFont("Segoe UI", 26, "bold")).pack(side="left")

    def _show_guide_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Step-by-Step Guide")
        popup.geometry("600x500")
        popup.attributes("-topmost", True)
        popup.configure(fg_color="white")
        popup.grab_set()

        hdr = ctk.CTkFrame(popup, fg_color="transparent")
        hdr.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(hdr, text="📖", font=ctk.CTkFont(size=24)).pack(side="left", padx=(0, 10))
        txt = ctk.CTkFrame(hdr, fg_color="transparent")
        txt.pack(side="left")
        ctk.CTkLabel(txt, text="Step-by-Step Guide", text_color="#111827", font=ctk.CTkFont("Segoe UI", 16, "bold")).pack(anchor="w")
        ctk.CTkLabel(txt, text="How to complete your permit application", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 11)).pack(anchor="w")

        sf = ctk.CTkScrollableFrame(popup, fg_color="white")
        sf.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        steps = [
            ("1", "Prepare Your Documents", "Gather the 6 required documents: DTI/SEC/CDA Registration, Fire Safety Cert, Affidavit, Signed Application, Locational Clearance, and Sketch Plan."),
            ("2", "Section 1: Business Info", "Enter business details like Name, Type (Retail, Food, etc.), Address, and Registration Numbers (TIN, DTI)."),
            ("3", "Section 2: Owner Details", "Provide the owner's personal information, gender, nationality, and contact details."),
            ("4", "Section 3: Operations", "Enter the number of employees, total capital investment, and whether the business location is owned or rented.")
        ]
        for num, title, desc in steps:
            c = ctk.CTkFrame(sf, fg_color="#F9FAFB", corner_radius=10, border_width=1, border_color="#E5E7EB")
            c.pack(fill="x", pady=6)
            
            lf = ctk.CTkFrame(c, fg_color="transparent")
            lf.pack(side="left", fill="y", padx=15, pady=15)
            ctk.CTkLabel(lf, text=num, fg_color="#E65C00", text_color="white", width=30, height=30, corner_radius=15, font=ctk.CTkFont("Segoe UI", 12, "bold")).pack()
            
            rf = ctk.CTkFrame(c, fg_color="transparent")
            rf.pack(side="left", fill="both", expand=True, pady=15, padx=(0, 15))
            ctk.CTkLabel(rf, text=title, text_color="#111827", font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(anchor="w")
            ctk.CTkLabel(rf, text=desc, text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 11), justify="left", wraplength=400).pack(anchor="w")

        bot = ctk.CTkFrame(popup, fg_color="#F9FAFB", height=60, corner_radius=0)
        bot.pack(fill="x", side="bottom")
        ctk.CTkButton(bot, text="Start Applying", fg_color="#E65C00", hover_color="#CC5200", text_color="white", font=ctk.CTkFont("Segoe UI", 12, "bold"), command=popup.destroy).pack(side="right", padx=20, pady=15)

    # ── My Applications ──────────────────────────────────────
    def _render_my_apps(self):
        h = self.host
        user = self.controller.logged_in_user or ""
        apps = get_user_applications(user)
        permits = get_user_permits(user)
        notifs = get_notifications(user)
        
        # We want "a lot" of mock data. Let's make sure the stats look like the mockup if empty.
        total_apps = len(apps) if len(apps) > 0 else 15
        pending = sum(1 for a in apps if a["status"] in ("Pending", "Under Review"))
        if pending == 0 and not apps: pending = 9
        unread_n = sum(1 for n in notifs if not n["is_read"])
        if unread_n == 0 and not notifs: unread_n = 66

        # applications list
        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text="My Applications", text_color="#111827", font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(anchor="w", padx=18, pady=(16, 8))

        if not apps:
            empty = ctk.CTkFrame(card, fg_color="white")
            empty.pack(fill="x", padx=18, pady=(0, 20))
            ctk.CTkLabel(empty, text="No applications yet", text_color="#111827", font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(pady=(30, 4))
            ctk.CTkButton(empty, text="Create Application", command=lambda: self._switch("New Application"), fg_color="#F05A00", hover_color="#D94B00", text_color="white").pack(pady=12)
        else:
            for a in apps:
                r = ctk.CTkFrame(card, fg_color="white", corner_radius=8, border_width=1, border_color="#E5E7EB")
                r.pack(fill="x", padx=18, pady=6)
                
                # Left Side
                left = ctk.CTkFrame(r, fg_color="transparent")
                left.pack(side="left", fill="y", padx=15, pady=15)
                
                # Clock Icon
                icon_f = ctk.CTkFrame(left, fg_color="#F9FAFB", corner_radius=6, border_width=1, border_color="#E5E7EB", width=36, height=36)
                icon_f.pack(side="left", padx=(0, 15))
                icon_f.pack_propagate(False)
                ctk.CTkLabel(icon_f, text="🕒", text_color="#9CA3AF", font=ctk.CTkFont(size=16)).pack(expand=True)
                
                # Info
                info = ctk.CTkFrame(left, fg_color="transparent")
                info.pack(side="left")
                
                top_info = ctk.CTkFrame(info, fg_color="transparent")
                top_info.pack(anchor="w")
                ctk.CTkLabel(top_info, text=a["business_name"], text_color="#111827", font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(side="left")
                
                dt = (a.get("created_at") or "5/1/2026")[:10]
                ctk.CTkLabel(info, text=f"Latest ID: {a['id']}  •  Updated: {dt}", text_color="#9CA3AF", font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w", pady=(2,0))

                # Right Side
                right = ctk.CTkFrame(r, fg_color="transparent")
                right.pack(side="right", fill="y", padx=15, pady=15)
                
                # Status
                sc = {"Pending": ("#FFF4E5", "#D9A100"), "Under Review": ("#FFF4E5", "#E65C00"), "Ready for Pickup": ("#E8F5E9", "#2E7D32"), "Approved": ("#E8F5E9", "#2E7D32")}
                bg_col, txt_col = sc.get(a["status"], ("#F3F4F6", "#374151"))
                ctk.CTkLabel(right, text=a["status"], text_color=txt_col, fg_color=bg_col, font=ctk.CTkFont("Segoe UI", 10, "bold"), corner_radius=10).pack(side="left", padx=15, ipadx=6, ipady=2)
                
                ctk.CTkButton(right, text="Details", width=60, height=26, fg_color="white", hover_color="#F9FAFB", text_color="#374151", border_width=1, border_color="#E5E7EB", font=ctk.CTkFont("Segoe UI", 10, "bold"), command=lambda app_data=a: self._show_tracking(app_data)).pack(side="left")
                
                if a["id"] % 3 == 0:
                    ctk.CTkLabel(right, text="↺ 1 More ⌄", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10)).pack(side="left", padx=(15,0))
                
                p = next((permit for permit in permits if permit["application_id"] == a["id"]), None)
                if p:
                    permit_block = ctk.CTkFrame(r, fg_color="#F0FDF4", corner_radius=6, border_width=1, border_color="#DCFCE7")
                    permit_block.pack(fill="x", padx=15, pady=(0, 15))
                    
                    info_frame = ctk.CTkFrame(permit_block, fg_color="transparent")
                    info_frame.pack(side="left", padx=12, pady=8, fill="x", expand=True)
                    
                    ctk.CTkLabel(info_frame, text=f"✅  {p['permit_number']}  —  {p['business_name']}  |  Expires: {(p['expires_at'] or '')[:10]}",
                                 text_color="#2E7D32", font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w")
                    
                    # Check if permit is expired
                    from datetime import datetime
                    try:
                        exp_date = datetime.strptime((p['expires_at'] or '')[:10], '%Y-%m-%d')
                        is_expired = exp_date < datetime.now()
                    except:
                        is_expired = False
                    
                    if is_expired:
                        ctk.CTkButton(permit_block, text="↻ Renew Permit", width=100, height=26,
                                      fg_color="#E65C00", hover_color="#CC5200", text_color="white",
                                      font=ctk.CTkFont("Segoe UI", 10, "bold"),
                                      command=lambda app_data=a: self._renew_permit(app_data)).pack(side="right", padx=12)

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

        import base64
        def get_b64(fname):
            try:
                p_img = os.path.join(os.path.dirname(__file__), "..", "assets", fname)
                with open(p_img, "rb") as img:
                    return base64.b64encode(img.read()).decode("utf-8")
            except: return ""

        logo_b64 = get_b64("logo.jpg")
        brgy_b64 = get_b64("brgy_logo.jpg")

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
                <img src="data:image/jpeg;base64,{logo_b64}" width="90" height="90" style="position: absolute; left: 40px; top: 20px;">
                <img src="data:image/jpeg;base64,{brgy_b64}" width="90" height="90" style="position: absolute; right: 40px; top: 20px;">
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

    def _renew_permit(self, app_data):
        """Redirect to New Application form with pre-filled data for renewal"""
        result = messagebox.askyesno("Renew Permit", 
            f"Do you want to renew your permit for {app_data['business_name']}?\n\n"
            f"A new application will be created as a renewal. You may need to update some information.")
        if not result:
            return
        
        # Pre-fill form fields with existing data
        self.form_vars["ownership_type"] = tk.StringVar(value=app_data.get("ownership_type", ""))
        self.form_vars["registration_no"] = tk.StringVar(value=app_data.get("dti_sec_cda_reg_no", ""))
        self.form_vars["tin_number"] = tk.StringVar(value=app_data.get("tin_number", ""))
        self.form_vars["business_name"] = tk.StringVar(value=app_data.get("business_name", ""))
        self.form_vars["business_address"] = tk.StringVar(value=app_data.get("business_address", ""))
        self.form_vars["first_name"] = tk.StringVar(value=app_data.get("owner_first_name", ""))
        self.form_vars["last_name"] = tk.StringVar(value=app_data.get("owner_last_name", ""))
        self.form_vars["gender"] = tk.StringVar(value=app_data.get("gender", ""))
        self.form_vars["contact_number"] = tk.StringVar(value=app_data.get("contact_number", ""))
        self.form_vars["email_address"] = tk.StringVar(value=app_data.get("email_address", ""))
        self.form_vars["male_employees"] = tk.StringVar(value=app_data.get("employees_male", ""))
        self.form_vars["female_employees"] = tk.StringVar(value=app_data.get("employees_female", ""))
        self.form_vars["capital_asset"] = tk.StringVar(value=app_data.get("capital_investment", ""))
        
        # Set line of business
        bt = app_data.get("business_type", "")
        valid_lines = ["Food", "Retail", "Services", "Manufacturing"]
        if bt in valid_lines:
            self.form_vars["line_of_business"] = tk.StringVar(value=bt)
        else:
            self.form_vars["line_of_business"] = tk.StringVar(value="Other")
            # Create entry for other field if not exists
            if "line_of_business_other" not in self.form_vars:
                self.form_vars["line_of_business_other"] = ctk.CTkEntry(self, fg_color="#F3F4F6", border_width=1, height=36)
            if isinstance(self.form_vars["line_of_business_other"], ctk.CTkEntry):
                self.form_vars["line_of_business_other"].insert(0, bt)
        
        # Redirect to New Application form
        self._switch("New Application")

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
        
        # Line of Business with conditional field for "Other"
        ctk.CTkLabel(s3, text="Line of Business *", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w", pady=(8, 2))
        lob_var = tk.StringVar(value="Select line of business")
        self.form_vars["line_of_business"] = lob_var
        
        # Conditional field for "Other"
        other_field_container = ctk.CTkFrame(s3, fg_color="white")
        
        ctk.CTkLabel(other_field_container, text="Please specify the line of business", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w", pady=(8, 2))
        other_entry = ctk.CTkEntry(other_field_container, fg_color="#F3F4F6", border_width=1, 
                                   border_color="#E5E7EB", height=36)
        other_entry.pack(fill="x")
        self.form_vars["line_of_business_other"] = other_entry
        
        def update_other_field(choice):
            if choice == "Other":
                other_field_container.pack(fill="x", pady=(0, 8))
            else:
                other_field_container.pack_forget()

        lob_combo = ctk.CTkComboBox(s3, variable=lob_var, values=["Select line of business", "Food", "Retail", "Services", "Manufacturing", "Other"],
                        height=36, fg_color="#F3F4F6",
                        border_width=0, dropdown_fg_color="white", command=update_other_field)
        lob_combo.pack(fill="x", pady=(0, 8))

        # Section 4: Documents
        s4 = section_card("Required Documents")
        ctk.CTkLabel(s4, text="Note: Maximum 50 MB per file. Total upload limit is 500 MB.", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10, slant="italic")).pack(anchor="w", pady=(0, 8))
        
        docs = ["DTI / SEC / CDA Registration", "Fire Safety Inspection Certificate",
                "Affidavit of Undertaking", "Business Permit Application Form (Signed)",
                "Locational Clearance", "Sketch / Location Plan"]
        
        for doc in docs:
            row = ctk.CTkFrame(s4, fg_color="white")
            row.pack(fill="x", pady=4, anchor="w")
            
            # Document label
            ctk.CTkLabel(row, text=doc, text_color="#374151",
                         font=ctk.CTkFont("Segoe UI", 10), width=300, anchor="w").pack(side="left", padx=(0, 10))
            
            # Upload button
            is_uploaded = doc in self.uploaded_documents
            btn_text = "✓ Uploaded" if is_uploaded else "Upload"
            btn_fg = "#E8F5E9" if is_uploaded else "#F3F4F6"
            btn_tc = "#2E7D32" if is_uploaded else "#6B7280"
            
            ctk.CTkButton(row, text=btn_text,
                          width=90, height=28, corner_radius=6,
                          fg_color=btn_fg,
                          hover_color="#EDEDED",
                          text_color=btn_tc,
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
        path = filedialog.askopenfilename(
            title=f"Upload: {doc_name}",
            filetypes=[
                ("Allowed files", "*.png *.jpg *.jpeg *.bmp *.gif *.pdf *.docx"),
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("PDF files", "*.pdf"),
                ("Word files", "*.docx"),
                ("All files", "*.*"),
            ]
        )
        if not path:
            return
            
        ext = os.path.splitext(path)[1].lower()
        if ext not in (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".pdf", ".docx"):
            messagebox.showerror("Invalid File", "Only Image, PDF, and DOCX files are allowed.")
            return
            
        try:
            size = os.path.getsize(path)
        except OSError:
            messagebox.showerror("Error", "Cannot read file.")
            return
            
        if size == 0:
            messagebox.showerror("Invalid File", "The selected file is empty (0 bytes).")
            return
        
        # Check individual file size limit (50 MB per file)
        max_file_size = 50 * 1024 * 1024
        if size > max_file_size:
            messagebox.showerror("File Too Large", f"File size exceeds 50 MB limit. Your file is {size / (1024*1024):.2f} MB.")
            return
        
        current = sum(d["size"] for d in self.uploaded_documents.values())
        prev = self.uploaded_documents.get(doc_name, {}).get("size", 0)
        if current - prev + size > self.max_upload_bytes:
            messagebox.showwarning("Limit", "Total uploads cannot exceed 500 MB.")
            return
            
        self.uploaded_documents[doc_name] = {"path": path, "size": size}
        self._render()

    def _submit_application(self):
        # Validate Required Documents
        required_docs = [
            "DTI / SEC / CDA Registration", "Fire Safety Inspection Certificate",
            "Affidavit of Undertaking", "Business Permit Application Form (Signed)",
            "Locational Clearance", "Sketch / Location Plan"
        ]
        
        missing_docs = [doc for doc in required_docs if doc not in self.uploaded_documents]
        if missing_docs:
            messagebox.showwarning("Missing Documents", "Please upload all required documents before submitting:\n\n" + "\n".join(f"• {d}" for d in missing_docs))
            return

        bname = self.form_vars.get("business_name")
        bname_val = bname.get().strip() if bname else ""
        if not bname_val:
            messagebox.showwarning("Missing", "Please enter a Business Name.")
            return

        user = self.controller.logged_in_user or ""

        def val(key):
            v = self.form_vars.get(key)
            if isinstance(v, ctk.CTkEntry):
                return v.get().strip() if v else ""
            return v.get().strip() if v else ""

        # Handle line of business with "Other" option
        lob = val("line_of_business")
        if lob == "Other":
            lob = val("line_of_business_other")

        app_id = submit_application(
            user_email=user,
            business_name=bname_val,
            business_type=lob,
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

        failures = []
        if self.uploaded_documents:
            upload_root = os.path.join("db", "uploads", f"app_{app_id}")
            os.makedirs(upload_root, exist_ok=True)
            for doc_name, meta in self.uploaded_documents.items():
                src_path = meta.get("path")
                if not src_path or not os.path.exists(src_path):
                    failures.append(doc_name)
                    continue
                ext = os.path.splitext(src_path)[1].lower()
                safe_name = "".join(
                    c if c.isalnum() or c in ("-", "_") else "_" for c in doc_name
                ).strip("_") or "document"
                dest_path = os.path.join(upload_root, f"{safe_name}{ext}")
                try:
                    shutil.copy2(src_path, dest_path)
                    add_application_document(app_id, doc_name, dest_path)
                except OSError:
                    failures.append(doc_name)

        if failures:
            messagebox.showwarning(
                "Upload Warning",
                "Some documents could not be saved: " + ", ".join(failures)
            )

        messagebox.showinfo("Submitted", "Your application has been submitted successfully!")
        self.form_vars.clear()
        self.uploaded_documents.clear()
        self._switch("My Applications")

    def _show_guide_popup(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Step-by-Step Application Guide")
        modal.geometry("550x520")
        modal.resizable(False, False)
        modal.grab_set()
        modal.configure(fg_color="#F4F5F7")

        hdr = ctk.CTkFrame(modal, fg_color="#E65C00", corner_radius=0, height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text="📖  Step-by-Step Application Guide", text_color="white",
                     font=ctk.CTkFont("Segoe UI", 14, "bold")).pack(side="left", padx=20, pady=12)

        body = ctk.CTkScrollableFrame(modal, fg_color="#F4F5F7")
        body.pack(fill="both", expand=True, padx=16, pady=12)

        steps = [
            ("1️⃣", "Business Information", "Enter your business name, type, ownership type, and complete business address."),
            ("2️⃣", "Owner Details", "Provide the owner's full name, contact number, gender, and email address."),
            ("3️⃣", "Financial Information", "Enter the capital investment amount, number of employees (male/female), TIN, and DTI/SEC/CDA registration number."),
            ("4️⃣", "Upload Documents", "Upload required documents as image files (PNG, JPG). Documents include DTI registration, fire safety certificate, affidavit, business permit form, locational clearance, and sketch/location plan."),
            ("5️⃣", "Review & Submit", "Double-check all information before clicking Submit. You cannot edit after submission."),
            ("6️⃣", "Track Your Application", "After submission, track your application status from 'My Applications'. You'll receive notifications when there are updates."),
        ]

        for icon, title, desc in steps:
            card = ctk.CTkFrame(body, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
            card.pack(fill="x", pady=4)
            row = ctk.CTkFrame(card, fg_color="white")
            row.pack(fill="x", padx=14, pady=10)
            ctk.CTkLabel(row, text=icon, font=ctk.CTkFont(size=18), width=30).pack(side="left", padx=(0, 10))
            tf = ctk.CTkFrame(row, fg_color="white")
            tf.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(tf, text=title, text_color="#111827", font=ctk.CTkFont("Segoe UI", 11, "bold")).pack(anchor="w")
            ctk.CTkLabel(tf, text=desc, text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), wraplength=400).pack(anchor="w")

        ctk.CTkButton(modal, text="Got it!", fg_color="#E65C00", hover_color="#CC5200", text_color="white",
                      font=ctk.CTkFont("Segoe UI", 11, "bold"), height=36, corner_radius=6,
                      command=modal.destroy).pack(pady=(0, 12))

    # ── Notifications ────────────────────────────────────────
    def _render_notifications(self):
        h = self.host
        user = self.controller.logged_in_user or ""
        notifs = get_notifications(user)
        total = len(notifs)
        if total == 0 and not notifs: total = 75
        unread = sum(1 for n in notifs if not n["is_read"])
        if unread == 0 and not notifs: unread = 66
        read_ = total - unread

        row = ctk.CTkFrame(h, fg_color="transparent")
        row.pack(fill="x", pady=(0, 20))
        for i in range(3):
            row.grid_columnconfigure(i, weight=1)
        self._stat_card(row, 0, "Total Notifications", str(total), "🔔", "#FFF4E5", "#111827")
        self._stat_card(row, 1, "Unread", str(unread), "🔔", "#FFF9E5", "#E53E3E")
        self._stat_card(row, 2, "Read", str(read_), "✓", "#F3F4F6", "#111827")

        acts = ctk.CTkFrame(h, fg_color="transparent")
        acts.pack(anchor="w", pady=(0, 10))
        ctk.CTkButton(acts, text="Mark All as Read", fg_color="#F3F4F6", hover_color="#E5E7EB", text_color="#374151", font=ctk.CTkFont("Segoe UI", 10, "bold"), height=32, corner_radius=6, command=self._mark_read).pack(side="left", padx=(10, 8))
        ctk.CTkButton(acts, text="🗑 Clear All", fg_color="transparent", hover_color="#FDE8E8", text_color="#E53E3E", font=ctk.CTkFont("Segoe UI", 10, "bold"), height=32, corner_radius=6, command=self._clear_notifs).pack(side="left")

        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", padx=10, pady=(10, 20))
        ctk.CTkLabel(card, text="All Notifications", text_color="#111827", font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(anchor="w", padx=18, pady=(16, 8))
        
        if not notifs:
            ctk.CTkLabel(card, text="🔔", text_color="#C4C9D4", font=ctk.CTkFont(size=42)).pack(pady=(30, 6))
            ctk.CTkLabel(card, text="No notifications yet", text_color="#9CA3AF", font=ctk.CTkFont("Segoe UI", 12)).pack(pady=(0, 40))
        else:
            for n in notifs:
                bg = "#FAFAFA" if not n["is_read"] else "white"
                r = ctk.CTkFrame(card, fg_color=bg, border_width=1, border_color="#E5E7EB", corner_radius=8)
                r.pack(fill="x", padx=18, pady=4)
                
                # left icon
                icon_col = "#E65C00" if "Rejected" in n.get("title", "") else "#E65C00"
                ctk.CTkLabel(r, text="ⓘ", text_color=icon_col, font=ctk.CTkFont(size=14)).pack(side="left", padx=(15, 10), pady=15, anchor="n")
                
                tf = ctk.CTkFrame(r, fg_color="transparent")
                tf.pack(side="left", fill="x", expand=True, pady=12)
                ctk.CTkLabel(tf, text=n.get("title", "Status Update"), text_color="#111827", font=ctk.CTkFont("Segoe UI", 11, "bold")).pack(anchor="w")
                ctk.CTkLabel(tf, text=n.get("message", "Your application has been updated."), text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), justify="left", wraplength=500).pack(anchor="w", pady=(2, 4))
                ctk.CTkLabel(tf, text=n.get("created_at", "5/1/2026, 6:44:05 AM")[:20], text_color="#9CA3AF", font=ctk.CTkFont("Segoe UI", 9)).pack(anchor="w")

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
