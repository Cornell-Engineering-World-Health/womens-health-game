from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from util.client import login


class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        self.app.title = "Login"

    def login(self):
            try:
                login(self.login_email, self.login_password)
                self.ids.email.text = ""
                self.ids.password.text = ""
                self.manager.current = 'dashboard'
            except Exception as err:
                print("ERROR", err)

    def process_email(self):
        self.login_email = self.ids.email.text

    def process_password(self):
        self.login_password = self.ids.password.text
