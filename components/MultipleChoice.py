import kivy
import json
import random
from Question import Question

from kivy.lang import Builder



class MultipleChoice():

    Builder.load_file('kv/multiplechoice.kv')

    def __init__(self, **kwargs):
        super().__init__()
        Question.__init__(self, question_id=kwargs['question_id'], question_text=kwargs['question_text'], question_audio=kwargs['question_audio'], explanation_text=kwargs['explanation_text'],explanation_audio=kwargs['explanation_audio'])
        self.image_options = kwargs['image_options']
        self.correct_answer = kwargs['correct_answer']
        assert [i for i in self.correct_answer not in self.image_options] == []
        self.selected_choices = []

    # returns kivy element for this question, renders image_options
    def render_question(self):
        pass

    def verify(self):
        return set(self.selected_choices) == set(self.correct_answer)

    def __str__(self):
        ret = ''
        for i in self.assessment:
            ret = ret + '\n Question: '
            ret = ret + ' ' + 'Text: ' + i.question_text + ' ' + 'ID: ' + str(i.question_id) + ' ' + \
                  'Audio: ' + i.question_audio + ' ' + \
                  'Expl Text: ' + i.explanation_text + ' ' + 'Expl Audio: ' + i.explanation_audio
        return ret