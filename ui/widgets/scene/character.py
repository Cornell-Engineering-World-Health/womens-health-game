from kivy.clock import Clock
from kivy.app import App

from kivymd.uix.button import *
from kivy.graphics import Color, Rectangle

# import behaviors
from kivy.uix.behaviors import *


class Character():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        boolean is_talking = false

        self.ui_layout()

    def ui_layout(self):
        print(is_talking)
