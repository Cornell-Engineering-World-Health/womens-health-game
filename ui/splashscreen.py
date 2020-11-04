from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.clock import Clock

class SplashScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        Clock.schedule_once(self.after_init, 5)

    def on_pre_enter(self, *args):
        self.app.title = "Splash"
        
    def after_init(self, dt):
        MDApp.get_running_app().root.ids.screen_manager.current = 'login_screen'

