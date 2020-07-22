from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, RoundedRectangle
import kivy.utils


class Card(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__()

        with self.canvas.before:
            Color(rgba=(0, 0, .4, 0.1))
            self.rect = RoundedRectangle(radius=[(40.0, 40.0), (40.0, 40.0), (40.0, 40.0), (40.0, 40.0)])
        self.bind(pos=self.update_rect, size=self.update_rect)


        self.first_name = MDLabel(text=kwargs["first_name"],
                             pos_hint={"center_x": .5, "top": .9}, size_hint=(.5, .3),
                             theme_text_color="Primary", font_style="H6", halign="center")

        self.last_name = MDLabel(text=kwargs["last_name"],
                             pos_hint={"center_x": .5, "top": .8}, size_hint=(.5, .3),
                             theme_text_color="Primary", font_style="H6", halign="center")
        
        self.village_name = MDLabel(text=kwargs["village_name"],
                             pos_hint={"center_x": .5, "top": .6}, size_hint=(.5, .3),
                             theme_text_color="Primary", font_style="H5", halign="center")
    

        self.add_widget(self.first_name)
        self.add_widget(self.last_name)
        self.add_widget(self.village_name)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
