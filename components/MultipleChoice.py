import kivy
import json
import random
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.uix.button import Button
from components.Question import Question
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout


from kivy.lang import Builder
class Button(Button):
    def __init__(self, **kw):
        super(Button, self).__init__(**kw)

class MultipleChoice(BoxLayout):

    Builder.load_file("kv/multiplechoice.kv")

    def __init__(self, **kwargs):
        super().__init__()
        Question.__init__(self, question_id=kwargs['question_id'], question_text=kwargs['question_text'], question_audio=kwargs['question_audio'], explanation_text=kwargs['explanation_text'],explanation_audio=kwargs['explanation_audio'])
        self.image_options = kwargs['image_options']
        self.correct_answer = kwargs['explanation_text'].split(", ")
        self.on_complete = kwargs['on_complete']
        self.selected_choices = []
        self.feedback = 'Select all that apply.'

    def selected(self, button):
        self.ids[button].background_color = (0 , 0, 1, 1)

    def incorrect(self):
        self.feedback = 'Sorry, that was incorrect. Explanation: ' + self.explanation_text
        self.ids['submit'].text = 'Press to Continue'

    def choose(self, txt):
        self.selected_choices.append(txt)

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
        if set(self.selected_choices) == set(self.correct_answer)  or self.ids['submit'].text == 'Press to Continue':
            self.ids['feedback'].text = 'Correct! ' + self.explanation_text
            self.on_complete()
        else:
            self.incorrect()



