import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from styles.landing_styles import LANDING_COLORS, LANDING_FONTS, LANDING_LAYOUT


class LandingFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=LANDING_COLORS["header_bg"])
        self.controller = controller
        self.hero_frame = None
        self.header_frame = None
        self._canvas = None
        self.tracking_ref_var = tk.StringVar()

        self._build_scrollable_layout()

    def _build_scrollable_layout(self):
        canvas = tk.Canvas(self, bg=LANDING_COLORS["page_bg"], highlightthickness=0, bd=0)
        self._canvas = canvas
        scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=canvas.yview)
        content = ctk.CTkFrame(canvas, fg_color=LANDING_COLORS["page_bg"])

        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        content_window_id = canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind(
            "<Configure>",
            lambda e: self._on_canvas_resize(content_window_id, e.width, e.height)
        )

        self._build_header(content)
        self._build_hero(content)
        self._build_how_it_works(content)
        self._build_timeline_section(content)
        self._build_requirements_section(content)
        self._build_tracking_section(content)
        self._build_scoring_section(content)
        self._build_contact_footer(content)

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def _build_header(self, parent):
        header = ctk.CTkFrame(parent, fg_color=LANDING_COLORS["header_bg"])
        header.pack(fill="x", padx=LANDING_LAYOUT["header_pad_x"], pady=LANDING_LAYOUT["header_pad_y"])
        self.header_frame = header
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        brand = ctk.CTkFrame(header, fg_color=LANDING_COLORS["header_bg"])
        brand.grid(row=0, column=0, sticky="w")

        self.nav_logo_image = self._load_nav_logo()
        if self.nav_logo_image:
            ctk.CTkLabel(brand, text="", image=self.nav_logo_image, fg_color=LANDING_COLORS["header_bg"]).pack(side="left", padx=(0, 10))

        brand_text = ctk.CTkFrame(brand, fg_color=LANDING_COLORS["header_bg"])
        brand_text.pack(side="left")

        ctk.CTkLabel(
            brand_text, text="Barangay 183",
            text_color=LANDING_COLORS["brand_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            brand_text, text="Caloocan City",
            text_color=LANDING_COLORS["brand_secondary"],
            font=ctk.CTkFont(family="Segoe UI", size=10),
        ).pack(anchor="w")

        actions = ctk.CTkFrame(header, fg_color=LANDING_COLORS["header_bg"])
        actions.grid(row=0, column=1, sticky="e")
        ctk.CTkButton(
            actions, text="Login",
            command=lambda: self.controller.show_frame("LoginFrame"),
            fg_color=LANDING_COLORS["button_secondary_bg"],
            hover_color="#EDEDED",
            text_color=LANDING_COLORS["button_secondary_fg"],
            border_width=1, border_color="#D0D5DD",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            width=90, height=34, corner_radius=6,
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            actions, text="Magrehistro / Register",
            command=lambda: self.controller.show_frame("RegisterFrame"),
            fg_color=LANDING_COLORS["button_primary_bg"],
            hover_color="#C44E00",
            text_color=LANDING_COLORS["button_primary_fg"],
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            width=170, height=36, corner_radius=6,
        ).pack(side="left")

    def _load_nav_logo(self):
        return self.controller.icons.get("lgu_logo.png", size=(38, 38))

    def _build_hero(self, parent):
        hero = ctk.CTkFrame(parent, fg_color=LANDING_COLORS["page_bg"])
        hero.pack(fill="x", pady=38)
        self.hero_frame = hero

        hero_inner = ctk.CTkFrame(hero, fg_color=LANDING_COLORS["page_bg"])
        hero_inner.pack(expand=True, pady=40)

        ctk.CTkLabel(
            hero_inner, text="Barangay 183 Business Permit System",
            fg_color=LANDING_COLORS["badge_bg"],
            text_color=LANDING_COLORS["badge_fg"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=6, padx=14, pady=6,
        ).pack()

        ctk.CTkLabel(
            hero_inner,
            text="Integrated Barangay Business\nPermit Application & Tracking\nSystem",
            text_color=LANDING_COLORS["text_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=34, weight="bold"),
            justify="center",
        ).pack(pady=(16, 12))

        ctk.CTkLabel(
            hero_inner,
            text=(
                "A modern, transparent, and efficient platform for business permit applications "
                "in Barangay 183, Caloocan City. Featuring AI-assisted decision support to help "
                "our staff process applications faster and more consistently."
            ),
            text_color=LANDING_COLORS["text_secondary"],
            font=ctk.CTkFont(family="Segoe UI", size=13),
            justify="center",
            wraplength=LANDING_LAYOUT["hero_wrap"],
        ).pack(padx=20)

        ctas = ctk.CTkFrame(hero_inner, fg_color=LANDING_COLORS["page_bg"])
        ctas.pack(pady=22)

        ctk.CTkButton(
            ctas, text="Mag-apply ng Permit",
            command=lambda: self.controller.show_frame("RegisterFrame"),
            fg_color=LANDING_COLORS["button_primary_bg"],
            hover_color="#C44E00",
            text_color=LANDING_COLORS["button_primary_fg"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            width=200, height=44, corner_radius=8,
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            ctas, text="I-track ang Application",
            command=lambda: self.controller.show_frame("LoginFrame"),
            fg_color=LANDING_COLORS["button_secondary_bg"],
            hover_color="#EDEDED",
            text_color=LANDING_COLORS["button_secondary_fg"],
            border_width=1, border_color="#D0D5DD",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            width=200, height=44, corner_radius=8,
        ).pack(side="left", padx=6)

    def _on_canvas_resize(self, content_window_id, width, height):
        self._canvas.itemconfigure(content_window_id, width=width)

    def _build_how_it_works(self, parent):
        section = ctk.CTkFrame(parent, fg_color=LANDING_COLORS["page_bg"])
        section.pack(fill="x", pady=LANDING_LAYOUT["section_gap_y"])

        ctk.CTkLabel(
            section, text="Paano Ito Gumagana? / How It Works",
            text_color=LANDING_COLORS["text_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
        ).pack()
        ctk.CTkLabel(
            section, text="Simple three-step process for your business permit",
            text_color="#5B5B5B",
            font=ctk.CTkFont(family="Segoe UI", size=11),
        ).pack(pady=(6, 20))

        cards_wrap = ctk.CTkFrame(section, fg_color=LANDING_COLORS["page_bg"])
        cards_wrap.pack(fill="x", padx=LANDING_LAYOUT["content_pad_x"])

        cards = [
            ("1", "Submit Application", "Complete the online form and upload required documents. The system will guide you through every step."),
            ("2", "Review by Barangay Staff", "Our trained staff reviews your application with AI assistance for completeness and compliance checks."),
            ("3", "Approval & Release", "Once approved by authorized officials, receive your permit and start operating your business legally."),
        ]

        for idx, (step, title, body) in enumerate(cards):
            card = ctk.CTkFrame(
                cards_wrap,
                fg_color=LANDING_COLORS["card_bg"],
                border_width=1,
                border_color=LANDING_COLORS["card_border"],
                corner_radius=10,
            )
            card.grid(row=0, column=idx, padx=LANDING_LAYOUT["cards_gap_x"], pady=LANDING_LAYOUT["cards_gap_y"], sticky="nsew")
            cards_wrap.grid_columnconfigure(idx, weight=1)

            ctk.CTkLabel(
                card, text=step,
                fg_color=LANDING_COLORS["step_badge_bg"],
                text_color=LANDING_COLORS["step_badge_fg"],
                font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                width=40, height=40, corner_radius=20,
            ).pack(pady=(20, 18))
            ctk.CTkLabel(
                card, text=title,
                text_color="#0F1B3A",
                font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
                wraplength=LANDING_LAYOUT["card_wrap"],
                justify="center",
            ).pack()
            ctk.CTkLabel(
                card, text=body,
                text_color="#4E4E4E",
                font=ctk.CTkFont(family="Segoe UI", size=11),
                wraplength=LANDING_LAYOUT["card_wrap"],
                justify="center",
            ).pack(pady=(12, 20), padx=18)

    def _build_requirements_section(self, parent):
        section = ctk.CTkFrame(parent, fg_color=LANDING_COLORS["page_bg"])
        section.pack(fill="x", pady=LANDING_LAYOUT["section_gap_y"])

        box = ctk.CTkFrame(
            section,
            fg_color=LANDING_COLORS["requirements_bg"],
            border_width=1,
            border_color=LANDING_COLORS["requirements_border"],
            corner_radius=10,
        )
        box.pack(fill="x", padx=LANDING_LAYOUT["content_pad_x"])

        ctk.CTkLabel(
            box, text="Requirements Checklist",
            text_color=LANDING_COLORS["text_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
        ).pack(anchor="w", padx=36, pady=(20, 0))
        ctk.CTkLabel(
            box, text="Prepare these before starting your business permit application.",
            text_color=LANDING_COLORS["muted_text"],
            font=ctk.CTkFont(family="Segoe UI", size=11),
        ).pack(anchor="w", padx=36, pady=(2, 14))

        items = [
            "Valid government ID of applicant",
            "Business name and activity details",
            "Proof of business address or lease agreement",
            "Recent community tax certificate (if applicable)",
            "Previous permit copy for renewal (if any)",
            "Initial payment reference or official receipt details",
        ]
        grid = ctk.CTkFrame(box, fg_color=LANDING_COLORS["requirements_bg"])
        grid.pack(fill="x", padx=36, pady=(0, 20))
        for col_idx in range(LANDING_LAYOUT["requirements_columns"]):
            grid.grid_columnconfigure(col_idx, weight=1)

        for idx, text in enumerate(items):
            row = idx // LANDING_LAYOUT["requirements_columns"]
            col = idx % LANDING_LAYOUT["requirements_columns"]
            ctk.CTkLabel(
                grid, text=f"•  {text}",
                text_color=LANDING_COLORS["text_secondary"],
                font=ctk.CTkFont(family="Segoe UI", size=11),
                justify="left", anchor="w", wraplength=430,
            ).grid(row=row, column=col, sticky="w", padx=(0, 20), pady=6)

    def _build_tracking_section(self, parent):
        section = ctk.CTkFrame(parent, fg_color=LANDING_COLORS["page_bg"])
        section.pack(fill="x", pady=LANDING_LAYOUT["section_gap_y"])

        box = ctk.CTkFrame(
            section,
            fg_color=LANDING_COLORS["card_bg"],
            border_width=1,
            border_color=LANDING_COLORS["card_border"],
            corner_radius=10,
        )
        box.pack(fill="x", padx=LANDING_LAYOUT["content_pad_x"])

        ctk.CTkLabel(
            box, text="Track Application by Reference Number",
            text_color=LANDING_COLORS["text_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
        ).pack(anchor="w", padx=36, pady=(20, 0))
        ctk.CTkLabel(
            box, text="Enter your reference number to check your current application status.",
            text_color=LANDING_COLORS["muted_text"],
            font=ctk.CTkFont(family="Segoe UI", size=11),
        ).pack(anchor="w", padx=36, pady=(2, 14))

        input_wrap = ctk.CTkFrame(box, fg_color=LANDING_COLORS["card_bg"])
        input_wrap.pack(fill="x", padx=36, pady=(0, 20))
        input_wrap.grid_columnconfigure(0, weight=1)

        entry = ctk.CTkEntry(
            input_wrap,
            textvariable=self.tracking_ref_var,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=40, corner_radius=6,
            border_width=1, border_color="#D0D5DD",
        )
        entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        ctk.CTkButton(
            input_wrap, text="Track Now",
            command=self._track_application,
            fg_color=LANDING_COLORS["button_primary_bg"],
            hover_color="#C44E00",
            text_color=LANDING_COLORS["button_primary_fg"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            width=130, height=40, corner_radius=6,
        ).grid(row=0, column=1)

    def _build_timeline_section(self, parent):
        section = ctk.CTkFrame(parent, fg_color=LANDING_COLORS["page_bg"])
        section.pack(fill="x", pady=LANDING_LAYOUT["section_gap_y"])

        ctk.CTkLabel(
            section, text="Processing Timeline",
            text_color=LANDING_COLORS["text_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
        ).pack()
        ctk.CTkLabel(
            section, text="Standard status flow and expected processing timeline.",
            text_color=LANDING_COLORS["muted_text"],
            font=ctk.CTkFont(family="Segoe UI", size=11),
        ).pack(pady=(2, 14))

        timeline = ctk.CTkFrame(section, fg_color=LANDING_COLORS["page_bg"])
        timeline.pack(fill="x", padx=LANDING_LAYOUT["content_pad_x"])

        steps = [
            ("Submitted", "Day 0"),
            ("Under Review", "1-2 business days"),
            ("For Approval", "Next 1-2 business days"),
            ("Released", "After approval"),
        ]
        for idx in range(LANDING_LAYOUT["timeline_steps"]):
            timeline.grid_columnconfigure(idx, weight=1)

        for idx, (title, eta) in enumerate(steps):
            cell = ctk.CTkFrame(timeline, fg_color=LANDING_COLORS["page_bg"])
            cell.grid(row=0, column=idx, sticky="nsew", padx=6)

            dot_color = LANDING_COLORS["timeline_dot_active"] if idx == 0 else LANDING_COLORS["timeline_dot"]
            ctk.CTkLabel(
                cell, text="", fg_color=dot_color,
                width=16, height=16, corner_radius=8,
            ).pack(pady=(0, 4))
            tk.Frame(cell, bg=LANDING_COLORS["timeline_line"], height=2).pack(fill="x", padx=16, pady=4)
            ctk.CTkLabel(
                cell, text=title,
                text_color=LANDING_COLORS["text_primary"],
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            ).pack()
            ctk.CTkLabel(
                cell, text=eta,
                text_color=LANDING_COLORS["muted_text"],
                font=ctk.CTkFont(family="Segoe UI", size=10),
            ).pack()

    def _track_application(self):
        reference = self.tracking_ref_var.get().strip()
        if not reference:
            messagebox.showwarning("Missing Reference", "Please enter your application reference number.")
            return
        messagebox.showinfo(
            "Tracking Available",
            f"Reference '{reference}' captured.\nPlease sign in to view full application details.",
        )
        self.controller.show_frame("LoginFrame")

    def _build_scoring_section(self, parent):
        section = ctk.CTkFrame(parent, fg_color=LANDING_COLORS["page_bg"])
        section.pack(fill="x", pady=LANDING_LAYOUT["section_gap_y"])

        outer = ctk.CTkFrame(section, fg_color=LANDING_COLORS["accent_panel_bg"], corner_radius=12)
        outer.pack(fill="x", padx=LANDING_LAYOUT["content_pad_x"])
        content = ctk.CTkFrame(outer, fg_color=LANDING_COLORS["accent_panel_bg"])
        content.pack(fill="x", padx=22, pady=22)
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=1)

        left = ctk.CTkFrame(content, fg_color=LANDING_COLORS["accent_panel_bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        ctk.CTkLabel(
            left, text="AI-Powered Decision Support",
            fg_color=LANDING_COLORS["accent_chip_bg"],
            text_color=LANDING_COLORS["accent_chip_fg"],
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            corner_radius=6, padx=10, pady=4,
        ).pack(anchor="w")

        ctk.CTkLabel(
            left, text="Rule-Assisted Scoring Model",
            text_color=LANDING_COLORS["button_primary_fg"],
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
        ).pack(anchor="w", pady=(10, 8))

        ctk.CTkLabel(
            left,
            text=(
                "Our system uses AI technology to assist barangay staff in assessing application "
                "completeness, identifying potential risks, and recommending priority levels. "
                "This supports fair, consistent, and efficient processing for all applicants."
            ),
            text_color=LANDING_COLORS["accent_text"],
            font=ctk.CTkFont(family="Segoe UI", size=11),
            wraplength=LANDING_LAYOUT["panel_text_wrap"],
            justify="left",
        ).pack(anchor="w")

        highlight_data = [
            ("AI-Assisted Evaluation", "For decision support only"),
            ("Data-Driven Insights", "Risk and completeness scoring"),
            ("Consistent Processing", "Standardized review criteria"),
            ("Human Oversight & Final Decision Authority", "Final approval remains with authorized barangay officials"),
        ]
        highlights = ctk.CTkFrame(left, fg_color=LANDING_COLORS["accent_panel_bg"])
        highlights.pack(fill="x", pady=(16, 0))
        for text, subtext in highlight_data:
            item = ctk.CTkFrame(highlights, fg_color=LANDING_COLORS["highlight_bg"], corner_radius=6)
            item.pack(anchor="w", pady=4, fill="x")
            ctk.CTkLabel(
                item, text=text,
                text_color=LANDING_COLORS["highlight_fg"],
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            ).pack(anchor="w", padx=11, pady=(7, 0))
            ctk.CTkLabel(
                item, text=subtext,
                text_color=LANDING_COLORS["accent_text"],
                font=ctk.CTkFont(family="Segoe UI", size=10),
            ).pack(anchor="w", padx=11, pady=(0, 7))

        right = ctk.CTkFrame(content, fg_color=LANDING_COLORS["accent_panel_bg"])
        right.grid(row=0, column=1, sticky="n", padx=(8, 0))
        visual = ctk.CTkFrame(
            right,
            fg_color=LANDING_COLORS["panel_visual_bg"],
            width=LANDING_LAYOUT["panel_visual_size"],
            height=LANDING_LAYOUT["panel_visual_size"],
            corner_radius=70,
        )
        visual.pack(pady=16)
        visual.pack_propagate(False)
        ctk.CTkLabel(
            visual, text="AI",
            text_color=LANDING_COLORS["panel_visual_fg"],
            font=ctk.CTkFont(family="Segoe UI", size=42, weight="bold"),
        ).place(relx=0.5, rely=0.5, anchor="center")

    def _build_contact_footer(self, parent):
        footer = ctk.CTkFrame(parent, fg_color=LANDING_COLORS["page_bg"])
        footer.pack(fill="x", pady=30)

        contact_box = ctk.CTkFrame(
            footer, fg_color=LANDING_COLORS["card_bg"],
            border_width=1, border_color=LANDING_COLORS["card_border"],
            corner_radius=10,
        )
        contact_box.pack(fill="x", padx=LANDING_LAYOUT["content_pad_x"])

        ctk.CTkLabel(
            contact_box, text="Contact Barangay 183 Office",
            text_color=LANDING_COLORS["brand_primary"],
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
        ).pack(anchor="w", padx=24, pady=(20, 0))

        grid = ctk.CTkFrame(contact_box, fg_color=LANDING_COLORS["card_bg"])
        grid.pack(fill="x", padx=24, pady=(10, 20))
        for i in range(4):
            grid.grid_columnconfigure(i, weight=1)

        details = [
            ("Address", "F. Bautista St., Midtown Park Subd., Barangay 183, District 1, Caloocan"),
            ("Contact Number", "(02) 8936 4830"),
            ("Email", "brgy183@caloocan.gov.ph"),
            ("Office Hours", "Monday - Friday, 8:00 AM - 5:00 PM"),
        ]

        for idx, (label, value) in enumerate(details):
            col = ctk.CTkFrame(grid, fg_color=LANDING_COLORS["card_bg"])
            col.grid(row=0, column=idx, sticky="nsew", padx=8)
            ctk.CTkLabel(
                col, text=label,
                text_color="#1F1F1F",
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            ).pack(anchor="w")
            ctk.CTkLabel(
                col, text=value,
                text_color="#4D4D4D",
                font=ctk.CTkFont(family="Segoe UI", size=10),
                wraplength=LANDING_LAYOUT["contact_wrap"],
                justify="left",
            ).pack(anchor="w")

        ctk.CTkLabel(
            footer, text="© 2026 Barangay 183 Business Permit System",
            text_color="#565656",
            font=ctk.CTkFont(family="Segoe UI", size=10),
        ).pack(pady=(12, 0))
