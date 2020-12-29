from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.clock import Clock
from util.store import admin_state_exists


class SplashScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        Clock.schedule_once(self.after_init, 1)

    def on_pre_enter(self, *args):
        self.app.title = "Splash"

    def after_init(self, dt):
        sm = MDApp.get_running_app().root.ids.screen_manager
        if not admin_state_exists():
            sm.current = 'login_screen'
        else:
            print("Admin already logged in")
            sm.current = 'dashboard'
