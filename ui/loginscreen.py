from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from util.client import login, update_state
from util.store import current_state


class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        self.ids.admin = None

    def on_pre_enter(self, *args):
        self.app.title = "Login"
        self.add_local_state_to_backend()

    def add_local_state_to_backend(self):
        state = current_state()
        for user in state:
            game_state = state[user]['game_state']
            for module in range(len(game_state)):
                update_state(user, game_state[module])

    def login(self):
        # TEMP BYPASS
            if self.login_email == 'EWH':
                self.manager.current = 'module'
                return
            try:
                self.ids.admin = login(self.login_email, self.login_password)
                self.ids.email.text = ""
                self.ids.password.text = ""
                self.manager.current = 'dashboard'
            except Exception as err:
                print("ERROR", err)

    def process_email(self):
        self.login_email = self.ids.email.text

    def process_password(self):
        self.login_password = self.ids.password.text
