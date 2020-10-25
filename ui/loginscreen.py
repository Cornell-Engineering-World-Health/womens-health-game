from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from util.client import get_students_from_admin_id, authorize, login


class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        authorize()
        self.app.title = "Login"

    def login(self):
        # TEMP BYPASS
        if self.login_email == 'EWH':
            self.manager.current = 'module'

        try:
            self.ids.admin = login(self.login_email, self.login_password)
            res = get_students_from_admin_id(self.ids.admin['localId'])
            self.ids.users = res
            self.ids.email.text = ""
            self.ids.password.text = ""
            self.manager.current = 'dashboard'
        except NameError as err:
            print("ERROR", err)
        except Exception as err:
            print("INVALID USERNAME OR PASSWORD, PLEASE TRY AGAIN")

    def process_email(self):
        self.login_email = self.ids.email.text

    def process_password(self):
        self.login_password = self.ids.password.text
