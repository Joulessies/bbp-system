import tkinter as tk

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e1e")
        self.controller = controller
        
        self.container = tk.Frame(self, bg="#1e1e1e")
        self.container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.welcome_label = tk.Label(self.container, text="", fg="white", bg="#1e1e1e", font=controller.header_font, justify="center")
        self.welcome_label.pack(pady=(0, 40))
        
        tk.Button(self.container, text="Logout", command=lambda: controller.show_frame("LoginFrame"), bg="#dc3545", fg="white", font=controller.custom_font, relief="flat", width=15, pady=5).pack()

    def update_welcome(self):
        self.welcome_label.config(text=f"Welcome,\n{self.controller.logged_in_user}!")
