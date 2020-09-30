#import kivy
import json
import random
from components.Question import Question


class DragAndDrop(Question):

    def __init__(self, question_id, question_text, question_audio, explanation_text, explanation_audio,
                 ordered_image_ids, current_answer, on_complete):
        Question.__init__(self, question_id, question_text,
                          question_audio, explanation_text, explanation_audio)
        self.ordered_image_ids = ordered_image_ids
        self.current_answer = current_answer
        self.on_complete = on_complete

    def render_question(self):
        pass

    def verify(self):
        if len([i for i in range(len(self.current_answer)) if self.current_answer[i] == self.ordered_image_ids[i]]) == \
                len(self.current_answer):
            self.on_complete()
        return

    def __str__(self):
        ret = ''
        for i in self.assessment:
            ret = ret + '\n Question: '
            ret = ret + ' ' + 'Text: ' + i.question_text + ' ' + 'ID: ' + str(i.question_id) + ' ' + \
                'Audio: ' + i.question_audio + ' ' + \
                'Expl Text: ' + i.explanation_text + ' ' + 'Expl Audio: ' + i.explanation_audio
        return ret
