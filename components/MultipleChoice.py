from kivy.properties import ListProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from components.Question import Question
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.properties import StringProperty



class MultipleChoice(GridLayout):
    choices = ListProperty(["", "", "", ""])
    question_text = StringProperty("")
    selected = []
    def __init__(self, **kwargs):
        super().__init__()
        Question.__init__(self, question_id=kwargs['question_id'], question_text=kwargs['question_text'],
                          question_audio=kwargs['question_audio'], explanation_text=kwargs['explanation_text'],
                          explanation_audio=kwargs['explanation_audio'])
        self.choices = kwargs['choices']
        self.image_options = kwargs['image_options']
        self.selected = []
        self.correct_answer = kwargs['correct_answer']
        self.on_complete = kwargs['on_complete']
        Builder.load_file('kv/multiplechoice.kv')


    def verify(self):
        if set(self.correct_answer) == set(self.selected):
            self.ids["feedback"].text = "Correct!"
            self.on_complete
        else:
            self.ids["feedback"].text = "Incorrect"





