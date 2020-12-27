from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.button import MDFillRoundFlatButton
import kivy.utils

from util.style import module_card_style
from util.ui_support import RoundButton, FitImage
#from kivymd.utils.fitimage import FitImage

class ModuleCard(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__()

        # create card shape and background
        with self.canvas.before:
            Color(rgba=module_card_style["background_color"])
            self.rect = RoundedRectangle(radius=module_card_style["radius"])
        self.bind(pos=self.update_rect, size=self.update_rect)

        # access the screen manager via kwargs and set it to variable 'sm'
        self.sm = kwargs['screen_manager']

        # set 'selected_user' to the current user via kwargs
        self.selected_user = kwargs["user"]

        # module
        self.module = kwargs["module"]
        # module labels
        self.module_id = self.generateCardLabel('Module '+str(self.module.get("id") + 1), module_card_style["module_font"], module_card_style["id_y"])
        self.module_title = self.generateCardLabel(self.module.get("title"), module_card_style["module_font"], module_card_style["title_y"])

        # add widgets (all labels, buttons, etc) to the screen
        self.add_widget(self.preview())
        self.add_widget(self.module_id)
        self.add_widget(self.module_title)
        self.add_widget(self.playButton())
        # self.add_widget(MDLabel(text="Progress", pos_hint={"center_x": 0.2, "top": 0.6}, size_hint=card_style["size"], theme_text_color=card_style["theme"], font_style="Caption", halign="center"))
        # self.add_widget(self.module(0)) # TODO: get module number
        # self.add_widget(self.progress(50))  # TODO: get progress

    # load module screen
    def load_module(self, instance):
        self.sm.screens[3].ids.user = self.selected_user
        self.sm.screens[3].ids.module_number = self.module.get("id")
        self.sm.current = 'module'

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def preview(self):
        return FitImage(source=self.module.get("preview"),size_hint=(1, .55),pos_hint={"center_x": module_card_style["center_x"], "top": 1})

    def generateCardLabel(self, label, style, height):
        return MDLabel(text=label, \
          pos_hint={"center_x": module_card_style["center_x"], "top": height}, \
            size_hint=module_card_style["size"], \
              theme_text_color=module_card_style["theme"], \
                font_style=style, halign="center")

    def playButton(self):
        bt = RoundButton(text="Play", color=(0,0,0,1), font_size= '15sp', \
          bold= True, \
            pos_hint={"center_x": module_card_style["center_x"], "top": 0.2},\
              size_hint=(.5, .15))
        bt.bind(on_press=self.load_module)
        return bt
