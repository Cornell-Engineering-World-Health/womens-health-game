import kivy
from Question import Question


class DragAndDrop(Question):

    def __init__(self, question_text, question_id, question_audio, explanation_text, explanation_audio,
                 ordered_image_ids, current_answer):
        Question.__init__(self, question_text, question_id, question_audio, explanation_text, explanation_audio)
        self.ordered_image_ids = ordered_image_ids
        self.current_answer = current_answer

    def render_question(self):
        pass

    def verify(self):
        return [i for i in range(len(self.current_answer)) if self.current_answer[i] == self.ordered_image_ids[i]]

    def __str__(self):
        ret = ''
        ret = ret + ' ' + 'Text: ' + self.question_text + ' ' + 'ID: ' + str(self.question_id) + ' ' + \
                  'Audio: ' + self.question_audio + ' ' + \
                  'Expl Text: ' + self.explanation_text + ' ' + 'Expl Audio: ' + self.explanation_audio
        return ret


