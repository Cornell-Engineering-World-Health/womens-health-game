from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from util.client import logout
from kivy.properties import StringProperty
from util.store import get_admin_state
import webbrowser

class SettingsScreen(Screen):
    email = StringProperty("")
    error_message = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        admin_state = get_admin_state()
        self.users = admin_state['users']
        self.email = admin_state['admin']['email']
        self.app.title = "Settings"
        self.clear_error()

    # navigate back to previous screen
    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = self.ids.prev_page

    def open_url(self):
        webbrowser.open("https://health-friend-admin-website.herokuapp.com")

    def logout(self):
        sm = MDApp.get_running_app().root.ids.screen_manager
        status = logout(sm)
        if not status:
            self.process_error("Failed to log out, this is likely a network issue. Please check you are connected to the internet and try again.")

    def clear_error(self):
        self.error_message = ""

    def process_error(self, message):
        self.error_message = message
