#import kivy
import json
import random
from kivy.core.audio import SoundLoader
from components.Question import Question
from kivy.uix.button import Button

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivy.properties import ListProperty

from kivydnd.dragndropwidget import DragNDropWidget

class  DraggableButton(Button, DragNDropWidget):
    def __init__(self, **kw):
        super(DraggableButton, self).__init__(**kw)

class DragAndDrop(BoxLayout):

    ordered_image_ids = ListProperty(["", "", ""])

    def __init__(self, **kwargs):
        Builder.load_file('kv/draganddrop.kv')
        super().__init__()
        Question.__init__(self, question_id=kwargs['question_id'], question_text=kwargs['question_text'],
                          question_audio=kwargs['question_audio'], explanation_text=kwargs['explanation_text'],
                          explanation_audio=kwargs['explanation_audio'])
        self.ordered_image_ids = kwargs['ordered_image_ids']
        self.current_answer = kwargs['current_answer']
        self.on_complete = kwargs['on_complete']
        self.question_audio = SoundLoader.load(self.question_audio)
        self.explanation_audio = SoundLoader.load(self.explanation_audio)




    def correct(self, calling_widget):
        self.current_answer.append(calling_widget)
        print(self.current_answer)
        if len(self.current_answer) == len(self.ordered_image_ids):
            self.explanation_audio.stop()
            self.on_complete()
        print ("Correct!")

    def wrong(self, the_widget=None, parent=None, kv_root=None):
        self.explanation_audio.play()
        print("Wrong place!")



