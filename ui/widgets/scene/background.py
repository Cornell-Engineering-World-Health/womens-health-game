from kivy.clock import Clock
from kivy.app import App

from kivymd.uix.button import *
from kivy.graphics import Color, Rectangle

# import behaviors
from kivy.uix.behaviors import *


class Background():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name', '')
        self.scenes = kwargs.get('scenes', [])
        self.image = kwargs.get('img', '')
        self.ui_layout()

    def ui_layout(self):
        print(self.image)
