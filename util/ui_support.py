from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.button import Button

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import StringProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import RoundedRectangle

kv="""
<RoundButton@Button>:
    do_scale: False
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
            radius: [50]
"""

class RoundButton(Button):
    pass

Builder.load_string(kv)

#https://gist.github.com/benni12er/95a45eb168fc33a4fcd2d545af692dad
class FitImage(BoxLayout):
    source = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._late_init)

    def _late_init(self, *args):
        self.container = Container(self.source)
        self.add_widget(self.container)


class Container(Widget):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.adjust_size)
        self.image = Image(source=source)

    def adjust_size(self, *args):
        (par_x, par_y) = self.parent.size

        if par_x == 0 or par_y == 0:
            with self.canvas:
                self.canvas.clear()
            return

        par_scale = par_x / par_y

        (img_x, img_y) = self.image.texture.size
        img_scale = img_x / img_y

        if par_scale > img_scale:
            (img_x_new, img_y_new) = (img_x, img_x / par_scale)
        else:
            (img_x_new, img_y_new) = (img_y * par_scale, img_y)

        crop_pos_x = (img_x - img_x_new) / 2
        crop_pos_y = (img_y - img_y_new) / 2

        subtexture = self.image.texture.get_region(crop_pos_x, crop_pos_y, img_x_new, img_y_new)

        with self.canvas:
            self.canvas.clear()
            Color(1, 1, 1)
            RoundedRectangle(texture=subtexture, pos=self.pos, size=(par_x, par_y))

