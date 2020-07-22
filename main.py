# Import Libraries
from kivymd.app import MDApp
from kivy.lang import Builder



# Import Screens
from baseclass.loginscreen import LoginScreen
from baseclass.dashboard import DashBoard
from baseclass.settingsscreen import SettingsScreen


# Initialize APP
class MyApp(MDApp):

    # Constructor
    def build(self):
        self.title = "Health Friend"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("main.kv")

    def settings(self):
    	MDApp.get_running_app().root.ids.screen_manager.current = 'settings_screen'

# Start App
MyApp().run()
