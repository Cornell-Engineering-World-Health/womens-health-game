# App Styling

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
	"name_y": 0.8,
	"village_name_y": 0.7,
	"title_font": "Subtitle1",
	"subtitle_font": "Subtitle2",
	"theme": "Primary"
}

dnd_from_style = {
	"size_hint": (.3,.1),
	"background_color": [0,0,0,0],
	"sources": ['assets/drag-and-drop/shape1.png', 'assets/drag-and-drop/shape2.png', 
				'assets/drag-and-drop/shape3.png'],
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
