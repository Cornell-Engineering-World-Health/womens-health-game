#import kivy
import json
import random
from components.Question import Question
from kivy.uix.button import Button
from kivy.uix.image import Image

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
        self.ids.to_box.add_widget(Image(source='assets/drag-and-drop/shape' + id + '.png'), index=(3 - int(id)))

    def correct(self, calling_widget):
        self.current_answer.append(calling_widget)
        self._replace_image(calling_widget.text)
        print(self.current_answer)
        if len(self.current_answer) == len(self.ordered_image_ids):
            self.on_complete()
        print ("Correct!")

    def wrong(self, the_widget=None, parent=None, kv_root=None):
        print("Wrong place!")
