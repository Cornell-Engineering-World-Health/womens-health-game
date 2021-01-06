# Import Libraries

# from kivy.config import Config
# Config.set('graphics', 'resizable', 0)

from kivymd.app import MDApp
from kivy.lang import Builder

# Import Screens
from ui.loginscreen import LoginScreen
from ui.dashboard import Dashboard
from ui.module import Module
from ui.AssessmentManager import AssessmentManager
from ui.settingsscreen import SettingsScreen
from ui.splashscreen import SplashScreen
from ui.menuscreen import MenuScreen

# Import Constants
from util.constants import _title_
from util.style import app_style

"""
This is the main entrypoint into the application. The first screen we load is the
Splash Screen.
"""
class MyApp(MDApp):

    # Constructor
    def build(self):
        self.title = _title_
        self.theme_cls.primary_palette = app_style["primary_theme"]
        return Builder.load_file("main.kv")

    def settings(self, prev_page):
        sm = MDApp.get_running_app().root.ids.screen_manager
        sm.transition.direction = 'left'
        sm.current = 'settings_screen'
        sm.screens[5].ids.prev_page = prev_page


# Start App
MyApp().run()
