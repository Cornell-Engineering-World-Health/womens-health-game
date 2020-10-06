from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from util.client import get_students_from_admin_id, authorize
from util.firebase import firebase


class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        authorize()
        # self.app.title = "Login"

    def login(self):
        # TEMP BYPASS
        if self.login_email == 'EWH':
            self.manager.current = 'module'
            return

        try:
            auth = firebase.auth()
            user = auth.sign_in_with_email_and_password(self.login_email, self.login_password)
            self.ids.admin = user
       
            res = get_students_from_admin_id(user['localId'])

            self.ids.users = res
            self.manager.current = 'dashboard'

        except Exception:
            print("INVALID USERNAME OR PASSWORD, PLEASE TRY AGAIN")

    def process_email(self):
        self.login_email = self.ids.email.text

    def process_password(self):
        self.login_password = self.ids.password.text
