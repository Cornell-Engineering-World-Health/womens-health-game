from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.button import MDFillRoundFlatButton
import kivy.utils

from util.style import card_style
from util.ui_support import RoundButton

class Card(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__()

        # create card shape and background
        with self.canvas.before:
            Color(rgba=card_style["background_color"])
            self.rect = RoundedRectangle(radius=card_style["radius"])
        self.bind(pos=self.update_rect, size=self.update_rect)

        # set name variables to the corresponding passed in arguments
        self.name = self.generateCardLabel(kwargs["first_name"]+" "+kwargs["last_name"], card_style["title_font"], card_style["name_y"])
        self.village_name = self.generateCardLabel(kwargs["village_name"], card_style["subtitle_font"],  card_style["village_name_y"])

        # access the screen manager via kwargs and set it to variable 'sm'
        self.sm = kwargs['screen_manager']

        # set 'selected_user' to the current user via kwargs
        self.selected_user = {"id": kwargs["id"], "first_name": kwargs["first_name"], "last_name": kwargs["last_name"]}

        # add widgets (all labels, buttons, etc) to the screen
        self.add_widget(self.name)
        self.add_widget(self.village_name)
        self.add_widget(self.selectionButton())
        # self.add_widget(MDLabel(text="Progress", pos_hint={"center_x": 0.2, "top": 0.6}, size_hint=card_style["size"], theme_text_color=card_style["theme"], font_style="Caption", halign="center"))
        # self.add_widget(self.module(0)) # TODO: get module number
        # self.add_widget(self.progress(50))  # TODO: get progress
        self.add_widget(self.photo('assets/profile.png'))

    # menu screen
    def menu(self, instance):
        self.sm.screens[6].ids.user = self.selected_user
        #self.sm.screens[2].ids.module_number = 1 # get module number from user
        self.sm.current = 'menu_screen'

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def photo(self, source):
        return Image(source=source, pos_hint= {"center_x": 0.5, "top": 0.85}, size_hint_y= None, height= 120)
        #return RoundedButton(background_normal=source, background_down=source, pos_hint= {"center_x": 0.5, "top": 0.95}, size_hint =(.2, .2))

    def generateCardLabel(self, label, style, height):
        return MDLabel(text=label, pos_hint={"center_x": card_style["center_x"], "top": height}, size_hint=card_style["size"], theme_text_color=card_style["theme"], font_style=style, halign="center")

    # def module(self, module):
    #     return MDLabel(text="Module %d"%module, pos_hint={"center_x": 0.22, "top": 0.5}, size_hint=card_style["size"], theme_text_color=card_style["theme"], font_style="Subtitle2", halign="center")

    # def progress(self, progress):
    #     return MDLabel(text="%d %% \ncompleted"%progress, pos_hint={"center_x": 0.8, "top": 0.55}, size_hint=card_style["size"], theme_text_color="Custom", text_color= (0.227, 0.655, 0.427, 1), font_style="Caption", halign="center")

    def selectionButton(self):
        bt = RoundButton(text="Select", color=(0,0,0,1), font_size= '15sp', bold= True, pos_hint={"center_x": card_style["center_x"], "top": 0.2},size_hint=(.5, .15))
        bt.bind(on_press=self.menu)
        return bt
