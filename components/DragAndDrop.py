#import kivy
import json
import random
from kivy.core.audio import SoundLoader
from components.Question import Question
from kivy.uix.button import Button
from kivy.uix.image import Image

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivy.properties import ListProperty

from kivydnd.dragndropwidget import DragNDropWidget
from kivy.clock import Clock
from functools import partial


class  DraggableButton(Button, DragNDropWidget):
    def __init__(self, **kw):
        super(DraggableButton, self).__init__(**kw)


class DragAndDrop(BoxLayout):
    ordered_image_ids = ListProperty(["", "", "", "", "", ""])
    current_answer = []
    def __init__(self, **kwargs):
        super().__init__()
        Question.__init__(self, question_id=kwargs['question_id'], question_text=kwargs['question_text'],
                          question_audio=kwargs['question_audio'], explanation_text=kwargs['explanation_text'],
                          explanation_audio=kwargs['explanation_audio'])
        self.ordered_image_ids = kwargs['ordered_image_ids']
        self.current_answer = kwargs['current_answer']
        self.on_complete = kwargs['on_complete']
        self.on_attempt = kwargs['on_attempt']
        self.explanation_audio = SoundLoader.load(self.explanation_audio)

    def _get_id(self, id):
        id_dict = {
        '1': self.ids.box_1,
        '2': self.ids.box_2,
        '3': self.ids.box_3
        }
        return id_dict.get(id, "ERROR")

    def _replace_image(self, id):
        old_widget = self._get_id(id)
        self.ids.to_box.remove_widget(old_widget)
        self.ids.to_box.add_widget(Image(source=self.ordered_image_ids[int(id) - 1], size=(250, 350)),index=(3 - int(id)))

    def call_back(self, id, *largs):
        self._replace_image(id)

    def correct(self, calling_widget):
        self.current_answer.append(calling_widget)
        #Clock.schedule_once(partial(self.call_back, calling_widget.text), 1)
        if len(self.current_answer) == len(self.ordered_image_ids)//2:
            self.on_attempt()
            self.explanation_audio.stop()
            self.on_complete()

    def wrong(self, the_widget=None, parent=None, kv_root=None):
        self.explanation_audio.play()
        self.on_attempt()
