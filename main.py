#kivy imports
from kivymd.app import MDApp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager
from util.utility import Utility

#screen imports
from ui.screens.login import LoginScreen
from ui.screens.storyboard.scenemanager import SceneManagerScreen
# from ui.widgets.scene.script import Script

#project imports (backend code we might need, etc)

class MainBox(FloatLayout):
    def __init__(self, **kwargs):
        super(MainBox, self).__init__()

        self.screens = AnchorLayout(anchor_x='center', anchor_y='center')
        self.util = kwargs.get('util')
        self.content = ScreenManager()
        # self.content.add_widget(LoginScreen(name='login', util=self.util))
        self.content.add_widget(SceneManagerScreen(name='scenemanager'))
        self.screens.add_widget(self.content)

        self.add_widget(self.screens)

class MainApp(MDApp):
    util = Utility()

    def __init__(self, **kwargs):
        self.title = "Health Friend"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        super().__init__(**kwargs)

    def build(self):
        return MainBox(util=self.util)


if __name__ == '__main__':
     MainApp().run()
