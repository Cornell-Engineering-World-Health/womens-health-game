import json
from components.MultipleChoice import MultipleChoice
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from components.DragAndDrop import DragAndDrop
from kivy.clock import Clock
from kivy.core.audio import SoundLoader



class AssessmentManager(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        self.user = None
        self.module_number = 0
        self.assessment = []  # list of Question types
        self.index = -1
        self.current_question_text = ''
        self.current_question = ""
        self.grid = None
        Clock.schedule_once(self.finished_init)
        
    # built in kivy function that runs before scene is loaded
    def finished_init(self, *args):
        # loads the current user data into user
        ids = self.ids
        if len(ids) > 2:
            self.user = ids.user
            self.module_number = ids.module_number
            self.app.title = "Health Friend [Assessment]  ::  " + self.user['first_name'] + " " + self.user['last_name']
        else:
            self.app.title = "Health Friend [Assessment]  ::  EWH"
        self.grid = self.ids.assessment_grid
        self._load(self.module_number)



    def _load(self, module_number: int):
        filepath = "assets/json/questions0.json"
        with open(filepath) as file:
            data = json.load(file)
        question_dicts = data['questions']
        for question in question_dicts:
            if question["type"] == 'multiple_choice':
                new_question = MultipleChoice(question_text = question['question_text'], question_id =question['question_id'],
                            question_audio = question['question_audio'], explanation_text = question["explanation_text"],
                            explanation_audio = question["explanation_audio"], image_options = question["image_options"],
                            correct_answer = question["correct_answer"], choices = question['choices'], on_complete = self.advance_question)
            if question["type"] == "drag_and_drop":
                new_question = DragAndDrop(question_text = question['question_text'], question_id = question['question_id'],
                                           question_audio = question['question_audio'], explanation_text = question["explanation_text"],
                                           explanation_audio = question["explanation_audio"], ordered_image_ids = question["ordered_image_ids"],
                                           current_answer = question["current_answer"], on_complete = self.advance_question)
            self.assessment.append(new_question)


    def advance_question(self):
        self.grid.clear_widgets()
        if self.index < len(self.assessment) - 1:
            self.index = self.index + 1
            self.render_question()
        else:
            self.manager.current = "module"


    def render_question(self):
        curr = self.assessment[self.index]
        self.grid.add_widget(curr)
        question_audio = SoundLoader.load(curr.question_audio)
        question_audio.play()




    def __str__(self):
        ret = ''
        for i in self.assessment:
            ret = ret + '\n Question: '
            ret = ret + ' ' + 'Text: ' + i.question_text + ' ' + 'ID: ' + str(i.question_id) + ' ' + \
                'Audio: ' + i.question_audio + ' ' + \
                'Expl Text: ' + i.explanation_text + ' ' + 'Expl Audio: ' + i.explanation_audio
        return ret




