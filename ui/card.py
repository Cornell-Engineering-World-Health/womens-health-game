from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, RoundedRectangle
import kivy.utils

from util.style import card_style

class Card(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__()

        with self.canvas.before:
            Color(rgba=card_style["background_color"])
            self.rect = RoundedRectangle(radius=card_style["radius"])
        self.bind(pos=self.update_rect, size=self.update_rect)        

        self.first_name = self.generateCardLabel(kwargs["first_name"], card_style["title_font"], card_style["first_name_y"])
        self.last_name = self.generateCardLabel(kwargs["last_name"], card_style["title_font"], card_style["last_name_y"])
        self.village_name = self.generateCardLabel(kwargs["village_name"], card_style["subtitle_font"],  card_style["village_name_y"])
    

        self.add_widget(self.first_name)
        self.add_widget(self.last_name)
        self.add_widget(self.village_name)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def generateCardLabel(self, label, style, height):
        return MDLabel(text=label, pos_hint={"center_x": card_style["center_x"], "top": height}, size_hint=card_style["size"], theme_text_color=card_style["theme"], font_style=style, halign="center")

