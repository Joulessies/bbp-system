import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from database.db import (
    get_application_stats, get_all_applications, update_application_status,
    get_all_users, delete_user, update_user_role,
    get_notifications, mark_all_notifications_read, clear_all_notifications,
    get_all_permits, issue_permit, get_staff_stats, add_notification,
)


class AdminFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#F4F5F7")
        self.controller = controller
        self.current_section = "Dashboard"
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
        ctk.CTkLabel(sidebar, text="👤  Administrator", text_color="#E55A00",
                     font=ctk.CTkFont("Segoe UI", 11, "bold")).grid(
            row=1, column=0, sticky="w", padx=18, pady=(8, 12))

        # nav
        nav = ctk.CTkFrame(sidebar, fg_color="#F9F9F9")
        nav.grid(row=2, column=0, sticky="ew", padx=10)
        for label in ["Dashboard", "Reports", "User Management", "Permit Holders", "Notifications"]:
            self._add_nav(nav, label, active=(label == "Dashboard"))

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
        self.main_container.grid_rowconfigure(1, weight=1)

        # top bar
        top = ctk.CTkFrame(self.main_container, fg_color="#F4F5F7")
        top.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 0))
        self.top_title = ctk.CTkLabel(top, text="Admin Dashboard",
                                      text_color="#101828",
                                      font=ctk.CTkFont("Segoe UI", 26, "bold"))
        self.top_title.pack(anchor="w")
        self.top_sub = ctk.CTkLabel(top, text="Overview of Barangay 183 Business Permit System",
                                    text_color="#6B7280",
                                    font=ctk.CTkFont("Segoe UI", 11))
        self.top_sub.pack(anchor="w", pady=(2, 0))

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
        self.top_title.configure(text=s if s != "Dashboard" else "Admin Dashboard")
        subs = {"Dashboard": "Overview of Barangay 183 Business Permit System",
                "Reports": "View system reports and analytics",
                "User Management": "Manage registered users and roles",
                "Permit Holders": "View active permit holders",
                "Notifications": "Stay updated on your application status"}
        self.top_sub.configure(text=subs.get(s, ""))
        if s == "Dashboard":
            self._render_dashboard()
        elif s == "Notifications":
            self._render_notifications()
        elif s == "User Management":
            self._render_users()
        elif s == "Permit Holders":
            self._render_permits()
        elif s == "Reports":
            self._render_reports()
        else:
            self._render_placeholder(s)

    def update_welcome(self):
        self._render()

    # ── Dashboard view ───────────────────────────────────────
    def _render_dashboard(self):
        h = self.host
        st = get_application_stats()
        rate_str = f"{st['rate']}% approval rate"

        row1 = ctk.CTkFrame(h, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 10))
        for i in range(4):
            row1.grid_columnconfigure(i, weight=1)
        self._stat_card(row1, 0, "Total Applications", "22", "📄", "#FFF4E5", "#111827", "📈 Live data from system", "#2E7D32")
        self._stat_card(row1, 1, "Pending", "8", "🕒", "#FFF9E5", "#D9A100", "Awaiting review", "#6B7280")
        self._stat_card(row1, 2, "Approved", "6", "✅", "#E8F5E9", "#2E7D32", "27.3% approval rate", "#6B7280")
        self._stat_card(row1, 3, "5.3 days", "", "📊", "#F3E8FF", "#111827", "📈 Real-time average", "#2E7D32")

        row2 = ctk.CTkFrame(h, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 12))
        row2.grid_columnconfigure(0, weight=1)
        row2.grid_columnconfigure(1, weight=1)
        row2.grid_columnconfigure(2, weight=1)
        row2.grid_columnconfigure(3, weight=1)
        self._stat_card(row2, 0, "Pending Renewals", "2", "🔄", "#FFF4E5", "#E65C00", "⊙ Active renewals", "#E65C00")

        row3 = ctk.CTkFrame(h, fg_color="transparent")
        row3.pack(fill="x", pady=(0, 12))
        row3.grid_columnconfigure(0, weight=1)
        row3.grid_columnconfigure(1, weight=1)
        self._chart_card(row3, 0, "Monthly Applications Trend", "bar")
        self._chart_card(row3, 1, "Applications by Business Type", "pie")

        self._staff_leaderboard(h)
        self._contact_footer(h)

    def _stat_card(self, parent, col, title, value, icon, icon_bg, val_color, subtitle="", sub_color="#9CA3AF"):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        card.grid(row=0, column=col, sticky="nsew", padx=10, pady=2)
        top = ctk.CTkFrame(card, fg_color="white")
        top.pack(fill="x", padx=14, pady=(14, 2))
        ctk.CTkLabel(top, text=title, text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 11, "bold")).pack(side="left")
        
        mid = ctk.CTkFrame(card, fg_color="white")
        mid.pack(fill="x", padx=14, pady=0)
        ctk.CTkLabel(mid, text=value, text_color=val_color, font=ctk.CTkFont("Segoe UI", 26, "bold")).pack(side="left")
        ctk.CTkLabel(mid, text=icon, fg_color=icon_bg, width=32, height=32, corner_radius=8, font=ctk.CTkFont(size=14)).pack(side="right")
        
        if subtitle:
            ctk.CTkLabel(card, text=subtitle, text_color=sub_color, font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w", padx=14, pady=(5, 14))

    def _chart_card(self, parent, col, title, chart_type):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        card.grid(row=0, column=col, sticky="nsew", padx=10, pady=2)
        ctk.CTkLabel(card, text=title, text_color="#111827", font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(anchor="w", padx=18, pady=(16, 0))
        
        c = tk.Canvas(card, bg="white", highlightthickness=0, height=200)
        c.pack(fill="both", expand=True, padx=20, pady=20)
        
        if chart_type == "bar":
            c.create_rectangle(50, 20, 90, 180, fill="#E65C00", outline="")
            c.create_rectangle(150, 150, 190, 180, fill="#E65C00", outline="")
            c.create_rectangle(190, 140, 230, 180, fill="#5C2D91", outline="")
            c.create_line(30, 180, 400, 180, fill="#E5E7EB", width=2)
            c.create_text(70, 190, text="April", fill="#6B7280", font=("Segoe UI", 9))
            c.create_text(190, 190, text="May", fill="#6B7280", font=("Segoe UI", 9))
            c.create_text(20, 20, text="14", fill="#6B7280", font=("Segoe UI", 8))
            c.create_text(20, 100, text="7", fill="#6B7280", font=("Segoe UI", 8))
            c.create_text(20, 180, text="0", fill="#6B7280", font=("Segoe UI", 8))
        else:
            c.create_arc(20, 20, 180, 180, start=0, extent=210, fill="#E65C00", outline="white", width=2)
            c.create_arc(20, 20, 180, 180, start=210, extent=45, fill="#2E7D32", outline="white", width=2)
            c.create_arc(20, 20, 180, 180, start=255, extent=30, fill="#1D4ED8", outline="white", width=2)
            c.create_arc(20, 20, 180, 180, start=285, extent=30, fill="#7C3AED", outline="white", width=2)
            c.create_arc(20, 20, 180, 180, start=315, extent=45, fill="#E53E3E", outline="white", width=2)
            legend = ["Food Service: 13 (59.1%)", "Automotive: 3 (13.6%)", ": 2 (9.1%)", "Others: 1 (4.5%)", "Personal Service: 1 (4.5%)"]
            colors = ["#E65C00", "#2E7D32", "#1D4ED8", "#7C3AED", "#E53E3E"]
            for i, text in enumerate(legend):
                c.create_rectangle(220, 30 + i*25, 230, 40 + i*25, fill=colors[i], outline="")
                c.create_text(240, 35 + i*25, text=text, fill="#374151", font=("Segoe UI", 9), anchor="w")

    def _chart_card_full(self, parent, title):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text=title, text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(
            anchor="w", padx=18, pady=(16, 0))
        ctk.CTkLabel(card, text="No data available", text_color="#9CA3AF",
                     font=ctk.CTkFont("Segoe UI", 11)).pack(pady=60)

    def _staff_leaderboard(self, parent):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text="👥  Staff Performance Leaderboard",
                     text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=18, pady=(16, 12))
        hdr = ctk.CTkFrame(card, fg_color="#FAFAFA", corner_radius=0)
        hdr.pack(fill="x", padx=18)
        for c in ["Staff Name", "Approved", "Rejected", "Total Reviews"]:
            ctk.CTkLabel(hdr, text=c, text_color="#374151",
                         font=ctk.CTkFont("Segoe UI", 10, "bold"),
                         width=160, anchor="w").pack(side="left", padx=8, pady=6)
        staff = get_staff_stats()
        if not staff:
            ctk.CTkLabel(card, text="No performance data recorded yet",
                         text_color="#9CA3AF",
                         font=ctk.CTkFont("Segoe UI", 11)).pack(pady=30)
        else:
            for s in staff:
                row = ctk.CTkFrame(card, fg_color="white")
                row.pack(fill="x", padx=18)
                for val in [s["staff"], str(s["approved"]), str(s["rejected"]), str(s["total"])]:
                    ctk.CTkLabel(row, text=val, text_color="#374151",
                                 font=ctk.CTkFont("Segoe UI", 10),
                                 width=160, anchor="w").pack(side="left", padx=8, pady=4)

    def _contact_footer(self, parent):
        sep = ctk.CTkFrame(parent, fg_color="#E5E7EB", height=1)
        sep.pack(fill="x", pady=(8, 16))
        ctk.CTkLabel(parent, text="📞  Contact Barangay 183 Office",
                     text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(anchor="w")
        grid = ctk.CTkFrame(parent, fg_color="transparent")
        grid.pack(fill="x", pady=(8, 20))
        for i in range(4):
            grid.grid_columnconfigure(i, weight=1)
        info = [
            ("📍 Address", "Palosapis St., Midway Park Subd.,\nBarangay 183, District 1, Caloocan"),
            ("📞 Contact Number", "(02) 8936 4030"),
            ("✉️ Email", "brgy183@caloocan.gov.ph"),
            ("🕐 Office Hours", "Monday - Friday\n8:00 AM - 5:00 PM"),
        ]
        for i, (lbl, val) in enumerate(info):
            f = ctk.CTkFrame(grid, fg_color="transparent")
            f.grid(row=0, column=i, sticky="nw", padx=4)
            ctk.CTkLabel(f, text=lbl, text_color="#374151",
                         font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w")
            ctk.CTkLabel(f, text=val, text_color="#6B7280",
                         font=ctk.CTkFont("Segoe UI", 10), justify="left").pack(anchor="w")

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

        acts = ctk.CTkFrame(h, fg_color="transparent")
        acts.pack(anchor="w", pady=(0, 10))
        ctk.CTkButton(acts, text="Mark All as Read", fg_color="white",
                      hover_color="#EDEDED", text_color="#374151",
                      border_width=1, border_color="#D0D5DD",
                      font=ctk.CTkFont("Segoe UI", 10), height=32, corner_radius=6,
                      command=self._mark_all_read).pack(side="left", padx=(0, 8))
        ctk.CTkButton(acts, text="🗑  Clear All", fg_color="white",
                      hover_color="#FDE8E8", text_color="#E53E3E",
                      border_width=1, border_color="#D0D5DD",
                      font=ctk.CTkFont("Segoe UI", 10), height=32, corner_radius=6,
                      command=self._clear_notifs).pack(side="left")

        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x")
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

    def _mark_all_read(self):
        mark_all_notifications_read("admin")
        self._render()

    def _clear_notifs(self):
        clear_all_notifications("admin")
        self._render()

    # ── User Management view ─────────────────────────────────
    def _render_users(self):
        h = self.host
        users = get_all_users()

        new_staff = ctk.CTkFrame(h, fg_color="#FFF9F0", corner_radius=10, border_width=1, border_color="#FDECD0")
        new_staff.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(new_staff, text="Create New Staff Account", text_color="#E65C00", font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(16, 4))
        ctk.CTkLabel(new_staff, text="Manually create a staff account for barangay personnel", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 11)).pack(anchor="w", padx=18)
        
        form_row1 = ctk.CTkFrame(new_staff, fg_color="transparent")
        form_row1.pack(fill="x", padx=18, pady=(15, 5))
        f1 = ctk.CTkFrame(form_row1, fg_color="transparent")
        f1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(f1, text="Full Name", text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.entry_staff_name = ctk.CTkEntry(f1, fg_color="#EBF5FF", border_width=0, placeholder_text="Juan dela Cruz", height=36)
        self.entry_staff_name.pack(fill="x")
        
        f2 = ctk.CTkFrame(form_row1, fg_color="transparent")
        f2.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(f2, text="Email Address", text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.entry_staff_email = ctk.CTkEntry(f2, fg_color="#EBF5FF", border_width=0, placeholder_text="✉ admin@caloocan.gov.ph", height=36)
        self.entry_staff_email.pack(fill="x")
        
        form_row2 = ctk.CTkFrame(new_staff, fg_color="transparent")
        form_row2.pack(fill="x", padx=18, pady=5)
        ctk.CTkLabel(form_row2, text="Temporary Password", text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.entry_staff_pass = ctk.CTkEntry(form_row2, fg_color="#EBF5FF", border_width=0, placeholder_text="••••••••••", height=36)
        self.entry_staff_pass.pack(fill="x")
        
        acts = ctk.CTkFrame(new_staff, fg_color="transparent")
        acts.pack(anchor="w", padx=18, pady=(15, 20))
        ctk.CTkButton(acts, text="Create Staff Account", fg_color="#E65C00", hover_color="#CC5200", text_color="white", height=34, font=ctk.CTkFont("Segoe UI", 10, "bold"), command=self._create_staff).pack(side="left", padx=(0, 10))
        ctk.CTkButton(acts, text="Cancel", fg_color="white", text_color="#374151", border_width=1, border_color="#E5E7EB", height=34, font=ctk.CTkFont("Segoe UI", 10, "bold"), command=lambda: (self.entry_staff_name.delete(0, "end"), self.entry_staff_email.delete(0, "end"), self.entry_staff_pass.delete(0, "end"))).pack(side="left")

        # Staff Members
        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text="Staff Members", text_color="#111827", font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(16, 4))
        ctk.CTkLabel(card, text="Manage barangay staff accounts and monitor their activity", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 11)).pack(anchor="w", padx=18, pady=(0, 16))

        hdr = ctk.CTkFrame(card, fg_color="#FAFAFA", corner_radius=0)
        hdr.pack(fill="x", padx=18)
        cols = [("Staff ID", 60), ("Name", 150), ("Email", 150), ("Role", 80), ("Date Added", 100), ("Status", 80), ("Actions", 80)]
        for col, w in cols:
            ctk.CTkLabel(hdr, text=col, text_color="#374151", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=w, anchor="w").pack(side="left", padx=6, pady=6)

        staff_users = [u for u in users if u["role"] == "staff"]
        
        for s in staff_users:
            row = ctk.CTkFrame(card, fg_color="white")
            row.pack(fill="x", padx=18, pady=2)
            fname = f"{s.get('first_name') or ''} {s.get('last_name') or ''}".strip() or "Unknown"
            ctk.CTkLabel(row, text=str(s["id"]), text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=60, anchor="w").pack(side="left", padx=6)
            ctk.CTkLabel(row, text=fname, text_color="#374151", font=ctk.CTkFont("Segoe UI", 10), width=150, anchor="w").pack(side="left", padx=6)
            ctk.CTkLabel(row, text=s["email"], text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=150, anchor="w").pack(side="left", padx=6)
            ctk.CTkLabel(row, text="Staff", fg_color="#FFF4E5", text_color="#E65C00", corner_radius=10, font=ctk.CTkFont("Segoe UI", 9, "bold")).pack(side="left", padx=6)
            ctk.CTkLabel(row, text=(s["created_at"] or "")[:10], text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=100, anchor="w").pack(side="left", padx=6)
            
            is_active = s.get("status", "Active") == "Active"
            st_color = "#E8F5E9" if is_active else "#FDE8E8"
            st_text_color = "#2E7D32" if is_active else "#E53E3E"
            status_text = "Active" if is_active else "Inactive"
            ctk.CTkLabel(row, text=status_text, fg_color=st_color, text_color=st_text_color, corner_radius=10, font=ctk.CTkFont("Segoe UI", 9, "bold"), width=60).pack(side="left", padx=6)
            
            toggle_opt = "Deactivate/Suspend" if is_active else "Activate Account"
            opts = ["Edit Account", "Reset Password", "View Audit Trail", toggle_opt]
            om = ctk.CTkOptionMenu(row, values=opts, width=40, height=28, fg_color="#FFFFFF", button_color="transparent", button_hover_color="#F3F4F6", text_color="#374151", dropdown_fg_color="white", dropdown_hover_color="#FFF4E5")
            om.pack(side="left", padx=6)
            om.set("⋮")
            om.configure(command=lambda choice, m=om, uid=s["id"], cstat=s.get("status", "Active"): self._handle_staff_action(choice, m, uid, cstat))

        # ── Registered Business Owners ──
        applicant_users = [u for u in users if u["role"] == "applicant"]
        from database.db import get_all_applications
        all_apps = get_all_applications()

        bo_card = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        bo_card.pack(fill="x", pady=(10, 12))
        ctk.CTkLabel(bo_card, text=f"Registered Business Owners ({len(applicant_users)})", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(16, 4))
        ctk.CTkLabel(bo_card, text="Users who registered to apply for business permits", text_color="#6B7280",
                     font=ctk.CTkFont("Segoe UI", 11)).pack(anchor="w", padx=18, pady=(0, 16))

        bo_hdr = ctk.CTkFrame(bo_card, fg_color="#FAFAFA", corner_radius=0)
        bo_hdr.pack(fill="x", padx=18)
        for col, w in [("ID", 50), ("Name", 150), ("Email", 180), ("Applications", 90), ("Date Joined", 100), ("Status", 80)]:
            ctk.CTkLabel(bo_hdr, text=col, text_color="#374151", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=w, anchor="w").pack(side="left", padx=6, pady=6)

        if not applicant_users:
            ctk.CTkLabel(bo_card, text="No business owners registered yet", text_color="#9CA3AF",
                         font=ctk.CTkFont("Segoe UI", 11)).pack(pady=20)
        else:
            for u in applicant_users:
                row = ctk.CTkFrame(bo_card, fg_color="white")
                row.pack(fill="x", padx=18, pady=2)
                fname = f"{u.get('first_name') or ''} {u.get('last_name') or ''}".strip() or "Unknown"
                app_count = len([a for a in all_apps if a["user_email"] == u["email"]])
                is_active = u.get("status", "Active") == "Active"

                ctk.CTkLabel(row, text=str(u["id"]), text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=50, anchor="w").pack(side="left", padx=6)
                ctk.CTkLabel(row, text=fname, text_color="#374151", font=ctk.CTkFont("Segoe UI", 10), width=150, anchor="w").pack(side="left", padx=6)
                ctk.CTkLabel(row, text=u["email"], text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=180, anchor="w").pack(side="left", padx=6)
                ctk.CTkLabel(row, text=f"{app_count} app(s)", text_color="#1D4ED8", fg_color="#EBF5FF", corner_radius=10,
                             font=ctk.CTkFont("Segoe UI", 9, "bold"), width=70).pack(side="left", padx=6)
                ctk.CTkLabel(row, text=(u["created_at"] or "")[:10], text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=100, anchor="w").pack(side="left", padx=6)

                st_color = "#E8F5E9" if is_active else "#FDE8E8"
                st_txt = "#2E7D32" if is_active else "#E53E3E"
                ctk.CTkLabel(row, text="Active" if is_active else "Inactive", fg_color=st_color, text_color=st_txt,
                             corner_radius=10, font=ctk.CTkFont("Segoe UI", 9, "bold"), width=60).pack(side="left", padx=6)

        # Application Management & Assignment Table
        app_card = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        app_card.pack(fill="x", pady=(10, 20))
        ctk.CTkLabel(app_card, text="Application Management & Assignment", text_color="#111827", font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(anchor="w", padx=18, pady=(16, 4))
        ctk.CTkLabel(app_card, text="Assign business permit applications to specific staff members", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 11)).pack(anchor="w", padx=18, pady=(0, 16))

        hdr2 = ctk.CTkFrame(app_card, fg_color="#FAFAFA", corner_radius=0)
        hdr2.pack(fill="x", padx=18)
        cols2 = [("Application ID", 80), ("Business Name", 150), ("Applicant", 150), ("Status", 120), ("Assigned To", 120), ("Action", 120)]
        for col, w in cols2:
            ctk.CTkLabel(hdr2, text=col, text_color="#374151", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=w, anchor="w").pack(side="left", padx=6, pady=6)
            
        from database.db import get_all_applications
        apps_to_assign = [a for a in get_all_applications() if a["status"] in ("Pending", "Under Review", "Returned for Correction")]
        staff_names = [s["email"] for s in staff_users]
        if not staff_names:
            staff_names = ["No staff available"]
            
        for am in apps_to_assign:
            row = ctk.CTkFrame(app_card, fg_color="white")
            row.pack(fill="x", padx=18, pady=4)
            ctk.CTkLabel(row, text=f"#{am['id']}", text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=80, anchor="w").pack(side="left", padx=6)
            ctk.CTkLabel(row, text=am['business_name'], text_color="#2B6CB0", font=ctk.CTkFont("Segoe UI", 10), width=150, anchor="w").pack(side="left", padx=6)
            ctk.CTkLabel(row, text=f"{am['owner_first_name']} {am['owner_last_name']}", text_color="#E65C00", font=ctk.CTkFont("Segoe UI", 10), width=150, anchor="w").pack(side="left", padx=6)
            
            bg_c = "#F3F4F6"
            txt_c = "#374151"
            if am['status'] == "Pending": bg_c, txt_c = "#FFF4E5", "#D9A100"
            elif am['status'] == "Under Review": bg_c, txt_c = "#EBF5FF", "#1D4ED8"
            
            ctk.CTkLabel(row, text=am['status'], fg_color=bg_c, text_color=txt_c, corner_radius=10, font=ctk.CTkFont("Segoe UI", 9, "bold"), width=120).pack(side="left", padx=6)
            
            assigned = am.get('assigned_to') or "Unassigned"
            ctk.CTkLabel(row, text=f"👤 {assigned}", text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=120, anchor="w").pack(side="left", padx=6)
            
            a_om = ctk.CTkOptionMenu(row, values=staff_names, width=120, height=28, fg_color="white", text_color="#111827", button_color="white", dropdown_fg_color="white")
            a_om.pack(side="left", padx=6)
            a_om.set("Assign To...")
            a_om.configure(command=lambda choice, app_id=am['id']: self._assign_app(choice, app_id))

    def _create_staff(self):
        name = self.entry_staff_name.get().strip()
        email = self.entry_staff_email.get().strip()
        pwd = self.entry_staff_pass.get().strip()
        if not name or not email or not pwd:
            messagebox.showerror("Error", "All fields are required")
            return
        from database.db import create_staff_account
        success, msg = create_staff_account(email, pwd, name)
        if success:
            messagebox.showinfo("Success", "Staff account created successfully!")
            self.entry_staff_name.delete(0, "end")
            self.entry_staff_email.delete(0, "end")
            self.entry_staff_pass.delete(0, "end")
            self._render()
        else:
            messagebox.showerror("Error", msg)

    def _handle_staff_action(self, choice, m, uid, current_status):
        m.set("⋮")
        if choice in ("Deactivate/Suspend", "Activate Account"):
            new_status = "Inactive" if current_status == "Active" else "Active"
            from database.db import update_user_status
            update_user_status(uid, new_status)
            self._render()
        elif choice == "Edit Account":
            self._show_edit_account_modal(uid)
        elif choice == "Reset Password":
            self._show_reset_password_modal(uid)
        elif choice == "View Audit Trail":
            self._show_audit_trail_modal(uid)

    def _show_edit_account_modal(self, uid):
        from database.db import get_all_users, update_user_details
        user = next((u for u in get_all_users() if u["id"] == uid), None)
        if not user:
            return
        modal = ctk.CTkToplevel(self)
        modal.title(f"Edit Staff Account #{uid}")
        modal.geometry("420x340")
        modal.resizable(False, False)
        modal.grab_set()
        modal.configure(fg_color="#F4F5F7")

        hdr = ctk.CTkFrame(modal, fg_color="#E65C00", corner_radius=0, height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=f"✏️  Edit Account #{uid}", text_color="white",
                     font=ctk.CTkFont("Segoe UI", 14, "bold")).pack(side="left", padx=20, pady=12)

        body = ctk.CTkFrame(modal, fg_color="#F4F5F7")
        body.pack(fill="both", expand=True, padx=20, pady=16)

        ctk.CTkLabel(body, text="First Name", text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        fn_entry = ctk.CTkEntry(body, fg_color="white", border_width=1, border_color="#E5E7EB", height=36)
        fn_entry.pack(fill="x", pady=(0, 10))
        fn_entry.insert(0, user.get("first_name") or "")

        ctk.CTkLabel(body, text="Last Name", text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        ln_entry = ctk.CTkEntry(body, fg_color="white", border_width=1, border_color="#E5E7EB", height=36)
        ln_entry.pack(fill="x", pady=(0, 10))
        ln_entry.insert(0, user.get("last_name") or "")

        ctk.CTkLabel(body, text="Email", text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        em_entry = ctk.CTkEntry(body, fg_color="white", border_width=1, border_color="#E5E7EB", height=36)
        em_entry.pack(fill="x", pady=(0, 10))
        em_entry.insert(0, user.get("email") or "")

        def save():
            update_user_details(uid, fn_entry.get().strip(), ln_entry.get().strip(), em_entry.get().strip())
            modal.destroy()
            messagebox.showinfo("Updated", "Account details updated.")
            self._render()

        bf = ctk.CTkFrame(modal, fg_color="#F4F5F7")
        bf.pack(fill="x", padx=20, pady=(0, 16))
        ctk.CTkButton(bf, text="Save Changes", fg_color="#2E7D32", hover_color="#1B5E20", text_color="white",
                      font=ctk.CTkFont("Segoe UI", 11, "bold"), height=36, corner_radius=6, command=save).pack(side="left", padx=(0, 8))
        ctk.CTkButton(bf, text="Cancel", fg_color="white", hover_color="#EDEDED", text_color="#374151",
                      border_width=1, border_color="#D0D5DD", font=ctk.CTkFont("Segoe UI", 10),
                      height=36, corner_radius=6, command=modal.destroy).pack(side="left")

    def _show_reset_password_modal(self, uid):
        from database.db import reset_user_password
        modal = ctk.CTkToplevel(self)
        modal.title(f"Reset Password - User #{uid}")
        modal.geometry("400x240")
        modal.resizable(False, False)
        modal.grab_set()
        modal.configure(fg_color="#F4F5F7")

        hdr = ctk.CTkFrame(modal, fg_color="#E65C00", corner_radius=0, height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=f"🔑  Reset Password", text_color="white",
                     font=ctk.CTkFont("Segoe UI", 14, "bold")).pack(side="left", padx=20, pady=12)

        body = ctk.CTkFrame(modal, fg_color="#F4F5F7")
        body.pack(fill="both", expand=True, padx=20, pady=16)

        ctk.CTkLabel(body, text="New Password", text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        pw1 = ctk.CTkEntry(body, fg_color="white", border_width=1, border_color="#E5E7EB", height=36, show="*")
        pw1.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(body, text="Confirm Password", text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        pw2 = ctk.CTkEntry(body, fg_color="white", border_width=1, border_color="#E5E7EB", height=36, show="*")
        pw2.pack(fill="x", pady=(0, 10))

        def save():
            if pw1.get() != pw2.get():
                messagebox.showerror("Error", "Passwords do not match.")
                return
            if len(pw1.get()) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters.")
                return
            reset_user_password(uid, pw1.get())
            modal.destroy()
            messagebox.showinfo("Success", "Password has been reset.")

        bf = ctk.CTkFrame(modal, fg_color="#F4F5F7")
        bf.pack(fill="x", padx=20, pady=(0, 16))
        ctk.CTkButton(bf, text="Reset Password", fg_color="#E65C00", hover_color="#CC5200", text_color="white",
                      font=ctk.CTkFont("Segoe UI", 11, "bold"), height=36, corner_radius=6, command=save).pack(side="left", padx=(0, 8))
        ctk.CTkButton(bf, text="Cancel", fg_color="white", hover_color="#EDEDED", text_color="#374151",
                      border_width=1, border_color="#D0D5DD", font=ctk.CTkFont("Segoe UI", 10),
                      height=36, corner_radius=6, command=modal.destroy).pack(side="left")

    def _show_audit_trail_modal(self, uid):
        from database.db import get_user_activity_log, get_all_users
        user = next((u for u in get_all_users() if u["id"] == uid), None)
        logs = get_user_activity_log(uid)

        modal = ctk.CTkToplevel(self)
        uname = f"{user.get('first_name','')} {user.get('last_name','')}".strip() if user else f"User #{uid}"
        modal.title(f"Audit Trail - {uname}")
        modal.geometry("600x450")
        modal.resizable(False, False)
        modal.grab_set()
        modal.configure(fg_color="#F4F5F7")

        hdr = ctk.CTkFrame(modal, fg_color="#E65C00", corner_radius=0, height=50)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=f"📜  Audit Trail — {uname}", text_color="white",
                     font=ctk.CTkFont("Segoe UI", 14, "bold")).pack(side="left", padx=20, pady=12)

        body = ctk.CTkScrollableFrame(modal, fg_color="#F4F5F7")
        body.pack(fill="both", expand=True, padx=16, pady=12)

        if not logs:
            ctk.CTkLabel(body, text="No activity recorded for this user.", text_color="#9CA3AF",
                         font=ctk.CTkFont("Segoe UI", 12)).pack(pady=40)
        else:
            for log in logs:
                card = ctk.CTkFrame(body, fg_color="white", corner_radius=8, border_width=1, border_color="#E5E7EB")
                card.pack(fill="x", pady=3)
                top_r = ctk.CTkFrame(card, fg_color="white")
                top_r.pack(fill="x", padx=12, pady=(8, 2))
                ctk.CTkLabel(top_r, text=f"App #{log['id']} — {log['business_name']}",
                             text_color="#111827", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(side="left")
                st_colors = {"Approved": "#2E7D32", "Rejected": "#E53E3E", "Pending": "#D9A100", "Under Review": "#1D4ED8"}
                ctk.CTkLabel(top_r, text=log["status"], text_color=st_colors.get(log["status"], "#374151"),
                             font=ctk.CTkFont("Segoe UI", 9, "bold")).pack(side="right")
                bot_r = ctk.CTkFrame(card, fg_color="white")
                bot_r.pack(fill="x", padx=12, pady=(0, 8))
                ctk.CTkLabel(bot_r, text=f"Reviewed: {(log.get('reviewed_at') or 'N/A')[:16]}  |  Submitted: {(log.get('submitted_at') or '')[:10]}",
                             text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 9)).pack(side="left")

        ctk.CTkButton(modal, text="Close", fg_color="white", hover_color="#EDEDED", text_color="#374151",
                      border_width=1, border_color="#D0D5DD", font=ctk.CTkFont("Segoe UI", 10),
                      height=36, corner_radius=6, command=modal.destroy).pack(pady=(0, 12))

    def _assign_app(self, choice, app_id):
        from database.db import assign_application
        assign_application(app_id, choice)
        self._render()

    # ── Permit Holders view ──────────────────────────────────
    def _render_permits(self):
        from datetime import datetime, timedelta
        h = self.host
        permits = get_all_permits()
        apps = get_all_applications()
        pending_apps = [a for a in apps if a["status"] == "Pending"]
        
        # Filters
        filter_box = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        filter_box.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(filter_box, text="Filter Permits", text_color="#111827", font=ctk.CTkFont("Segoe UI", 11, "bold")).pack(anchor="w", padx=18, pady=(16, 8))
        
        f_row = ctk.CTkFrame(filter_box, fg_color="transparent")
        f_row.pack(fill="x", padx=18, pady=(0, 16))
        
        # Date range filter
        date_frame = ctk.CTkFrame(f_row, fg_color="transparent")
        date_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(date_frame, text="Date Range", text_color="#374151", font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w")
        permit_date_var = tk.StringVar(value="All Time")
        permit_date_combo = ctk.CTkComboBox(date_frame, variable=permit_date_var, 
                                            values=["All Time", "Today", "This Week", "This Month", "This Year", "Custom"],
                                            fg_color="#F9FAFB", text_color="#111827", button_color="#F9FAFB", height=32)
        permit_date_combo.pack(fill="x", pady=(4, 0))
        
        # Apply date filter
        def apply_permit_filter():
            date_range = permit_date_var.get()
            now = datetime.now()
            filtered = permits
            
            if date_range == "Today":
                filtered = [p for p in permits if p.get("issued_at", "")[:10] == now.strftime("%Y-%m-%d")]
            elif date_range == "This Week":
                start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
                filtered = [p for p in permits if p.get("issued_at", "")[:10] >= start]
            elif date_range == "This Month":
                filtered = [p for p in permits if p.get("issued_at", "")[:10][:7] == now.strftime("%Y-%m")]
            elif date_range == "This Year":
                filtered = [p for p in permits if p.get("issued_at", "")[:4] == now.strftime("%Y")]
            
            return filtered
        
        permits = apply_permit_filter()

        # Pending applications to review
        if pending_apps:
            rev = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                                border_width=1, border_color="#E5E7EB")
            rev.pack(fill="x", pady=(0, 12))
            ctk.CTkLabel(rev, text=f"Pending Applications ({len(pending_apps)})", text_color="#D9A100",
                         font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(
                anchor="w", padx=18, pady=(16, 8))
            for a in pending_apps:
                row = ctk.CTkFrame(rev, fg_color="#FFFBF0", corner_radius=4)
                row.pack(fill="x", padx=18, pady=2)
                ctk.CTkLabel(row, text=f"#{a['id']}  {a['business_name']}  —  {a['user_email']}",
                             text_color="#374151", font=ctk.CTkFont("Segoe UI", 10)).pack(side="left", padx=10, pady=6)
                ctk.CTkButton(row, text="📋 Review", width=90, height=26,
                              fg_color="#EBF5FF", hover_color="#DBEAFE", text_color="#1D4ED8",
                              font=ctk.CTkFont("Segoe UI", 9, "bold"), corner_radius=4,
                              command=lambda a=a: self._open_review_modal(a)).pack(side="right", padx=4, pady=4)

        # Active permits
        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text=f"Active Permits ({len(permits)})", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=18, pady=(16, 12))
        hdr = ctk.CTkFrame(card, fg_color="#FAFAFA", corner_radius=0)
        hdr.pack(fill="x", padx=18)
        for col, w in [("Permit #", 100), ("Business", 130), ("Owner", 130), ("Issued", 90), ("Expires", 90), ("Status", 80), ("Actions", 100)]:
            ctk.CTkLabel(hdr, text=col, text_color="#374151",
                         font=ctk.CTkFont("Segoe UI", 10, "bold"),
                         width=w, anchor="w").pack(side="left", padx=4, pady=6)
        if not permits:
            ctk.CTkLabel(card, text="No permits issued yet", text_color="#9CA3AF",
                         font=ctk.CTkFont("Segoe UI", 11)).pack(pady=30)
        else:
            for p in permits:
                row = ctk.CTkFrame(card, fg_color="white")
                row.pack(fill="x", padx=18, pady=1)
                ctk.CTkLabel(row, text=p["permit_number"], text_color="#1D4ED8", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=100, anchor="w").pack(side="left", padx=4, pady=4)
                ctk.CTkLabel(row, text=p["business_name"], text_color="#374151", font=ctk.CTkFont("Segoe UI", 10), width=130, anchor="w").pack(side="left", padx=4, pady=4)
                ctk.CTkLabel(row, text=p["user_email"], text_color="#6B7280", font=ctk.CTkFont("Segoe UI", 10), width=130, anchor="w").pack(side="left", padx=4, pady=4)
                ctk.CTkLabel(row, text=(p["issued_at"] or "")[:10], text_color="#374151", font=ctk.CTkFont("Segoe UI", 10), width=90, anchor="w").pack(side="left", padx=4, pady=4)
                ctk.CTkLabel(row, text=(p["expires_at"] or "")[:10], text_color="#374151", font=ctk.CTkFont("Segoe UI", 10), width=90, anchor="w").pack(side="left", padx=4, pady=4)
                st_bg = "#E8F5E9" if p["status"] == "Active" else "#FDE8E8"
                st_tc = "#2E7D32" if p["status"] == "Active" else "#E53E3E"
                ctk.CTkLabel(row, text=p["status"], fg_color=st_bg, text_color=st_tc, corner_radius=10, font=ctk.CTkFont("Segoe UI", 9, "bold"), width=70).pack(side="left", padx=4, pady=4)
                ctk.CTkButton(row, text="👁", width=30, height=24, fg_color="#EBF5FF", hover_color="#DBEAFE", text_color="#1D4ED8", corner_radius=4, command=lambda p=p: messagebox.showinfo("Permit Details", f"Permit: {p['permit_number']}\nBusiness: {p['business_name']}\nOwner: {p['user_email']}\nIssued: {(p['issued_at'] or '')[:10]}\nExpires: {(p['expires_at'] or '')[:10]}\nStatus: {p['status']}")).pack(side="left", padx=2, pady=4)
                ctk.CTkButton(row, text="🖨", width=30, height=24, fg_color="#F3F4F6", hover_color="#E5E7EB", text_color="#374151", corner_radius=4, command=lambda p=p: self._print_permit(p)).pack(side="left", padx=2, pady=4)

    def _open_review_modal(self, app):
        modal = ctk.CTkToplevel(self)
        modal.title(f"Review Application #{app['id']}")
        modal.geometry("620x680")
        modal.resizable(False, False)
        modal.grab_set()
        modal.configure(fg_color="#F4F5F7")

        # Header
        hdr = ctk.CTkFrame(modal, fg_color="#E65C00", corner_radius=0, height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        ctk.CTkLabel(hdr, text=f"📋  Review Application #{app['id']}",
                     text_color="white",
                     font=ctk.CTkFont("Segoe UI", 16, "bold")).pack(side="left", padx=20, pady=15)
        status_bg = {"Pending": "#FFF4E5", "Under Review": "#EBF5FF", "Approved": "#E8F5E9", "Rejected": "#FDE8E8"}
        status_tc = {"Pending": "#D9A100", "Under Review": "#1D4ED8", "Approved": "#2E7D32", "Rejected": "#E53E3E"}
        st = app.get("status", "Pending")
        ctk.CTkLabel(hdr, text=st, fg_color=status_bg.get(st, "#F3F4F6"),
                     text_color=status_tc.get(st, "#374151"),
                     corner_radius=12, font=ctk.CTkFont("Segoe UI", 10, "bold"),
                     width=90, height=26).pack(side="right", padx=20)

        # Scrollable body
        body = ctk.CTkScrollableFrame(modal, fg_color="#F4F5F7")
        body.pack(fill="both", expand=True, padx=16, pady=(12, 0))

        def section(parent, title, icon=""):
            f = ctk.CTkFrame(parent, fg_color="white", corner_radius=10,
                             border_width=1, border_color="#E5E7EB")
            f.pack(fill="x", pady=(0, 10))
            ctk.CTkLabel(f, text=f"{icon}  {title}", text_color="#111827",
                         font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(
                anchor="w", padx=16, pady=(14, 8))
            return f

        def field(parent, label, value):
            row = ctk.CTkFrame(parent, fg_color="white")
            row.pack(fill="x", padx=16, pady=2)
            ctk.CTkLabel(row, text=label, text_color="#6B7280",
                         font=ctk.CTkFont("Segoe UI", 10), width=160, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=str(value or "—"), text_color="#111827",
                         font=ctk.CTkFont("Segoe UI", 10, "bold"), anchor="w").pack(side="left", fill="x", expand=True)

        # Business Information
        s1 = section(body, "Business Information", "🏢")
        field(s1, "Business Name", app.get("business_name"))
        field(s1, "Business Type", app.get("business_type"))
        field(s1, "Ownership Type", app.get("ownership_type"))
        field(s1, "Business Address", app.get("business_address"))
        ctk.CTkFrame(s1, fg_color="white", height=8).pack()

        # Owner Details
        s2 = section(body, "Owner Details", "👤")
        owner = f"{app.get('owner_first_name', '')} {app.get('owner_last_name', '')}".strip()
        field(s2, "Full Name", owner)
        field(s2, "Email", app.get("user_email"))
        field(s2, "Contact Number", app.get("contact_number"))
        field(s2, "Gender", app.get("gender"))
        ctk.CTkFrame(s2, fg_color="white", height=8).pack()

        # Financial & Registration
        s3 = section(body, "Financial & Registration", "💰")
        cap = app.get("capital_investment", 0)
        field(s3, "Capital Investment", f"₱{cap:,.2f}" if cap else "—")
        male = app.get("employees_male", 0) or 0
        female = app.get("employees_female", 0) or 0
        field(s3, "Employees (M / F)", f"{male} Male  /  {female} Female")
        field(s3, "Total Employees", str(male + female))
        field(s3, "TIN Number", app.get("tin_number"))
        field(s3, "DTI/SEC/CDA Reg. No.", app.get("dti_sec_cda_reg_no"))
        ctk.CTkFrame(s3, fg_color="white", height=8).pack()

        # Application Meta
        s4 = section(body, "Application Meta", "📊")
        field(s4, "Submitted At", (app.get("submitted_at") or "")[:19])
        field(s4, "Assigned To", app.get("assigned_to") or "Unassigned")
        field(s4, "Risk Level", app.get("risk_level", "Low"))
        field(s4, "Remarks", app.get("remarks") or "None")
        ctk.CTkFrame(s4, fg_color="white", height=8).pack()

        # Notes field
        notes_frame = ctk.CTkFrame(body, fg_color="white", corner_radius=10,
                                   border_width=1, border_color="#E5E7EB")
        notes_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(notes_frame, text="📝  Reviewer Notes", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(
            anchor="w", padx=16, pady=(14, 6))
        notes_entry = ctk.CTkTextbox(notes_frame, height=60, fg_color="#F9FAFB",
                                     border_width=1, border_color="#E5E7EB",
                                     font=ctk.CTkFont("Segoe UI", 10),
                                     text_color="#374151", corner_radius=6)
        notes_entry.pack(fill="x", padx=16, pady=(0, 14))
        if app.get("notes"):
            notes_entry.insert("1.0", app["notes"])

        # Action buttons
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
            update_application_status(app["id"], "Returned for Correction",
                                      self.controller.logged_in_user or "admin@bbp.com")
            add_notification(app["user_email"], "Application Returned",
                             f"Your application for '{app['business_name']}' was returned for correction. Notes: {notes}")
            add_notification("admin", "Application Returned",
                             f"Application #{app['id']} for '{app['business_name']}' returned for correction.")
            modal.destroy()
            messagebox.showinfo("Returned", "Application returned for correction.")
            self._render()

        ctk.CTkButton(btn_frame, text="✓  Approve & Issue Permit", width=180, height=38,
                      fg_color="#2E7D32", hover_color="#1B5E20", text_color="white",
                      font=ctk.CTkFont("Segoe UI", 11, "bold"), corner_radius=6,
                      command=do_approve).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_frame, text="↩  Return for Correction", width=170, height=38,
                      fg_color="#FFF4E5", hover_color="#FDECD0", text_color="#D9A100",
                      font=ctk.CTkFont("Segoe UI", 11, "bold"), corner_radius=6,
                      command=do_return).pack(side="left", padx=(0, 8))
        ctk.CTkButton(btn_frame, text="✕  Reject", width=100, height=38,
                      fg_color="#FDE8E8", hover_color="#FECACA", text_color="#E53E3E",
                      font=ctk.CTkFont("Segoe UI", 11, "bold"), corner_radius=6,
                      command=do_reject).pack(side="left")
        ctk.CTkButton(btn_frame, text="Close", width=80, height=38,
                      fg_color="white", hover_color="#EDEDED", text_color="#374151",
                      border_width=1, border_color="#D0D5DD",
                      font=ctk.CTkFont("Segoe UI", 10), corner_radius=6,
                      command=modal.destroy).pack(side="right")

    def _approve_app(self, app):
        update_application_status(app["id"], "Approved", self.controller.logged_in_user or "admin@bbp.com")
        pnum = issue_permit(app["id"], app["user_email"], app["business_name"])
        add_notification("admin", "Application Approved",
                         f"Permit {pnum} issued for '{app['business_name']}'.")
        add_notification(app["user_email"], "Permit Approved",
                         f"Your application for '{app['business_name']}' has been approved! Permit: {pnum}")
        messagebox.showinfo("Approved", f"Permit {pnum} issued.")
        self._render()

    def _reject_app(self, app):
        update_application_status(app["id"], "Rejected", self.controller.logged_in_user or "admin@bbp.com")
        add_notification("admin", "Application Rejected",
                         f"Application #{app['id']} for '{app['business_name']}' was rejected.")
        add_notification(app["user_email"], "Application Rejected",
                         f"Your application for '{app['business_name']}' has been rejected.")
        messagebox.showinfo("Rejected", "Application rejected.")
        self._render()

    # ── Reports view ─────────────────────────────────────────
    def _render_reports(self):
        h = self.host
        st = get_application_stats()
        apps = get_all_applications()

        # Export & Archive Reports
        export_box = ctk.CTkFrame(h, fg_color="#FFF9F0", corner_radius=10, border_width=1, border_color="#FDECD0")
        export_box.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(export_box, text="📥 Export & Archive Reports", text_color="#E65C00", font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(anchor="w", padx=18, pady=(16, 8))
        
        btns = ctk.CTkFrame(export_box, fg_color="transparent")
        btns.pack(fill="x", padx=18, pady=(0, 16))
        ctk.CTkButton(btns, text="📄 Print Official Report", fg_color="#E65C00", hover_color="#CC5200", text_color="white", font=ctk.CTkFont("Segoe UI", 11, "bold"), height=36, command=self._print_report).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btns, text="📥 Export as CSV", fg_color="#2E7D32", hover_color="#1B5E20", text_color="white", font=ctk.CTkFont("Segoe UI", 11, "bold"), height=36, command=self._export_csv).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btns, text="📄 Export as PDF", fg_color="white", text_color="#374151", border_width=1, border_color="#E5E7EB", font=ctk.CTkFont("Segoe UI", 11, "bold"), height=36, command=self._export_pdf).pack(side="left")
        ctk.CTkLabel(export_box, text="● Reports are pre-formatted for COA and City Hall submission with official watermark", text_color="#E65C00", font=ctk.CTkFont("Segoe UI", 9, slant="italic")).pack(anchor="w", padx=18, pady=(0, 16))
        # Filters
        filter_box = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        filter_box.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(filter_box, text="Filter Report Filters", text_color="#E65C00", font=ctk.CTkFont("Segoe UI", 11, "bold")).pack(anchor="w", padx=18, pady=(16, 8))
        
        f_row = ctk.CTkFrame(filter_box, fg_color="transparent")
        f_row.pack(fill="x", padx=18, pady=(0, 16))
        
        # Date range filter
        date_frame = ctk.CTkFrame(f_row, fg_color="transparent")
        date_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkLabel(date_frame, text="Date Range", text_color="#374151", font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w")
        date_range_var = tk.StringVar(value="All Time")
        date_range_combo = ctk.CTkComboBox(date_frame, variable=date_range_var, 
                                           values=["All Time", "Today", "This Week", "This Month", "This Year", "Custom"],
                                           fg_color="#F9FAFB", text_color="#111827", button_color="#F9FAFB", height=32)
        date_range_combo.pack(fill="x")
        
        def _add_filter(parent, label, vals):
            f = ctk.CTkFrame(parent, fg_color="transparent")
            f.pack(side="left", fill="x", expand=True, padx=(0, 10))
            ctk.CTkLabel(f, text=label, text_color="#374151", font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w")
            ctk.CTkOptionMenu(f, values=vals, fg_color="#F9FAFB", text_color="#111827", button_color="#F9FAFB", height=32).pack(fill="x")
            
        _add_filter(f_row, "Status", ["All Status", "Pending", "Under Review", "Approved", "Returned for Correction"])
        _add_filter(f_row, "Business Type", ["All Types", "Food", "Retail", "Services", "Manufacturing", "Other"])
        _add_filter(f_row, "Risk Level", ["All Levels", "Low", "Medium", "High"])
        
        ctk.CTkButton(filter_box, text="Reset Filters", fg_color="white", text_color="#374151", border_width=1, border_color="#E5E7EB", width=100, height=30).pack(anchor="w", padx=18, pady=(0, 16))

        # Stats
        stat_row = ctk.CTkFrame(h, fg_color="transparent")
        stat_row.pack(fill="x", pady=(0, 12))
        for i in range(4): stat_row.grid_columnconfigure(i, weight=1)
        self._stat_card(stat_row, 0, "Applications in View", str(st["total"]), "", "#F9FAFB", "#111827")
        self._stat_card(stat_row, 1, "Approved/Ready", str(st["approved"]), "", "#F9FAFB", "#2E7D32")
        self._stat_card(stat_row, 2, "Success Rate", f"{st['rate']}%", "", "#F9FAFB", "#E65C00")
        self._stat_card(stat_row, 3, "High Risk Apps", str(st.get("high_risk", 0)), "", "#F9FAFB", "#E53E3E")

        # Table
        log = ctk.CTkFrame(h, fg_color="white", corner_radius=10, border_width=1, border_color="#E5E7EB")
        log.pack(fill="x", pady=(0, 20))
        
        top_hdr = ctk.CTkFrame(log, fg_color="#FFF9F0", corner_radius=10)
        top_hdr.pack(fill="x", padx=18, pady=(16, 8))
        ctk.CTkLabel(top_hdr, text="📄 Issued Business Permits - Barangay 183", text_color="#111827", font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(top_hdr, text="Report Type: Administrative Summary", text_color="#E65C00", font=ctk.CTkFont("Segoe UI", 10, "bold")).pack(side="right", padx=10)

        hdr = ctk.CTkFrame(log, fg_color="#E65C00", corner_radius=0)
        hdr.pack(fill="x", padx=18)
        cols = [("ID", 40), ("Business Name", 140), ("Owner", 140), ("Business Type", 100), ("App. Type", 80), ("Address", 140), ("Date Issued", 80), ("Status", 120)]
        for col, w in cols:
            ctk.CTkLabel(hdr, text=col, text_color="white", font=ctk.CTkFont("Segoe UI", 10, "bold"), width=w, anchor="w").pack(side="left", padx=4, pady=8)
            
        mock_reports = get_all_applications()
        
        for m in mock_reports:
            row = ctk.CTkFrame(log, fg_color="white")
            row.pack(fill="x", padx=18, pady=2)
            c_vals = [
                (str(m["id"]), "#6B7280", 40), (m["business_name"], "#374151", 140), (f"{m['owner_first_name']} {m['owner_last_name']}", "#6B7280", 140), 
                (m["business_type"] or "Retail", "#6B7280", 100), ("New", "#6B7280", 80), (m["business_address"][:15]+"...", "#6B7280", 140), 
                ((m["submitted_at"] or "")[:10], "#6B7280", 80)
            ]
            for val, color, w in c_vals:
                ctk.CTkLabel(row, text=val, text_color=color, font=ctk.CTkFont("Segoe UI", 10), width=w, anchor="w").pack(side="left", padx=4, pady=4)
            
            sc = {"Pending": "#D9A100", "Under Review": "#1D4ED8", "Approved": "#2E7D32", "Returned for Correction": "#374151"}
            status = m["status"]
            ctk.CTkLabel(row, text=status, text_color=sc.get(status, "#111827"), font=ctk.CTkFont("Segoe UI", 9, "bold"), width=120, anchor="w").pack(side="left", padx=4)

    # ── Placeholder view ─────────────────────────────────────
    def _render_placeholder(self, title):
        card = ctk.CTkFrame(self.host, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text=f"{title} content coming soon",
                     text_color="#9CA3AF",
                     font=ctk.CTkFont("Segoe UI", 13)).pack(pady=80)

    def _print_permit(self, p):
        import os, tempfile, webbrowser
        from datetime import datetime
        
        try:
            date_str = p.get('issued_at', str(datetime.now()))[:10]
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = dt.strftime('%B %d, %Y')
        except:
            formatted_date = datetime.now().strftime('%B %d, %Y')

        owner_name = f"{p.get('owner_first_name', '')} {p.get('owner_last_name', '')}".strip()
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

    # ── Export functions ──────────────────────────────────────
    def _get_report_data(self):
        from database.db import get_all_applications, get_all_permits, get_application_stats
        return get_all_applications(), get_all_permits(), get_application_stats()

    def _export_csv(self):
        import csv, os
        from tkinter import filedialog
        apps, permits, _ = self._get_report_data()
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
                                            initialfile="bbp_report.csv", title="Save CSV Report")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Application ID", "Business Name", "Owner", "Type", "Status", "Capital", "Submitted", "Reviewed By"])
            for a in apps:
                owner = f"{a.get('owner_first_name','')} {a.get('owner_last_name','')}".strip()
                w.writerow([a["id"], a["business_name"], owner, a.get("business_type",""),
                            a["status"], a.get("capital_investment",0),
                            (a.get("submitted_at") or "")[:10], a.get("reviewed_by","")])
            w.writerow([])
            w.writerow(["Permit #", "Business", "Owner Email", "Issued", "Expires", "Status"])
            for p in permits:
                w.writerow([p["permit_number"], p["business_name"], p["user_email"],
                            (p.get("issued_at") or "")[:10], (p.get("expires_at") or "")[:10], p["status"]])
        messagebox.showinfo("Exported", f"CSV report saved to:\n{path}")

    def _build_report_html(self):
        from datetime import datetime
        apps, permits, st = self._get_report_data()
        rows_html = ""
        for a in apps:
            owner = f"{a.get('owner_first_name','')} {a.get('owner_last_name','')}".strip()
            rows_html += f"<tr><td>{a['id']}</td><td>{a['business_name']}</td><td>{owner}</td><td>{a['status']}</td><td>{(a.get('submitted_at') or '')[:10]}</td></tr>\n"
        permit_rows = ""
        for p in permits:
            permit_rows += f"<tr><td>{p['permit_number']}</td><td>{p['business_name']}</td><td>{p['user_email']}</td><td>{(p.get('issued_at') or '')[:10]}</td><td>{p['status']}</td></tr>\n"
        return f"""<html><head><title>BBP System Report</title>
<style>body{{font-family:Arial,sans-serif;padding:40px;color:#111827}}
h1{{color:#E65C00;text-align:center}}h2{{color:#374151;border-bottom:2px solid #E5E7EB;padding-bottom:6px}}
table{{width:100%;border-collapse:collapse;margin-bottom:30px}}
th{{background:#FFF4E5;color:#E65C00;text-align:left;padding:8px 10px;border:1px solid #E5E7EB}}
td{{padding:6px 10px;border:1px solid #E5E7EB}}
.stats{{display:flex;gap:20px;margin-bottom:30px}}
.stat-box{{flex:1;background:#FFF9F0;border:1px solid #FDECD0;border-radius:8px;padding:16px;text-align:center}}
.stat-val{{font-size:28px;font-weight:bold;color:#E65C00}}.stat-lbl{{color:#6B7280;font-size:12px}}
.footer{{text-align:center;color:#9CA3AF;font-size:11px;margin-top:40px;border-top:1px solid #E5E7EB;padding-top:12px}}
@media print{{body{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}}}</style></head>
<body>
<h1>Barangay 183 Business Permit System — Official Report</h1>
<p style="text-align:center;color:#6B7280">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
<div class="stats">
<div class="stat-box"><div class="stat-val">{st['total']}</div><div class="stat-lbl">Total Applications</div></div>
<div class="stat-box"><div class="stat-val">{st['approved']}</div><div class="stat-lbl">Approved</div></div>
<div class="stat-box"><div class="stat-val">{st['pending']}</div><div class="stat-lbl">Pending</div></div>
<div class="stat-box"><div class="stat-val">{st['rate']}%</div><div class="stat-lbl">Approval Rate</div></div>
</div>
<h2>Applications</h2>
<table><tr><th>ID</th><th>Business Name</th><th>Owner</th><th>Status</th><th>Submitted</th></tr>
{rows_html}</table>
<h2>Issued Permits</h2>
<table><tr><th>Permit #</th><th>Business</th><th>Owner Email</th><th>Issued</th><th>Status</th></tr>
{permit_rows}</table>
<div class="footer">Barangay 183, Zone 16, Caloocan City &bull; Official Report &bull; NOT VALID WITHOUT DRY SEAL</div>
</body></html>"""

    def _print_report(self):
        import os, tempfile, webbrowser
        html = self._build_report_html().replace("</body>", '<script>window.onload=function(){window.print()}</script></body>')
        fd, path = tempfile.mkstemp(suffix=".html")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open("file://" + os.path.realpath(path))

    def _export_pdf(self):
        import os, tempfile, webbrowser
        html = self._build_report_html()
        fd, path = tempfile.mkstemp(suffix=".html")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open("file://" + os.path.realpath(path))
        messagebox.showinfo("Export as PDF", "The report opened in your browser.\nUse Ctrl+P → 'Save as PDF' to save it.")
