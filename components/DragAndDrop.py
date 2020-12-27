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
        self.question = Question(question_id=kwargs['question_id'], question_text=kwargs['question_text'],
                          question_audio=kwargs['question_audio'], explanation_text=kwargs['explanation_text'],
                          explanation_audio=kwargs['explanation_audio'])
        self.ordered_image_ids = kwargs['ordered_image_ids']
        self.current_answer = kwargs['current_answer']
        self.on_complete = kwargs['on_complete']
        self.on_attempt = kwargs['on_attempt']
        self.explanation_audio = SoundLoader.load(self.question.explanation_audio)
        self.explanation_audio.bind(on_stop=self.on_explanation_audio_finish)

        if self.question.question_audio is not None:
            self.question_audio = SoundLoader.load(self.question.question_audio)
            self.question_audio.bind(on_stop=self.on_question_audio_finish)
        else:
            self.question_audio =  None

    def _get_id(self, id):
        id_dict = {
        '1': self.ids.box_1,
        '2': self.ids.box_2,
        '3': self.ids.box_3
        }
        return id_dict.get(id, "ERROR")

    def _replace_image(self, id):
        self.ordered_image_ids[int(id) + 2] = self.ordered_image_ids[int(id) - 1]

    def call_back(self, id, *largs):
        self._replace_image(id)

    def correct(self, calling_widget):
        self.current_answer.append(calling_widget)
        Clock.schedule_once(partial(self.call_back, calling_widget.text), 0.1)
        if len(self.current_answer) == len(self.ordered_image_ids)//2:
            self.on_attempt()

            #stop playing the question if it is still going on
            if not self.question_audio is None:
                self.question_audio.stop()

            #play the explanation
            self.explanation_audio.play()

    def wrong(self, the_widget=None, parent=None, kv_root=None):
        self.on_attempt()

    def on_explanation_audio_finish(self, sound):
        self.explanation_audio.unload()
        self.on_complete()

    def on_question_audio_finish(self, sound):
        self.question_audio.unload()
        self.question_audio = None

    def play_question_audio(self):
        if(not self.question_audio is None):
            self.question_audio.play()