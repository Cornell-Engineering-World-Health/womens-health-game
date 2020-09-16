import kivy
import json
import random


class Question():
    def __init__(self, question_text, question_id, question_audio):
        self.question_text = question_text
        self.question_id = question_id
        self.question_audio = question_audio
        self.explanation_text = None
        self.explanation_audio = None

    #plays question audio
    def play_question_audio(self):
        pass

    #plays answer audio
    def play_answer_audio(self):
        pass
