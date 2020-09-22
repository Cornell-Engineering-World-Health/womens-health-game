import kivy
import json
import random
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

class AssessmentManager(Screen):
    def __init__(self, **kw):

        #self.module_number = module_number
        #self.assessment = assessment #list of Question types
        #self.current_question = current_question

        super().__init__(**kw)
        self.app = MDApp.get_running_app()


        #self._load()
        
    # built in kivy function that runs before scene is loaded
    def on_pre_enter(self, *args):

        # loads the current user data into user
        if len(self.manager.screens[2].ids) > 0:
            self.user = self.manager.screens[2].ids.user
            self.app.title = "Health Friend [Assessment]  ::  " + self.user['first_name'] + " " + self.user['last_name']
        else:
            self.app.title = "Health Friend [Assessment]  ::  EWH"




    def _load(self, module_number: int):
        pass

    def advance_question(self):
        pass

    def render_question(self):
        return
