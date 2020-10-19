# App Styling
#from ui.AssessmentManager import AssessmentManager
import json

def get_dnd_images(module_number, question_index):
	filepath = "assets/json/questions" + str(module_number) + ".json"
	with open(filepath) as file:
		data = json.load(file)
	questions = data['questions']
	dnd = [questions[x]['ordered_image_ids'] for x in range(len(questions)) if questions[x]['type'] == 'drag_and_drop']
	return dnd[question_index]

app_style = {
	"primary_theme": "Red",
	"assessment_background": [0.870, 0.678, 0.502,1],
	"button_color": [0.647, 0.196, .137],
}

card_style = {
	"radius": [(40.0, 40.0), (40.0, 40.0), (40.0, 40.0), (40.0, 40.0)],
	"background_color": (0, 0, .4, 0.1),
	"center_x": .5,
	"size": (.5, .3),
	"first_name_y": 0.9,
	"last_name_y": 0.8,
	"village_name_y": 0.6,
	"title_font": "H6",
	"subtitle_font": "H5",
	"theme": "Primary"
}

dnd_from_style = {
	"size_hint": (.3,.1),
	"background_color": [0,0,0,0],
	"sources": get_dnd_images(0, 0),
	"layout_size_x": .7,
	"layout_size_y": .5,
	"spacing": 75,
}

dnd_to_style = {
	"pos_hint_x": .4,
	"layout_size_x": .5,
	"layout_size_y": .8,
	"spacing": 50
}
