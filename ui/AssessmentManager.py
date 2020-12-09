import json
from components.MultipleChoice import MultipleChoice
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from components.DragAndDrop import DragAndDrop
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from util.store import update_assessment_state, complete_question_state, current_assessment_state

class AssessmentManager(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        self.user = None
        self.module_number = 0
        self.assessment = []  # list of Question types
        self.index = -1
        self.current_question_attempts = 0
        self.current_question_text = ''
        self.current_question = ""
        self.types = []
        self.grid = None
        Clock.schedule_once(self.finished_init)

    def finished_init(self, *args):
        self.grid = self.ids.assessment_grid
        self._load(self.module_number)

    def on_pre_enter(self, *args):
        # loads the current user data into user if they exist
        # Pre-existing id: float (FloatLayout id)
        if len(self.ids) > 1:
            self.user = self.ids.user
            self.module_number = self.ids.module_number
            self.app.title = "Health Friend [Game]  ::  " + \
                self.user['first_name'] + " " + self.user['last_name']
        else:
            self.app.title = "Health Friend [Game]  ::  EWH"

        self.load_local_storage()

    # TODO: load in current state and override other values
    def load_local_storage(self):
        state = current_assessment_state(self.user['id'], self.module_number)
        print("STATE", state)
        pass

    def _load(self, module_number: int):
        filepath = "assets/json/questions" + str(module_number) + ".json"
        with open(filepath) as file:
            data = json.load(file)
        question_dicts = data['questions']
        for question in question_dicts:
            if question["type"] == 'multiple_choice':
                self.types.append(1)
                new_question = MultipleChoice(question_text = question['question_text'], question_id =question['question_id'],
                            question_audio = question['question_audio'], explanation_text = question["explanation_text"],
                            explanation_audio = question["explanation_audio"], image_options = question["image_options"],
                            correct_answer = question["correct_answer"], choices = question['choices'], on_complete = self.advance_question, on_attempt = self.attempt)
            if question["type"] == "drag_and_drop":
                self.types.append(0)
                new_question = DragAndDrop(question_text = question['question_text'], question_id = question['question_id'],
                                           question_audio = question['question_audio'], explanation_text = question["explanation_text"],
                                           explanation_audio = question["explanation_audio"], ordered_image_ids = question["ordered_image_ids"],
                                           current_answer = question["current_answer"], on_complete = self.advance_question, on_attempt = self.attempt)
            self.assessment.append(new_question)


    def advance_question(self):
        self.grid.clear_widgets()
        if self.index < len(self.assessment) - 1:
            # update question state to complete (user_id, module_id, question_id)
            if(self.index >= 0):
                complete_question_state(self.user['id'], self.module_number, self.index)
                self.current_question_attempts = 0
            self.index = self.index + 1
            self.render_question()
        else:
            self.on_assessment_complete()

    def on_assessment_complete(self):
        print("DONE")
        self.manager.current = "menu_screen"

    def attempt(self):
        # update question state to reflect attempt change (user_id, module_id, question_id, attempts)
        self.current_question_attempts += 1
        update_assessment_state(self.user['id'], self.module_number, self.index, self.current_question_attempts)

    def render_question(self):
        curr = self.assessment[self.index]
        self.grid.add_widget(curr)
        question_audio = SoundLoader.load("rushes.wav")
        question_audio.play()

    def __str__(self):
        ret = ''
        for i in self.assessment:
            ret = ret + '\n Question: '
            ret = ret + ' ' + 'Text: ' + i.question_text + ' ' + 'ID: ' + str(i.question_id) + ' ' + \
                'Audio: ' + i.question_audio + ' ' + \
                'Expl Text: ' + i.explanation_text + ' ' + 'Expl Audio: ' + i.explanation_audio
        return ret
