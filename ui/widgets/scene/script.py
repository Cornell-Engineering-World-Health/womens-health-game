from kivy.clock import Clock
from kivy.app import App

from kivymd.uix.button import *
from kivy.graphics import Color, Rectangle

# import behaviors
from kivy.uix.behaviors import *


class Script():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scenes = kwargs.get('scenes', [])
        # add scenes
