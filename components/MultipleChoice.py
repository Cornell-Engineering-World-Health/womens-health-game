import kivy
import json
import random
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from components.card import Card, CardButton
from components.Question import Question
from kivy.uix.togglebutton import ToggleButton

from kivy.lang import Builder


class MultipleChoice(Question):

    Builder.load_file('kv/multiplechoice.kv')

    def __init__(self, **kwargs):
        Question.__init__(self, question_id=kwargs['question_id'], question_text=kwargs['question_text'], question_audio=kwargs['question_audio'], explanation_text=kwargs['explanation_text'],explanation_audio=kwargs['explanation_audio'])
        self.image_options = kwargs['image_options']
        self.correct_answer = kwargs['correct_answer']
        self.on_complete = kwargs['on_complete']
        self.selected_choices = []



    # returns kivy element for this question, renders image_options
    def render_question(self):
        #grid = self.manager.screens[1].ids.grid_card
        #grid.add_widget(self.question_text)
        #for options in self.image_options:
            #choice = ToggleButton(screen_manager=self.manager, image=options)
            #grid.add_widget(choice)
        pass

    def toggle_button(self):
        # choice = state = 'down'
        # update grid
        pass

    def verify(self):
        if set(self.selected_choices) == set(self.correct_answer):
            self.on_complete()

    def __str__(self):
        ret = ''
        for i in self.assessment:
            ret = ret + '\n Question: '
            ret = ret + ' ' + 'Text: ' + i.question_text + ' ' + 'ID: ' + str(i.question_id) + ' ' + \
                'Audio: ' + i.question_audio + ' ' + \
                'Expl Text: ' + i.explanation_text + ' ' + 'Expl Audio: ' + i.explanation_audio
        return ret
