#import kivy
import json
import random


class Question():
    def __init__(self, **kwargs):
        self.question_text = kwargs["question_text"]
        self.question_id = kwargs["question_id"]
        self.question_audio = kwargs['question_audio']
        self.explanation_text = kwargs['explanation_text']
        self.explanation_audio = kwargs['explanation_audio']

    #plays question audio
    def play_question_audio(self):
        pass

    #plays answer audio
    def play_answer_audio(self):
        pass
