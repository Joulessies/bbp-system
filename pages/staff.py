import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
from database.db import (
    get_application_stats, get_all_applications, update_application_status,
    get_notifications, mark_all_notifications_read, clear_all_notifications,
    get_all_permits, issue_permit, get_staff_stats, add_notification,
    get_all_users, get_application_documents,
)


class StaffFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F4F5F7")
        self.controller = controller
        self.current_section = "Applications"
        self.nav_buttons = {}
        self._build_layout()

    def _build_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_main_content()

    # ── Sidebar ──────────────────────────────────────────────
    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color="#F9F9F9", width=220, corner_radius=0,
                               border_width=1, border_color="#E5E7EB")
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(3, weight=1)

        # brand
        brand = ctk.CTkFrame(sidebar, fg_color="#F9F9F9")
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

        # role badge
        ctk.CTkLabel(sidebar, text="👤  Staff Member", text_color="#2E7D32",
                     font=ctk.CTkFont("Segoe UI", 11, "bold")).grid(
            row=1, column=0, sticky="w", padx=18, pady=(8, 12))

        # nav
        nav = ctk.CTkFrame(sidebar, fg_color="#F9F9F9")
        nav.grid(row=2, column=0, sticky="ew", padx=10)
        for label in ["Applications", "Permit Holders", "Notifications"]:
            self._add_nav(nav, label, active=(label == "Applications"))

        # logout
        ctk.CTkButton(sidebar, text="Logout", command=self._logout,
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
        self.main_container.grid_rowconfigure(0, weight=1)

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
        self.host.grid(row=0, column=0, sticky="nsew", padx=24, pady=12)
        self.host.grid_columnconfigure(0, weight=1)

    def _render(self):
        self._clear()
        s = self.current_section
        
        if s == "Notifications":
            self._render_notifications()
        elif s == "Applications":
            self._render_applications()
        elif s == "Permit Holders":
            self._render_permit_holders()

    def update_welcome(self):
        self._render()

    def _stat_card(self, parent, col, title, value, icon, icon_bg, val_color, subtitle=""):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.grid(row=0, column=col, sticky="nsew", padx=4, pady=2)
        top = ctk.CTkFrame(card, fg_color="white")
        top.pack(fill="x", padx=14, pady=(14, 2))
        ctk.CTkLabel(top, text=title, text_color="#6B7280",
                     font=ctk.CTkFont("Segoe UI", 10)).pack(side="left")
        icon_lbl = ctk.CTkLabel(top, text=icon, fg_color=icon_bg,
                                width=32, height=32, corner_radius=8,
                                font=ctk.CTkFont(size=14))
        icon_lbl.pack(side="right")
        ctk.CTkLabel(card, text=value, text_color=val_color,
                     font=ctk.CTkFont("Segoe UI", 24, "bold")).pack(anchor="w", padx=14)
        if subtitle:
            ctk.CTkLabel(card, text=subtitle, text_color="#9CA3AF",
                         font=ctk.CTkFont("Segoe UI", 9)).pack(anchor="w", padx=14, pady=(0, 12))

    # ── Notifications view ───────────────────────────────────
    def _render_notifications(self):
        h = self.host
        notifs = get_notifications("admin")
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

        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=10)
        ctk.CTkLabel(card, text="All Notifications", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(
            anchor="w", padx=18, pady=(16, 8))
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
                ctk.CTkLabel(tf, text=n.get("title", ""),
                             text_color="#111827",
                             font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w")
                ctk.CTkLabel(tf, text=n.get("message", ""),
                             text_color="#6B7280",
                             font=ctk.CTkFont("Segoe UI", 9)).pack(anchor="w")
                ctk.CTkLabel(r, text=n.get("created_at", "")[:16], text_color="#9CA3AF",
                             font=ctk.CTkFont("Segoe UI", 8)).pack(side="right", padx=8)

    # ── Applications view ────────────────────────────────────
    def _render_applications(self):
        h = self.host
        apps = get_all_applications()
        
        # Get current staff member's email
        staff_email = self.controller.logged_in_user or ""

        # Build staff lookup map (email -> full name + email)
        staff_lookup = {}
        for staff in get_all_users():
            staff_email_key = (staff.get("email") or "").strip()
            if not staff_email_key:
                continue
            full_name = f"{staff.get('first_name', '')} {staff.get('last_name', '')}".strip()
            display_name = f"{full_name} ({staff_email_key})" if full_name else staff_email_key
            staff_lookup[staff_email_key] = display_name

        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 12))
        
        # Title and Filter Button
        title_row = ctk.CTkFrame(card, fg_color="white")
        title_row.pack(anchor="w", padx=18, pady=(16, 8), fill="x")
        ctk.CTkLabel(title_row, text="Applications", text_color="#111827", font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(side="left")
        
        # Filter button to show only assigned to me
        if not hasattr(self, 'filter_assigned_only'):
            self.filter_assigned_only = tk.BooleanVar(value=False)
        
        def toggle_filter():
            self.filter_assigned_only.set(not self.filter_assigned_only.get())
            self._render()
        
        filter_btn = ctk.CTkButton(title_row, text="📌 Assigned to Me", width=120, height=26,
                                   fg_color="#F3F4F6" if not self.filter_assigned_only.get() else "#E65C00",
                                   hover_color="#E5E7EB" if not self.filter_assigned_only.get() else "#CC5200",
                                   text_color="#374151" if not self.filter_assigned_only.get() else "white",
                                   font=ctk.CTkFont("Segoe UI", 9, "bold"),
                                   command=toggle_filter)
        filter_btn.pack(side="right", padx=(0, 18))
        
        hdr = ctk.CTkFrame(card, fg_color="#FAFAFA", corner_radius=0)
        hdr.pack(fill="x", padx=18)
        cols = [("ID", 50), ("Business Name", 130), ("Owner", 110), ("Type", 80), 
            ("Status", 90), ("Risk", 70), ("Score", 60), ("Assigned", 180), 
            ("Submitted", 90), ("Actions", 70)]
        for col, width in cols:
            ctk.CTkLabel(hdr, text=col, text_color="#374151", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=width, anchor="w").pack(side="left", padx=4, pady=6)
        
        # Filter apps if needed
        if self.filter_assigned_only.get():
            apps = [a for a in apps if a.get("assigned_to") == staff_email]
            
        if not apps:
            ctk.CTkLabel(card, text="No applications found", text_color="#9CA3AF", font=ctk.CTkFont("Segoe UI", 11)).pack(pady=30)
        else:
            for a in apps:
                row = ctk.CTkFrame(card, fg_color="white")
                row.pack(fill="x", padx=18, pady=4)
                
                docs_uploaded = get_application_documents(a["id"])
                docs_count = min(len(docs_uploaded), 6)
                base_score = int((docs_count / 6) * 70)  
                data_fields = [a.get("business_name"), a.get("business_address"), a.get("contact_number"), a.get("capital_investment"), a.get("tin_number"), a.get("dti_sec_cda_reg_no")]
                filled_count = sum(1 for f in data_fields if f and str(f).strip() and str(f) != "0" and str(f) != "0.0")
                data_score = int((filled_count / 6) * 30)
                total_score = base_score + data_score
                score = f"{total_score}%"
                
                cap = a.get("capital_investment", 0)
                if cap > 1000000:
                    risk = "High"
                    risk_color = "#FDE8E8"
                    risk_txt = "#E53E3E"
                elif cap > 100000:
                    risk = "Medium"
                    risk_color = "#FEF3C7"
                    risk_txt = "#D97706"
                else:
                    risk = "Low"
                    risk_color = "#E1F2E8"
                    risk_txt = "#2E7D32"
                    
                status_color = "#FFF4E5" if a["status"] in ("Pending", "Returned for Correction") else "#E8F5E9" if a["status"] in ("Approved", "Ready for Pickup") else "#FDE8E8"
                status_txt = "#F05A00" if a["status"] in ("Pending", "Returned for Correction") else "#2E7D32" if a["status"] in ("Approved", "Ready for Pickup") else "#E53E3E"
                
                ctk.CTkLabel(row, text=str(a["id"]), text_color="#374151", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=50, anchor="w").pack(side="left", padx=4)
                ctk.CTkLabel(row, text=a["business_name"], text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=130, anchor="w").pack(side="left", padx=4)
                owner_name = f"{a.get('owner_first_name', '')} {a.get('owner_last_name', '')}".strip() or a["user_email"]
                ctk.CTkLabel(row, text=owner_name, text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=110, anchor="w").pack(side="left", padx=4)
                ctk.CTkLabel(row, text=a.get("business_type", "Retail"), text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=80, anchor="w").pack(side="left", padx=4)
                
                # Status badge
                s_frame = ctk.CTkFrame(row, fg_color="transparent", width=90, height=35)
                s_frame.pack(side="left", padx=4)
                s_frame.pack_propagate(False)
                ctk.CTkLabel(s_frame, text=a["status"], text_color=status_txt, fg_color=status_color, corner_radius=10, font=ctk.CTkFont("Segoe UI", 8, "bold")).pack(anchor="w", pady=6, ipadx=4, ipady=2)
                
                # Risk Level
                r_frame = ctk.CTkFrame(row, fg_color="transparent", width=70, height=35)
                r_frame.pack(side="left", padx=4)
                r_frame.pack_propagate(False)
                ctk.CTkLabel(r_frame, text=risk, text_color=risk_txt, fg_color=risk_color, corner_radius=10, font=ctk.CTkFont("Segoe UI", 8, "bold")).pack(anchor="w", pady=6, ipadx=4, ipady=2)
                
                ctk.CTkLabel(row, text=score, text_color="#374151", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=60, anchor="w").pack(side="left", padx=4)
                
                assigned_email = a.get("assigned_to") or ""
                assigned = staff_lookup.get(assigned_email, assigned_email) if assigned_email else "Unassigned"
                ctk.CTkLabel(row, text=assigned, text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=180, anchor="w").pack(side="left", padx=4)
                ctk.CTkLabel(row, text=a.get("submitted_at", "")[:10], text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=90, anchor="w").pack(side="left", padx=4)
                
                if a["status"] in ("Pending", "Under Review"):
                    act_frame = ctk.CTkFrame(row, fg_color="transparent", width=70, height=35)
                    act_frame.pack(side="left", padx=4)
                    act_frame.pack_propagate(False)
                    ctk.CTkButton(act_frame, text="Review", width=60, height=24, fg_color="#E65C00", hover_color="#CC5200", text_color="white", font=ctk.CTkFont("Segoe UI", 9, "bold"), corner_radius=4, command=lambda a=a: self._open_review_modal(a)).pack(pady=5)
                else:
                    act_frame = ctk.CTkFrame(row, fg_color="transparent", width=70, height=35)
                    act_frame.pack(side="left", padx=4)
                    act_frame.pack_propagate(False)
                    ctk.CTkButton(act_frame, text="View", width=60, height=24, fg_color="#F3F4F6", hover_color="#E5E7EB", text_color="#374151", font=ctk.CTkFont("Segoe UI", 9), corner_radius=4, command=lambda a=a: self._open_review_modal(a)).pack(pady=5)

    # ── Permit Holders view ──────────────────────────────────
    def _render_permit_holders(self):
        h = self.host
        permits = get_all_permits()

        # Top summary box
        top_box = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        top_box.pack(fill="x", pady=(0, 20))
        
        stat = ctk.CTkFrame(top_box, fg_color="transparent")
        stat.pack(anchor="w", padx=20, pady=20)
        ctk.CTkLabel(stat, text="Total Clearances Issued", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 11)).pack(anchor="w")
        
        val_row = ctk.CTkFrame(stat, fg_color="transparent")
        val_row.pack(anchor="w", pady=(5, 0))
        ctk.CTkLabel(val_row, text=str(len(permits)), text_color="#111827", font=ctk.CTkFont("Segoe UI", 24, "bold")).pack(side="left")
        ctk.CTkLabel(val_row, text=" ✓ ", text_color="#2E7D32", fg_color="#E8F5E9", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=4).pack(side="left", padx=15)
        
        # Search and filters
        filters = ctk.CTkFrame(h, fg_color="transparent")
        filters.pack(fill="x", pady=(0, 10))
        
        # SEARCH RECORDS
        sf = ctk.CTkFrame(filters, fg_color="transparent")
        sf.pack(side="left", padx=(0, 15))
        ctk.CTkLabel(sf, text="SEARCH RECORDS", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        
        if not hasattr(self, "permit_search_var"):
            self.permit_search_var = tk.StringVar(value="")
            
        search_entry = ctk.CTkEntry(sf, textvariable=self.permit_search_var, placeholder_text="🔍 Business or Owner...", width=200, height=35, fg_color="#F9FAFB", border_color="#E5E7EB")
        search_entry.pack()

        # FILTER BY YEAR
        yf = ctk.CTkFrame(filters, fg_color="transparent")
        yf.pack(side="left", padx=15)
        ctk.CTkLabel(yf, text="FILTER BY YEAR", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ctk.CTkOptionMenu(yf, values=["All Years", "2026", "2025"], fg_color="#F9FAFB", text_color="#111827", button_color="#F9FAFB", button_hover_color="#F3F4F6", dropdown_fg_color="white", dropdown_text_color="#111827", height=35).pack()

        # START DATE
        sdf = ctk.CTkFrame(filters, fg_color="transparent")
        sdf.pack(side="left", padx=15)
        ctk.CTkLabel(sdf, text="START DATE", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ctk.CTkEntry(sdf, placeholder_text="dd/mm/yyyy 📅", width=150, height=35, fg_color="#F9FAFB", border_color="#E5E7EB").pack()

        # END DATE
        edf = ctk.CTkFrame(filters, fg_color="transparent")
        edf.pack(side="left", padx=15)
        ctk.CTkLabel(edf, text="END DATE", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        ctk.CTkEntry(edf, placeholder_text="dd/mm/yyyy 📅", width=150, height=35, fg_color="#F9FAFB", border_color="#E5E7EB").pack()

        # Tabs & Apply Filters
        tabs = ctk.CTkFrame(h, fg_color="transparent")
        tabs.pack(fill="x", pady=(10, 20))
        ctk.CTkButton(tabs, text="Apply Filters / Search", width=140, height=30, fg_color="#E65C00", hover_color="#CC5200", text_color="white", font=ctk.CTkFont("Segoe UI", 10, "bold"), corner_radius=6, command=self._render).pack(side="left", padx=(0, 15))
        ctk.CTkButton(tabs, text="Current Year", width=100, height=30, fg_color="white", text_color="#E65C00", border_width=1, border_color="#E65C00", corner_radius=20).pack(side="left", padx=(0, 5))
        ctk.CTkButton(tabs, text="All History", width=100, height=30, fg_color="#F3F4F6", text_color="#6B7280", hover_color="#E5E7EB", corner_radius=20).pack(side="left")

        # Active Permit Holders
        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        card.pack(fill="x")
        
        ctk.CTkLabel(card, text="Active Permit Holders", text_color="#111827", font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(16, 12))
        
        hdr = ctk.CTkFrame(card, fg_color="#FAFAFA", corner_radius=0)
        hdr.pack(fill="x", padx=18)
        cols = [("Year", 60), ("Business Name", 200), ("Owner", 160), ("Type", 100), ("Status", 100), ("Actions", 140)]
        for col, width in cols:
            ctk.CTkLabel(hdr, text=col, text_color="#374151", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=width, anchor="w").pack(side="left", padx=4, pady=6)
            
        if not permits:
            ctk.CTkLabel(card, text="No permits issued yet", text_color="#9CA3AF", font=ctk.CTkFont("Segoe UI", 11)).pack(pady=30)
        else:
            # Apply filtering
            query = self.permit_search_var.get().lower() if hasattr(self, "permit_search_var") else ""
            apps = get_all_applications()
            
            filtered_permits = []
            for p in permits:
                app = next((a for a in apps if a["id"] == p["application_id"]), {})
                owner = f"{app.get('owner_first_name', '')} {app.get('owner_last_name', '')}".strip() or p["user_email"]
                if query and query not in p["business_name"].lower() and query not in owner.lower() and query not in p["permit_number"].lower():
                    continue
                filtered_permits.append((p, app, owner))
                
            if not filtered_permits:
                ctk.CTkLabel(card, text="No matches found for your search", text_color="#9CA3AF", font=ctk.CTkFont("Segoe UI", 11)).pack(pady=30)

            for p, app, owner in filtered_permits:
                row = ctk.CTkFrame(card, fg_color="white")
                row.pack(fill="x", padx=18, pady=4)
                
                year = p["issued_at"][:4] if p["issued_at"] else "2026"
                app_type = "RENEWAL" if app.get("business_type", "").lower() == "renewal" else "NEW"
                
                ctk.CTkLabel(row, text=year, text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=60, anchor="w").pack(side="left", padx=4)
                ctk.CTkLabel(row, text=p["business_name"], text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=200, anchor="w").pack(side="left", padx=4)
                ctk.CTkLabel(row, text=owner, text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=160, anchor="w").pack(side="left", padx=4)
                
                ctk.CTkLabel(row, text=app_type, text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=100, anchor="w").pack(side="left", padx=4)
                
                s_frame = ctk.CTkFrame(row, fg_color="transparent", width=100, height=35)
                s_frame.pack(side="left", padx=4)
                s_frame.pack_propagate(False)
                ctk.CTkLabel(s_frame, text=p.get("status", "Approved"), text_color="#2E7D32", fg_color="#E8F5E9", corner_radius=10, font=ctk.CTkFont("Segoe UI", 9, "bold")).pack(anchor="w", pady=6, ipadx=6, ipady=2)
                
                act = ctk.CTkFrame(row, fg_color="transparent", width=140, height=35)
                act.pack(side="left", padx=4)
                act.pack_propagate(False)
                ctk.CTkButton(act, text="View", width=60, height=24, fg_color="#F3F4F6", hover_color="#E5E7EB", text_color="#374151", font=ctk.CTkFont("Segoe UI", 10, "bold"), corner_radius=4, command=lambda p=p, o=owner, t=app_type: self._view_permit(p, o, t)).pack(side="left", padx=(0, 5), pady=5)
                ctk.CTkButton(act, text="Print", width=60, height=24, fg_color="#E65C00", hover_color="#CC5200", text_color="white", font=ctk.CTkFont("Segoe UI", 10, "bold"), corner_radius=4, command=lambda p=p, o=owner: self._print_permit(p, o)).pack(side="left", pady=5)

    def _view_permit(self, p, owner, app_type):
        details = f"Permit Number: {p['permit_number']}\nBusiness Name: {p['business_name']}\nOwner: {owner}\nType: {app_type}\nExpires: {(p.get('expires_at') or '')[:10]}"
        messagebox.showinfo("Permit Details", details)

    def _print_permit(self, p, owner_name):
        import os, tempfile, webbrowser
        from datetime import datetime
        
        try:
            date_str = p.get('issued_at', str(datetime.now()))[:10]
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = dt.strftime('%B %d, %Y')
        except:
            formatted_date = datetime.now().strftime('%B %d, %Y')

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
            <title>Barangay Business Clearance - {p.get('permit_number', '')}</title>
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
                @media print {{ body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }} }}
            </style>
        </head>
        <body onload="window.print()">
            <div class="permit-box">
                <img src="data:image/jpeg;base64,{logo_b64}" width="90" height="90" style="position: absolute; left: 40px; top: 20px;">
                <img src="data:image/jpeg;base64,{brgy_b64}" width="90" height="90" style="position: absolute; right: 40px; top: 20px;">
                <div class="header">REPUBLIC OF THE PHILIPPINES<br>CITY OF CALOOCAN<br><span class="header-title">BARANGAY 183, ZONE 16, DISTRICT 1</span><br>Office of the Punong Barangay</div>
                <div class="red-line"></div>
                <div class="main-title">BARANGAY BUSINESS CLEARANCE</div>
                <div class="content">
                    <b>TO WHOM IT MAY CONCERN:</b><br><br>
                    <p>This is to certify that the business establishment <b>{p.get('business_name', '')}</b>, owned and operated by <b>{owner_name}</b>, with business address located at <b>{p.get('business_address', '_____________________')}</b> has been granted this Barangay Business Clearance.</p>
                    <p>This clearance is issued upon the request of the applicant for the purpose of securing a Business/Mayor's Permit and for whatever legal intent it may serve, provided that the business complies with all applicable laws and ordinances.</p>
                    <p>The applicant has complied with the requirements of this barangay and has paid the necessary fees in accordance with the existing barangay revenue code.</p>
                    <p>Issued this <b>{formatted_date}</b> at Barangay 183, Zone 16, Caloocan City.</p>
                </div>
                <div class="footer-grid">
                    <div class="sig-box"><div style="text-align: left; font-size: 12px; color: #4b5563; padding-left: 10%;">Conforme / Signature of Applicant:</div><div class="sig-line"></div><div class="sig-name">{owner_name}</div><div class="sig-title">Applicant / Owner</div></div>
                    <div class="sig-box"><div style="text-align: left; font-size: 12px; color: #4b5563; padding-left: 10%;">Approved By:</div><div class="sig-line"></div><div class="sig-name red-text">HON. MICHAEL RONALD PUNONGBAYAN</div><div class="sig-title">Punong Barangay</div></div>
                </div>
                <div class="bottom-info">
                    <div>Clearance No: {p.get('permit_number', '')}<br>O.R. No: __________________<br>Amount Paid: P 500.00</div>
                    <div style="text-align: right;"><span class="red-text">NOT VALID WITHOUT DRY SEAL</span><br>Valid until: December 31, {datetime.now().year}</div>
                </div>
            </div>
        </body>
        </html>
        """
        
        fd, path = tempfile.mkstemp(suffix=".html")
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        webbrowser.open('file://' + os.path.realpath(path))

    def _open_review_modal(self, app):
        modal = ctk.CTkToplevel(self)
        modal.title(f"Review Application #{app['id']}")
        modal.geometry("620x680")
        modal.resizable(False, False)
        modal.grab_set()
        modal.configure(fg_color="#F4F5F7")

        hdr = ctk.CTkFrame(modal, fg_color="#E65C00", corner_radius=0, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=f"📋  Review Application #{app['id']}", text_color="white",
                     font=ctk.CTkFont("Segoe UI", 16, "bold")).pack(side="left", padx=20, pady=15)
        st = app.get("status", "Pending")
        st_bg = {"Pending": "#FFF4E5", "Under Review": "#EBF5FF", "Approved": "#E8F5E9", "Rejected": "#FDE8E8"}
        st_tc = {"Pending": "#D9A100", "Under Review": "#1D4ED8", "Approved": "#2E7D32", "Rejected": "#E53E3E"}
        ctk.CTkLabel(hdr, text=st, fg_color=st_bg.get(st, "#F3F4F6"), text_color=st_tc.get(st, "#374151"),
                     corner_radius=12, font=ctk.CTkFont("Segoe UI", 10, "bold"), width=90, height=26).pack(side="right", padx=20)

        body = ctk.CTkScrollableFrame(modal, fg_color="#F4F5F7")
        body.pack(fill="both", expand=True, padx=16, pady=(12, 0))

        def section(parent, title, icon=""):
            f = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
            f.pack(fill="x", pady=(0, 10))
            ctk.CTkLabel(f, text=f"{icon}  {title}", text_color="#111827",
                         font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(anchor="w", padx=16, pady=(14, 8))
            return f

        def field(parent, label, value):
            row = ctk.CTkFrame(parent, fg_color="white")
            row.pack(fill="x", padx=16, pady=2)
            ctk.CTkLabel(row, text=label, text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=160, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=str(value or "—"), text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold"), anchor="w").pack(side="left", fill="x", expand=True)

        s1 = section(body, "Business Information", "🏢")
        field(s1, "Business Name", app.get("business_name"))
        field(s1, "Business Type", app.get("business_type"))
        field(s1, "Ownership Type", app.get("ownership_type"))
        field(s1, "Business Address", app.get("business_address"))
        ctk.CTkFrame(s1, fg_color="white", height=8).pack()

        s2 = section(body, "Owner Details", "👤")
        owner = f"{app.get('owner_first_name', '')} {app.get('owner_last_name', '')}".strip()
        field(s2, "Full Name", owner)
        field(s2, "Email", app.get("user_email"))
        field(s2, "Contact Number", app.get("contact_number"))
        field(s2, "Gender", app.get("gender"))
        ctk.CTkFrame(s2, fg_color="white", height=8).pack()

        s3 = section(body, "Financial & Registration", "💰")
        cap = app.get("capital_investment", 0)
        field(s3, "Capital Investment", f"₱{cap:,.2f}" if cap else "—")
        male = app.get("employees_male", 0) or 0
        female = app.get("employees_female", 0) or 0
        field(s3, "Employees (M / F)", f"{male} Male  /  {female} Female")
        field(s3, "TIN Number", app.get("tin_number"))
        field(s3, "DTI/SEC/CDA Reg. No.", app.get("dti_sec_cda_reg_no"))
        ctk.CTkFrame(s3, fg_color="white", height=8).pack()

        staff_lookup_modal = {}
        for staff in get_all_users():
            staff_email_key = (staff.get("email") or "").strip()
            if not staff_email_key:
                continue
            full_name = f"{staff.get('first_name', '')} {staff.get('last_name', '')}".strip()
            display_name = f"{full_name} ({staff_email_key})" if full_name else staff_email_key
            staff_lookup_modal[staff_email_key] = display_name

        s4 = section(body, "Application Meta", "📊")
        field(s4, "Submitted At", (app.get("submitted_at") or "")[:19])
        assigned_email = app.get("assigned_to") or ""
        assigned_display = staff_lookup_modal.get(assigned_email, assigned_email) if assigned_email else "Unassigned"
        field(s4, "Assigned To", assigned_display)
        field(s4, "Risk Level", app.get("risk_level", "Low"))
        ctk.CTkFrame(s4, fg_color="white", height=8).pack()

        # Documents section - show uploaded document status
        s5 = section(body, "Uploaded Documents", "📎")
        docs = ["DTI / SEC / CDA Registration", "Fire Safety Inspection Certificate",
                "Affidavit of Undertaking", "Business Permit Application Form (Signed)",
                "Locational Clearance", "Sketch / Location Plan"]
        doc_rows = get_application_documents(app["id"])
        doc_map = {d["doc_name"]: d["file_path"] for d in doc_rows}

        def open_doc(path):
            if not path or not os.path.exists(path):
                messagebox.showerror("Missing File", "Document file not found.")
                return
            try:
                os.startfile(path)
            except OSError:
                messagebox.showerror("Open Failed", "Could not open document.")

        docs_received = 0
        for doc in docs:
            file_path = doc_map.get(doc, "")
            is_received = bool(file_path and os.path.exists(file_path))
            if is_received:
                docs_received += 1
            doc_row = ctk.CTkFrame(s5, fg_color="white")
            doc_row.pack(fill="x", padx=16, pady=4)
            ctk.CTkLabel(doc_row, text=f"• {doc}", text_color="#374151",
                         font=ctk.CTkFont("Segoe UI", 10), anchor="w").pack(side="left", fill="x", expand=True)
            if is_received:
                ctk.CTkButton(doc_row, text="View", width=60, height=24,
                              fg_color="#EBF5FF", hover_color="#DBEAFE", text_color="#1D4ED8",
                              font=ctk.CTkFont("Segoe UI", 9, "bold"), corner_radius=4,
                              command=lambda p=file_path: open_doc(p)).pack(side="right", padx=(6, 0))
                ctk.CTkLabel(doc_row, text="✓ Received", text_color="#2E7D32",
                             font=ctk.CTkFont("Segoe UI", 9, "bold")).pack(side="right")
            else:
                ctk.CTkLabel(doc_row, text="Missing", text_color="#E53E3E",
                             font=ctk.CTkFont("Segoe UI", 9, "bold")).pack(side="right")

        doc_summary = ctk.CTkFrame(s5, fg_color="#E8F5E9", corner_radius=6)
        doc_summary.pack(fill="x", padx=16, pady=(8, 0))
        ctk.CTkLabel(doc_summary, text=f"✓ {docs_received}/{len(docs)} documents received",
                     text_color="#2E7D32", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(padx=10, pady=6)
        ctk.CTkFrame(s5, fg_color="white", height=8).pack()

        nf = ctk.CTkFrame(body, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        nf.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(nf, text="📝  Reviewer Notes", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(anchor="w", padx=16, pady=(14, 6))
        notes_entry = ctk.CTkTextbox(nf, height=60, fg_color="#F9FAFB", border_width=1, border_color="#E5E7EB",
                                     font=ctk.CTkFont("Segoe UI", 10), text_color="#374151", corner_radius=6)
        notes_entry.pack(fill="x", padx=16, pady=(0, 14))
        if app.get("notes"):
            notes_entry.insert("1.0", app["notes"])

        btn_frame = ctk.CTkFrame(modal, fg_color="#F4F5F7")
        btn_frame.pack(fill="x", padx=16, pady=(8, 16))

        def do_approve():
            modal.destroy()
            self._approve_app(app)

        def do_reject():
            modal.destroy()
            self._reject_app(app)

        def do_return():
            notes = notes_entry.get("1.0", "end-1c").strip()
            update_application_status(app["id"], "Returned for Correction", self.controller.logged_in_user or "staff@bbp.com")
            add_notification(app["user_email"], "Application Returned",
                             f"Your application for '{app['business_name']}' was returned for correction. Notes: {notes}")
            modal.destroy()
            messagebox.showinfo("Returned", "Application returned for correction.")
            self._render()

        ctk.CTkButton(btn_frame, text="✓  Approve & Issue Permit", width=180, height=38,
                      fg_color="#2E7D32", hover_color="#1B5E20", text_color="white",
                      font=ctk.CTkFont("Segoe UI", 11, "bold"), corner_radius=6, command=do_approve).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_frame, text="↩  Return for Correction", width=170, height=38,
                      fg_color="#FFF4E5", hover_color="#FDECD0", text_color="#D9A100",
                      font=ctk.CTkFont("Segoe UI", 11, "bold"), corner_radius=6, command=do_return).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_frame, text="✕  Reject", width=100, height=38,
                      fg_color="#FDE8E8", hover_color="#FECACA", text_color="#E53E3E",
                      font=ctk.CTkFont("Segoe UI", 11, "bold"), corner_radius=6, command=do_reject).pack(side="left")
        ctk.CTkButton(btn_frame, text="Close", width=80, height=38,
                      fg_color="white", hover_color="#EDEDED", text_color="#374151",
                      border_width=1, border_color="#D0D5DD", font=ctk.CTkFont("Segoe UI", 10),
                      corner_radius=6, command=modal.destroy).pack(side="right")

    def _approve_app(self, app):
        update_application_status(app["id"], "Approved", self.controller.logged_in_user or "staff@bbp.com")
        pnum = issue_permit(app["id"], app["user_email"], app["business_name"])
        add_notification("admin", "Application Approved",
                         f"Permit {pnum} issued for '{app['business_name']}'.")
        add_notification(app["user_email"], "Permit Approved",
                         f"Your application for '{app['business_name']}' has been approved! Permit: {pnum}")
        messagebox.showinfo("Approved", f"Permit {pnum} issued.")
        self._render()

    def _reject_app(self, app):
        update_application_status(app["id"], "Rejected", self.controller.logged_in_user or "staff@bbp.com")
        add_notification("admin", "Application Rejected",
                         f"Application #{app['id']} for '{app['business_name']}' was rejected.")
        add_notification(app["user_email"], "Application Rejected",
                         f"Your application for '{app['business_name']}' has been rejected.")
        messagebox.showinfo("Rejected", "Application rejected.")
        self._render()
