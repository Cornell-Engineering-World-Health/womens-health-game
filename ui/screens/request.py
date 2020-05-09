# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.button import Button

# util imports
from util.client import api_call
import json


class RequestScreen(Screen):
    def __init__(self, **kwargs):
        super(RequestScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        self.clear_widgets()

        # define a button
        requestButton = Button(text='USER REQUEST', font_size=30)

        # bind button with callback method
        requestButton.bind(on_press=self.callback)

        self.add_widget(requestButton)

        self.do_layout()

    def change_screen(self, screen):
        self.manager.current = screen

    # callback method makes api_calls
    def callback(self, instance):

    	# EXAMPLE GET REQUEST
        # api_call('users')

        # EXAMPLE POST REQUEST
        raw_data = {'user_id':'00', 'question_id':'00', 'correct':True, 'attempt_num': 1}
        data = json.dumps(raw_data) 
        api_call('progress', data)
