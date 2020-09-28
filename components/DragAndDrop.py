#import kivy
import json
import random
#from Question import Question

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class DragAndDrop(DraggableLayoutBehavior, BoxLayout):

    '''
    def __init__(self, question_id, question_text, question_audio, explanation_text, explanation_audio,
                 ordered_image_ids, current_answer):
        Question.__init__(self, question_id, question_text, question_audio, explanation_text, explanation_audio)
        self.ordered_image_ids = ordered_image_ids


        self.current_answer = current_answer
    '''

    def __init__(self, **kw):
        super().__init__(**kw)


    def render_question(self):
        pass

    def verify(self):
        return [i for i in range(len(self.current_answer)) if self.current_answer[i] == self.ordered_image_ids[i]]

    def __str__(self):
        ret = ''
        for i in self.assessment:
            ret = ret + '\n Question: '
            ret = ret + ' ' + 'Text: ' + i.question_text + ' ' + 'ID: ' + str(i.question_id) + ' ' + \
                  'Audio: ' + i.question_audio + ' ' + \
                  'Expl Text: ' + i.explanation_text + ' ' + 'Expl Audio: ' + i.explanation_audio
        return ret

    def compare_pos_to_widget(self, widget, pos):
        if self.orientation == 'vertical':
            return 'before' if pos[1] >= widget.center_y else 'after'
        return 'before' if pos[0] < widget.center_x else 'after'

    def handle_drag_release(self, index, drag_widget):
        self.add_widget(drag_widget, index)


class DragLabel(DraggableObjectBehavior, Label):

    def initiate_drag(self):
        # during a drag, we remove the widget from the original location
        self.parent.remove_widget(self)
