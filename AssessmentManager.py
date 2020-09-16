import kivy
import json
import random


class AssessmentManager:
    def __init__(self, module_number, asssessment, current_question):
        self.module_number = module_number
        self.assessment = assessment #list of Question types
        self.current_question = current_question
        self.load()

    def _load(self, module_number: int):
        pass

    def advance_question(self):
        pass

    def render_question(self):
        return
