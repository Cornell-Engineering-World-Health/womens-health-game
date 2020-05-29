from kivy.clock import Clock
from kivy.app import App

from kivymd.uix.button import *
from kivy.graphics import Color, Rectangle

# import behaviors
from kivy.uix.behaviors import *


class Line():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # character name
        self.character = kwargs.get('character', '')
        self.audio = kwargs.get('audio', '')
        self.text = kwargs.get('text', '')
        self.ui_layout()

    def ui_layout(self):
        print(self.text)
