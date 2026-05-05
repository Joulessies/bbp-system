import customtkinter as ctk
from pathlib import Path
from database.db import init_db
from pages.landing import LandingFrame
from pages.login import LoginFrame
from pages.register import RegisterFrame
from pages.dashboard import DashboardFrame
from pages.admin import AdminFrame
from ui.icons import AppIcons

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class BBPSystemApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BBP System")
        self.state("zoomed")
        self.configure(fg_color="white")
        self.assets_dir = Path(__file__).resolve().parent / "assets"
        self.icons = AppIcons(self.assets_dir)
        self._set_window_icon()

        init_db()
        self.logged_in_user = None

        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LandingFrame, LoginFrame, RegisterFrame, DashboardFrame, AdminFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LandingFrame")

    def _set_window_icon(self):
        app_icon = self.icons.get("lgu_logo.png", size=(64, 64))
        if app_icon:
            self.iconphoto(True, app_icon)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name in ("DashboardFrame", "AdminFrame"):
            frame.update_welcome()
        frame.tkraise()


if __name__ == "__main__":
    app = BBPSystemApp()
    app.mainloop()
