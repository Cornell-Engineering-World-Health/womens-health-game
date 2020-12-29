from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from util.client import logout
from kivy.properties import StringProperty
from util.store import get_admin_state


class SettingsScreen(Screen):
    email = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        admin_state = get_admin_state()
        self.users = admin_state['users']
        self.email = admin_state['admin']['email']
        self.app.title = "Settings"

    def logout(self):
        sm = MDApp.get_running_app().root.ids.screen_manager
        sm.current = 'login_screen'
        logout(sm)
