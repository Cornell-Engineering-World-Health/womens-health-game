import kivy
import json
import random
from Question import Question



class MultipleChoice(Question):
    def __init__(self, image_options, correct_answer, selected_choices):
        self.question_text = Question.question_text
        self.question_id = Question.question_id
        self.question_audio = Question.question_audio
        self.image_options = image_options
        self.correct_answer = currect_answer
        assert [i for i in self.correct_answer not in self.image_options] == []
        self.selected_choices = selected_choices

    # returns kivy element for this question, renders image_options
    def render_question(self):
        pass

    def verify(self):
        return set(self.selected_choices) == set(self.correct_answer)
