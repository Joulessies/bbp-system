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
            tk.Label(brand, image=self._logo, bg="#F9F9F9").pack(side="left", padx=(0, 8))
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
        self.controller.show_frame("LandingFrame")

    # ── Main content ─────────────────────────────────────────
    def _build_main_content(self):
        main = ctk.CTkFrame(self, fg_color="#F4F5F7", corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)

        # top bar
        top = ctk.CTkFrame(main, fg_color="#F4F5F7")
        top.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 0))
        self.top_title = ctk.CTkLabel(top, text="Admin Dashboard",
                                      text_color="#101828",
                                      font=ctk.CTkFont("Segoe UI", 26, "bold"))
        self.top_title.pack(anchor="w")
        self.top_sub = ctk.CTkLabel(top, text="Overview of Barangay 183 Business Permit System",
                                    text_color="#6B7280",
                                    font=ctk.CTkFont("Segoe UI", 11))
        self.top_sub.pack(anchor="w", pady=(2, 0))

        # scrollable host
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
        self._stat_card(row1, 0, "Total Applications", str(st["total"]), "📋", "#FFF4E5", "#F05A00", "📈 Live data from system")
        self._stat_card(row1, 1, "Pending", str(st["pending"]), "⏳", "#FFF9E5", "#D9A100", "Awaiting review")
        self._stat_card(row1, 2, "Approved", str(st["approved"]), "✅", "#E8F5E9", "#2E7D32", rate_str)
        self._stat_card(row1, 3, "Processing Time", "0 days", "📊", "#F3E8FF", "#7C3AED", "📈 Real time average")

        row2 = ctk.CTkFrame(h, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 12))
        row2.grid_columnconfigure(0, weight=1)
        self._stat_card(row2, 0, "Pending Renewals", str(st["renewal"]), "🔄", "#FDE8E8", "#E53E3E", "⊙ Active renewals")

        row3 = ctk.CTkFrame(h, fg_color="transparent")
        row3.pack(fill="x", pady=(0, 12))
        row3.grid_columnconfigure(0, weight=1)
        row3.grid_columnconfigure(1, weight=1)
        self._chart_card(row3, 0, "Monthly Applications Trend")
        self._chart_card(row3, 1, "Applications by Business Type")

        self._chart_card_full(h, "Application Status Breakdown")

        row5 = ctk.CTkFrame(h, fg_color="transparent")
        row5.pack(fill="x", pady=(0, 12))
        for i in range(4):
            row5.grid_columnconfigure(i, weight=1)
        self._mini_stat(row5, 0, "Active Business Owners", str(st["owners"]), "👥", "#FFF4E5", "#111827")
        self._mini_stat(row5, 1, "Business Diversity", f"{st['types']} Types", "📊", "#F3E8FF", "#7C3AED")
        self._mini_stat(row5, 2, "High-Risk Detection", str(st["high_risk"]), "⚠️", "#FDE8E8", "#E53E3E")
        comp = f"{st['rate']}%"
        self._mini_stat(row5, 3, "Completion Rate", comp, "✅", "#E8F5E9", "#2E7D32")

        self._staff_leaderboard(h)
        self._contact_footer(h)

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

    def _mini_stat(self, parent, col, title, value, icon, icon_bg, val_color):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.grid(row=0, column=col, sticky="nsew", padx=4, pady=2)
        inner = ctk.CTkFrame(card, fg_color="white")
        inner.pack(padx=14, pady=14, fill="x")
        ctk.CTkLabel(inner, text=icon, fg_color=icon_bg, width=36, height=36,
                     corner_radius=10, font=ctk.CTkFont(size=16)).pack(side="left", padx=(0, 10))
        txt = ctk.CTkFrame(inner, fg_color="white")
        txt.pack(side="left")
        ctk.CTkLabel(txt, text=title, text_color="#6B7280",
                     font=ctk.CTkFont("Segoe UI", 10)).pack(anchor="w")
        ctk.CTkLabel(txt, text=value, text_color=val_color,
                     font=ctk.CTkFont("Segoe UI", 16, "bold")).pack(anchor="w")

    def _chart_card(self, parent, col, title):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.grid(row=0, column=col, sticky="nsew", padx=4, pady=2)
        ctk.CTkLabel(card, text=title, text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 12, "bold")).pack(
            anchor="w", padx=18, pady=(16, 0))
        ctk.CTkLabel(card, text="No data available", text_color="#9CA3AF",
                     font=ctk.CTkFont("Segoe UI", 11)).pack(pady=50)

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

        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text=f"Registered Users ({len(users)})", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=18, pady=(16, 12))

        hdr = ctk.CTkFrame(card, fg_color="#FAFAFA", corner_radius=0)
        hdr.pack(fill="x", padx=18)
        for col in ["ID", "Email", "Role", "Created", "Actions"]:
            w = 60 if col == "ID" else 200 if col == "Email" else 100
            ctk.CTkLabel(hdr, text=col, text_color="#374151",
                         font=ctk.CTkFont("Segoe UI", 10, "bold"),
                         width=w, anchor="w").pack(side="left", padx=6, pady=6)

        if not users:
            ctk.CTkLabel(card, text="No users registered", text_color="#9CA3AF",
                         font=ctk.CTkFont("Segoe UI", 11)).pack(pady=30)
        else:
            for u in users:
                row = ctk.CTkFrame(card, fg_color="white")
                row.pack(fill="x", padx=18, pady=1)
                ctk.CTkLabel(row, text=str(u["id"]), text_color="#374151",
                             font=ctk.CTkFont("Segoe UI", 10), width=60, anchor="w").pack(side="left", padx=6)
                ctk.CTkLabel(row, text=u["email"], text_color="#374151",
                             font=ctk.CTkFont("Segoe UI", 10), width=200, anchor="w").pack(side="left", padx=6)
                ctk.CTkLabel(row, text=u.get("role", "user"), text_color="#6B7280",
                             font=ctk.CTkFont("Segoe UI", 10), width=100, anchor="w").pack(side="left", padx=6)
                ctk.CTkLabel(row, text=(u.get("created_at") or "")[:10], text_color="#9CA3AF",
                             font=ctk.CTkFont("Segoe UI", 10), width=100, anchor="w").pack(side="left", padx=6)
                if u["email"] != "admin@bbp.com":
                    ctk.CTkButton(row, text="Delete", width=60, height=26,
                                  fg_color="#FDE8E8", hover_color="#FECACA", text_color="#E53E3E",
                                  font=ctk.CTkFont("Segoe UI", 9), corner_radius=4,
                                  command=lambda uid=u["id"]: self._delete_user(uid)).pack(side="left", padx=4)

    def _delete_user(self, uid):
        if messagebox.askyesno("Confirm", "Delete this user?"):
            delete_user(uid)
            add_notification("admin", "User Deleted", f"User #{uid} was removed from the system.")
            self._render()

    # ── Permit Holders view ──────────────────────────────────
    def _render_permits(self):
        h = self.host
        permits = get_all_permits()
        apps = get_all_applications()
        pending_apps = [a for a in apps if a["status"] == "Pending"]

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
                ctk.CTkButton(row, text="Approve", width=70, height=26,
                              fg_color="#E8F5E9", hover_color="#C8E6C9", text_color="#2E7D32",
                              font=ctk.CTkFont("Segoe UI", 9), corner_radius=4,
                              command=lambda a=a: self._approve_app(a)).pack(side="right", padx=4, pady=4)
                ctk.CTkButton(row, text="Reject", width=70, height=26,
                              fg_color="#FDE8E8", hover_color="#FECACA", text_color="#E53E3E",
                              font=ctk.CTkFont("Segoe UI", 9), corner_radius=4,
                              command=lambda a=a: self._reject_app(a)).pack(side="right", padx=4, pady=4)

        # Active permits
        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text=f"Active Permits ({len(permits)})", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=18, pady=(16, 12))
        hdr = ctk.CTkFrame(card, fg_color="#FAFAFA", corner_radius=0)
        hdr.pack(fill="x", padx=18)
        for col in ["Permit #", "Business", "Owner", "Issued", "Expires", "Status"]:
            ctk.CTkLabel(hdr, text=col, text_color="#374151",
                         font=ctk.CTkFont("Segoe UI", 10, "bold"),
                         width=120, anchor="w").pack(side="left", padx=4, pady=6)
        if not permits:
            ctk.CTkLabel(card, text="No permits issued yet", text_color="#9CA3AF",
                         font=ctk.CTkFont("Segoe UI", 11)).pack(pady=30)
        else:
            for p in permits:
                row = ctk.CTkFrame(card, fg_color="white")
                row.pack(fill="x", padx=18, pady=1)
                for val in [p["permit_number"], p["business_name"], p["user_email"],
                            (p["issued_at"] or "")[:10], (p["expires_at"] or "")[:10], p["status"]]:
                    ctk.CTkLabel(row, text=str(val), text_color="#374151",
                                 font=ctk.CTkFont("Segoe UI", 10),
                                 width=120, anchor="w").pack(side="left", padx=4, pady=4)

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

        card = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text="Application Summary Report", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=18, pady=(16, 8))
        for label, val in [("Total Applications", st["total"]),
                           ("Pending", st["pending"]),
                           ("Approved", st["approved"]),
                           ("Rejected", st["rejected"]),
                           ("Approval Rate", f"{st['rate']}%"),
                           ("Unique Business Types", st["types"]),
                           ("Unique Owners", st["owners"]),
                           ("High-Risk Flagged", st["high_risk"])]:
            row = ctk.CTkFrame(card, fg_color="white")
            row.pack(fill="x", padx=18, pady=2)
            ctk.CTkLabel(row, text=str(label), text_color="#374151",
                         font=ctk.CTkFont("Segoe UI", 10), width=200, anchor="w").pack(side="left", padx=6)
            ctk.CTkLabel(row, text=str(val), text_color="#111827",
                         font=ctk.CTkFont("Segoe UI", 10, "bold"), anchor="w").pack(side="left")

        # All applications log
        log = ctk.CTkFrame(h, fg_color="white", corner_radius=10,
                           border_width=1, border_color="#E5E7EB")
        log.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(log, text=f"All Applications Log ({len(apps)})", text_color="#111827",
                     font=ctk.CTkFont("Segoe UI", 13, "bold")).pack(
            anchor="w", padx=18, pady=(16, 8))
        if not apps:
            ctk.CTkLabel(log, text="No applications submitted yet", text_color="#9CA3AF",
                         font=ctk.CTkFont("Segoe UI", 11)).pack(pady=30)
        else:
            hdr = ctk.CTkFrame(log, fg_color="#FAFAFA", corner_radius=0)
            hdr.pack(fill="x", padx=18)
            for col in ["ID", "Business", "Owner", "Status", "Submitted"]:
                ctk.CTkLabel(hdr, text=col, text_color="#374151",
                             font=ctk.CTkFont("Segoe UI", 10, "bold"),
                             width=140, anchor="w").pack(side="left", padx=4, pady=6)
            for a in apps:
                row = ctk.CTkFrame(log, fg_color="white")
                row.pack(fill="x", padx=18, pady=1)
                status_colors = {"Pending": "#D9A100", "Approved": "#2E7D32", "Rejected": "#E53E3E"}
                for val, color in [(str(a["id"]), "#374151"), (a["business_name"], "#374151"),
                                   (a["user_email"], "#6B7280"),
                                   (a["status"], status_colors.get(a["status"], "#374151")),
                                   ((a["submitted_at"] or "")[:10], "#9CA3AF")]:
                    ctk.CTkLabel(row, text=val, text_color=color,
                                 font=ctk.CTkFont("Segoe UI", 10),
                                 width=140, anchor="w").pack(side="left", padx=4, pady=3)

    # ── Placeholder view ─────────────────────────────────────
    def _render_placeholder(self, title):
        card = ctk.CTkFrame(self.host, fg_color="white", corner_radius=10,
                            border_width=1, border_color="#E5E7EB")
        card.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(card, text=f"{title} content coming soon",
                     text_color="#9CA3AF",
                     font=ctk.CTkFont("Segoe UI", 13)).pack(pady=80)
