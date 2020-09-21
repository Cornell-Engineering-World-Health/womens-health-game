import kivy
import json
import random


class AssessmentManager:
    def __init__(self, module_number, assessment, current_question):
        self.module_number = module_number
        self.assessment = assessment #list of Question types
        self.current_question = current_question
        self._load()

    def _load(self, module_number: int):
        with open() as file:
            data = json.loads(file)
        question_dict = data['questions']
        for question in question_dict:
            if question["type"] == 'multiple_choice':
                new_question = MultipleChoice(question['question_text'], question['question_id'],
                                              question['question_audio'], question["explanation_text"],
                                              question["explanation_audio"], question["image_options"],
                                              question["selected_choices"])
            else:
                new_question = DragAndDrop(question['question_text'], question['question_id'],
                                           question['question_audio'], question["explanation_text"],
                                           question["explanation_audio"], question["ordered_image_ids"],
                                           question["current_answer"])
            self.assessment.append(new_question)
        return

    def advance_question(self):
        pass

    def render_question(self):
        return

    def __str__(self):
        ret = ''
        for i in self.assessment:
            ret = ret + '\n Question: '
            ret = ret + ' ' + 'Text: ' + i.question_text + ' ' + 'ID: ' + str(i.question_id) + ' ' + \
                  'Audio: ' + i.question_audio + ' ' + \
                  'Expl Text: ' + i.explanation_text + ' ' + 'Expl Audio: ' + i.explanation_audio
        return ret
