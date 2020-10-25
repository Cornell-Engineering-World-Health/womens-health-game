# Import Libraries
from kivymd.app import MDApp
from kivy.lang import Builder

# Import Screens
from ui.loginscreen import LoginScreen
from ui.dashboard import Dashboard
from ui.module import Module
from ui.AssessmentManager import AssessmentManager
from ui.settingsscreen import SettingsScreen
from ui.splashscreen import SplashScreen

# Import Constants
from util.constants import _title_
from util.style import app_style
from util.client import logout

# Initialize APP
class MyApp(MDApp):

    # Constructor
    def build(self):
        self.title = _title_
        self.theme_cls.primary_palette = app_style["primary_theme"]
        return Builder.load_file("main.kv")

    def settings(self):
    	MDApp.get_running_app().root.ids.screen_manager.current = 'settings_screen'
    
    def login(self):
        sm = MDApp.get_running_app().root.ids.screen_manager
        sm.current = 'login_screen'
        logout(sm)
    
# Start App
MyApp().run()