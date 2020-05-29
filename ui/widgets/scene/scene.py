from kivy.clock import Clock
from kivy.app import App

from kivymd.uix.button import *
from kivy.graphics import Color, Rectangle

# import behaviors
from kivy.uix.behaviors import *


class Scene():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.characters = kwargs.get('characters', [])
        self.lines = kwargs.get('lines', [])
        # background can either be an index or a name
        self.background = kwargs.get('background', '')
