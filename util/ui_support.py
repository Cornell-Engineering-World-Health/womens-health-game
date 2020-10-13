from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.button import Button

# kv="""
# <RoundedButton@Button>:
#     background_color: 0,0,0,0
#     canvas.before:
#         Color:
#             rgba: (.4,.4,.4,1) if self.state=='normal' else (0,.7,.7,1)  # visual feedback of press
#         RoundedRectangle:
#             pos: self.pos
#             size: self.size
#             radius: [50,]

# """
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

class RoundedButton(Button):
    pass

Builder.load_string(kv)
