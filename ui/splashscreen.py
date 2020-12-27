from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.clock import Clock

from util.client import update_state
from util.store import current_state

class SplashScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        Clock.schedule_once(self.after_init, 1)

    def add_local_state_to_backend(self):
        state = current_state()
        for user in state:
            game_state = state[user]['game_state']
            for module in range(len(game_state)):
                update_state(user, game_state[module])

    def on_pre_enter(self, *args):
        self.app.title = "Splash"

    def after_init(self, dt):
        MDApp.get_running_app().root.ids.screen_manager.current = 'login_screen'
