from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.clock import Clock
from util.store import admin_state_exists
from util.store import get_admin_state

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
            return
            
        admin_state = get_admin_state()

        if admin_state.get("current_user") is not None:
            current_user = self._get_user_by_id_from_users(admin_state["current_user"], admin_state["users"])

            sm.screens[6].ids.user = {"id": current_user["_id"], "first_name": current_user["first_name"], "last_name": current_user["last_name"]}
            sm.current = "menu_screen"
        else:
            sm.current = "dashboard"

    def _get_user_by_id_from_users(self, id, users):
        for user in users:
            if user['_id'] == id:
                return user
        return None