from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.properties import StringProperty
from util.client import login


class LoginScreen(Screen):
    error_message = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        self.app.title = "Login"

    """
    Called when the user presses the login button.
    """
    def login(self):
        status = login(self.login_email, self.login_password)

        #always clear password inbetween logins
        self.ids.password.text = ""

        #login successful
        if(status[0]):
            self.ids.email.text = ""
            self.manager.current = 'dashboard'

        #login unsuccesful
        elif status[1] == "login_failure":
            self.process_error("Invalid username or password")

        elif status[1] == "network_failure":
            self.process_error("Something went wrong on our end, please try again in a couple minutes. If this message persists, please contact Cornell Engineering World Health for support.")

    def process_email(self):
        self.clear_error()
        self.login_email = self.ids.email.text

    def process_password(self):
        self.clear_error()
        self.login_password = self.ids.password.text

    def clear_error(self):
        self.error_message = ""

    def process_error(self, message):
        self.error_message = message
