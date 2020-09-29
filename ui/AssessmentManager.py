import kivy
import json
from components.MultipleChoice import MultipleChoice
from components.DragAndDrop import DragAndDrop
from kivy.uix.gridlayout import GridLayout
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button


class AssessmentManager(Screen, App):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

        self.user = None
        self.module_number = 0
        self.assessment = [] #list of Question types
        self.index = 0
        self.current_question = self.assessment[self.index]
        
    # built in kivy function that runs before scene is loaded
    def on_pre_enter(self, *args):

        # loads the current user data into user
        ids = self.manager.screens[3].ids
        if len(ids) > 2:
            self.user = ids.user
            self.module_number = ids.module_number
            self.assessment = ids.assessment
            self.   app.title = "Health Friend [Assessment]  ::  " + self.user['first_name'] + " " + self.user['last_name']
        else:
            self.app.title = "Health Friend [Assessment]  ::  EWH"
        self._load(self.module_number)

    def advance_question(self):
        self.index+=1


    def _load(self, module_number: int):
        print('loading', module_number)
        with open() as file:
            data = json.loads(file)
        question_dict = data['questions']
        for question in question_dict:
            if question["type"] == 'multiple_choice':
                new_question = MultipleChoice(question['question_text'], question['question_id'],
                                              question['question_audio'], question["explanation_text"],
                                              question["explanation_audio"], question["image_options"],
                                              question["selected_choices"], lambda x: x.advance_question())
            if question["type"] == "drag_and_drop":
                new_question = DragAndDrop(question['question_text'], question['question_id'],
                                           question['question_audio'], question["explanation_text"],
                                           question["explanation_audio"], question["ordered_image_ids"],
                                           question["current_answer"], lambda x: x.advance_question)
            self.assessment.append(new_question)
        return

    def __str__(self):
        ret = ''
        for i in self.assessment:
            ret = ret + '\n Question: '
            ret = ret + ' ' + 'Text: ' + i.question_text + ' ' + 'ID: ' + str(i.question_id) + ' ' + \
                  'Audio: ' + i.question_audio + ' ' + \
                  'Expl Text: ' + i.explanation_text + ' ' + 'Expl Audio: ' + i.explanation_audio
        return ret

class Grid(GridLayout):
    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.add_widget(Label(text=self.current_question.question_text))
        self.next = Button(text="Submit", font_size=40)
        self.next.bind(on_press=self.press)
        self.add_widget(self.next)

    def press(self, instance):
        self.advance_question()
        return Grid

class Run(App):
    def build(self):
        return Grid




