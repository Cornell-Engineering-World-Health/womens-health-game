import kivy
import json
import random
from components.MultipleChoice import MultipleChoice
from components.DragAndDrop import DragAndDrop
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen


class AssessmentManager(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

        self.user = None
        self.module_number = 0
        self.assessment = []  # list of Question types
        self.current_question = ""

    # built in kivy function that runs before scene is loaded
    def on_pre_enter(self, *args):

        # loads the current user data into user
        ids = self.manager.screens[3].ids
        if len(ids) > 2:
            self.user = ids.user
            self.module_number = ids.module_number
            self.assessment = ids.assessment
            self.   app.title = "Health Friend [Assessment]  ::  " + \
                self.user['first_name'] + " " + self.user['last_name']
        else:
            self.app.title = "Health Friend [Assessment]  ::  EWH"
        self._load(self.module_number)

    def _load(self, module_number: int):
        filepath = "assets/json/questions" + str(module_number) + ".json"
        with open(filepath) as file:
            data = json.load(file)
        question_dict = data['questions']
        for question in question_dict:
            if question["type"] == 'multiple_choice':
                new_question = MultipleChoice(question['question_text'], question['question_id'],
                                              question['question_audio'], question["explanation_text"],
                                              question["explanation_audio"], question["image_options"],
                                              question["correct_answer"])

            if question["type"] == "drag_and_drop":
                new_question = DragAndDrop(question['question_text'], question['question_id'],
                                           question['question_audio'], question["explanation_text"],
                                           question["explanation_audio"], question["ordered_image_ids"],
                                           question["current_answer"])
            self.assessment.append(new_question)
        return

    def advance_question(self):
        pass

    def render_question(self):
        return

    def __str__(self):
        ret = ''
        for i in self.assessment:
            ret = ret + '\n Question: '
            ret = ret + ' ' + 'Text: ' + i.question_text + ' ' + 'ID: ' + str(i.question_id) + ' ' + \
                'Audio: ' + i.question_audio + ' ' + \
                'Expl Text: ' + i.explanation_text + ' ' + 'Expl Audio: ' + i.explanation_audio
        return ret
