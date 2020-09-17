#import kivy
import json
import random
from Question import Question


class DragAndDrop(Question):

    def __init__(self, question_id, question_text, question_audio, explanation_text, explanation_audio,
                 ordered_image_ids, current_answer):
        Question.__init__(self, question_id, question_text, question_audio)
        self.explanation_text = explanation_text
        self.explanation_audio = explanation_audio
        self.default_current_answer = []
        self.ordered_image_ids = ordered_image_ids
        self.current_answer = current_answer

    def render_question(self):
        pass

    def verify(self):
        return [i for i in range(len(self.current_answer)) if self.current_answer[i] == self.ordered_image_ids[i]]

