from kivy.properties import ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
import kivy
import json
import random
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from components.card import Card
from components.Question import Question
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader



class MultipleChoice(GridLayout):
    choices = ListProperty(["", "", "", ""])
    question_text = StringProperty("")
    selected = []
    def __init__(self, **kwargs):
        Builder.load_file('kv/multiplechoice.kv')
        super().__init__()
        Question.__init__(self, question_id=kwargs['question_id'], question_text=kwargs['question_text'],
                          question_audio=kwargs['question_audio'], explanation_text=kwargs['explanation_text'],
                          explanation_audio=kwargs['explanation_audio'])
        self.choices = kwargs['choices']
        self.image_options = kwargs['image_options']
        self.selected = []
        self.correct_answer = kwargs['correct_answer']
        self.on_complete = kwargs['on_complete']
        self.question_audio = SoundLoader.load(self.question_audio)
        self.explanation_audio = SoundLoader.load(self.explanation_audio)




    def verify(self):
        if set(self.correct_answer) == set(self.selected):
            self.ids["feedback"].text = "Correct!"
            self.explanation_audio.stop()
            self.on_complete()
        else:
            self.ids["feedback"].text = "Incorrect"
            self.explanation_audio.play()




