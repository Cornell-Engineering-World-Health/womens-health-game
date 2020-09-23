import kivy
import json
import random
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

class AssessmentManager(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

        self.user = None
        self.module_number = 0
        self.assessment = [] #list of Question types
        self.current_question = ""
        
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


    def _load(self, module_number: int):
        print('loading', module_number)

    def advance_question(self):
        pass

    def render_question(self):
        return
