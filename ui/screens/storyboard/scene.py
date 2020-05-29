# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.widget import Widget

# kivymd imports
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

# import layouts
from kivy.uix.boxlayout import BoxLayout


class SceneScreen(Screen):
    def __init__(self, **kwargs):
        super(SceneScreen, self).__init__(name=kwargs.get('name'))
        self.ui_layout()

    def ui_layout(self):
        self.clear_widgets()

        # Layout declarations
        boxlayout = BoxLayout(orientation='horizontal')

        # Widget declarations

        # Adding widgets to layouts

        # Adding layouts to screen
        self.add_widget(boxlayout)

        self.do_layout()

    def change_screen(self, screen):
        self.manager.current = screen
