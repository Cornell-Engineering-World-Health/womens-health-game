from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.clock import Clock
from util.store import admin_state_exists
from util.store import get_admin_state

"""
This is the first page of our application that is shown while everything for the
game is being loaded.
"""
class SplashScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        Clock.schedule_once(self.after_init, 1)

    def on_pre_enter(self, *args):
        self.app.title = "Splash"

    """
    This is the main function for this screen, where we determine what screen 
    to progress to. 

    We go to the *login_screen* if no one has ever logged into this device before.

    We go to the *dashboard* (aka the student selection page) if an admin has logged in,
    but hasn't chosen a student to play the game.

    We go to the *menu_screen* (aka the module selection page) if an admin has logged in 
    and has chosen a student already.
    """
    def after_init(self, dt):
        sm = MDApp.get_running_app().root.ids.screen_manager

        if not admin_state_exists():
            sm.current = 'login_screen'
            return
            
        admin_state = get_admin_state()

        if admin_state.get("current_user") is not None:
            current_user = self._get_user_by_id_from_users(admin_state["current_user"], admin_state["users"])

            #set the appropriate user fields in the module selection screen
            sm.screens[6].ids.user = {"id": current_user["_id"], "first_name": current_user["first_name"], "last_name": current_user["last_name"]}
            
            sm.current = "menu_screen"
        else:
            sm.current = "dashboard"

    def _get_user_by_id_from_users(self, id, users):
        for user in users:
            if user['_id'] == id:
                return user
        return None