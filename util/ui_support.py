from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.button import Button

kv="""
<RoundButton@Button>:
    background_color: (0,0,0,0)
    background_normal: ''
    back_color: (0.925,0.786,0.27,1)
    border_radius: [50,]
    canvas.before:
        Color:
            rgba: self.back_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: self.border_radius
"""

class RoundButton(Button):
    pass

Builder.load_string(kv)
