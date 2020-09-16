import kivy
import json
import random
from Question import Question

class DragAndDrop(Question):
    def __init__(self, ordered_image_ids, current_answer):
        self.question_text = Question.question_text
        self.question_id = Question.question_id
        self.question_audio = Question.question_audio
        self.default_current_answer = []
        self.ordered_image_ids = ordered_image_ids
        self.current_answer = current_answer

    def render_question(self):
        pass

    def verify(self):
        return [i for i in range(len(self.current_answer)) if
        self.current_answer[i] == self.ordered_image_ids[i]]:
