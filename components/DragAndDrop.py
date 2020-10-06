#import kivy
import json
import random
from components.Question import Question
from kivy.uix.button import Button

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivydnd.dragndropwidget import DragNDropWidget

class  DraggableButton(Button, DragNDropWidget):
    def __init__(self, **kw):
        super(DraggableButton, self).__init__(**kw)

class DragAndDrop(BoxLayout, Question):

    Builder.load_file('kv/draganddrop.kv')

    def __init__(self, **kwargs):
        Question.__init__(self, question_id=kwargs['question_id'], question_text=kwargs['question_text'],
                          question_audio=kwargs['question_audio'], explanation_text=kwargs['explanation_text'],
                          explanation_audio=kwargs['explanation_audio'])
        self.ordered_image_ids = kwargs['ordered_image_ids']
        self.current_answer = kwargs['current_answer']
        self.on_complete = kwargs['on_complete']

    def correct(self, calling_widget):
        print ("Correct!")

    def wrong(self, the_widget=None, parent=None, kv_root=None):
        print("Wrong place!")

    def render_question(self):
        pass

    def verify(self):
        if len([i for i in range(len(self.current_answer)) if self.current_answer[i] == self.ordered_image_ids[i]]) == \
                len(self.current_answer):
            self.on_complete()

    def __str__(self):
        ret = ''
        for i in self.assessment:
            ret = ret + '\n Question: '
            ret = ret + ' ' + 'Text: ' + i.question_text + ' ' + 'ID: ' + str(i.question_id) + ' ' + \
                'Audio: ' + i.question_audio + ' ' + \
                'Expl Text: ' + i.explanation_text + ' ' + 'Expl Audio: ' + i.explanation_audio
        return ret

