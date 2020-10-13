from components.action import Action
from components.line import Line
from components.character import Character

import json
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.image import Image

class Module(Screen):
    # instances

    # **kwargs for json
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

        self.user = None
        self.module_number = 0
        self.scenes = []
        self.scene_characters = []
        self.screen_positions = []
        self.screen_characters = 0
        self.current_scene = None
        self.script_iterator = -1
        self.current_line = MDLabel(
            pos_hint= {"x": .3, "top": 1},
            size_hint= (.4, .1),
            text= "",
            halign= "center",
            theme_text_color= "Primary",
            id= 'dialogue_text'
        )

    # built in kivy function that runs before scene is loaded
    def on_pre_enter(self, *args):

        # loads the current user data into user if they exist

        # Pre-existing id: float (FloatLayout id)
        if len(self.ids) > 1:
            self.user = self.ids.user
            self.module_number = self.ids.module_number
            self.app.title = "Health Friend [Game]  ::  " + \
                self.user['first_name'] + " " + self.user['last_name']
        else:
            self.app.title = "Health Friend [Game]  ::  EWH"

        # Adding dialogue label to float layout
        self.ids.float.add_widget(self.current_line)

        self._init_module_ui()
        self._load_module(self.module_number)
        self._load_characters()
        # self.render_scene()

    # Screen positioning: assuming maximum of 3 characters on screen at one time
    def _init_module_ui(self):
        # 3 character positions on screen at once
        self.screen_positions.append({'x': -0.3, 'top': 0.75})
        self.screen_positions.append({'x': 0, 'top': 0.9})
        self.screen_positions.append({'x': 0.3, 'top': 0.75})

        # Add next and previous buttons
        # Change icon directory to assets/button...
        # Ripple effect on click?
        # next_button = MDIconButton(
        #     icon="assets/character-mouths/idle_happy.png",
        #     pos_hint={'x': 0.9, 'top': 0.5},
        #     user_font_size='64sp'
        # )
        # prev_button = MDIconButton(
        #     icon="assets/character-mouths/idle_happy.png",
        #     pos_hint={'x': 0, 'top': 0.5},
        #     user_font_size='64sp'
        # )
        # self.ids.float.add_widget(next_button)
        # self.ids.float.add_widget(prev_button)

    def _load_module(self, module_number):
        self._load_module_json(module_number)

    def _load_module_json(self, module_number):
        module_path = 'module' + str(module_number) + '.json'
        json_file_path = 'assets/json/' + module_path

        with open(json_file_path) as json_file:
            module_data_dict = json.load(json_file)

        self._parse_module_json(module_data_dict)

    def _parse_module_json(self, module_data_dict):
        json_scenes = module_data_dict['scenes']
        for json_scene in json_scenes:
            character_ids = json_scene['characters']
            background_image = json_scene['background']
            json_script = json_scene['script']
            script = []
            for script_line in json_script:
                if script_line['type'] == 'action':
                    character_id = script_line['character_id']
                    action_type = script_line['action_type']
                    script.append(Action(character_id, action_type))
                else:
                    character_id = script_line['character_id']
                    text = script_line['dialogue']
                    audio_file = script_line['dialogue_file']
                    script.append(Line(character_id, text, audio_file))
            scene = Scene(character_ids, background_image, script)
            self.scenes.append(scene)
            self.current_scene = self.scenes[0]

    def advance_line(self):
        if (self.script_iterator < len(self.current_scene.script)):
            self.script_iterator += 1
            line = self.current_scene.script[self.script_iterator]
            print(line)
            self.play_current_line(line)
        
    # When rewinding a line, should we remove characters that were just added?
    # Need to handle adding the same character twice when rewinding
    def previous_line(self):
        if (self.script_iterator > 0):
            self.script_iterator -= 1
            line = self.current_scene.script[self.script_iterator]
            print(line)
            self.play_current_line(line)

    # def render_scene(self):
    #     scene = self.current_scene
    #     script = scene.script
    #     self._load_characters()
    #     print(script)

    #     for script_line in script:
    #         print(script_line)
    #         self.play_current_line(script_line)
    #     self.scene_characters = []

    def play_current_line(self, line):
        if (type(line) == Line):
            self.current_line.text = line.text
        else:
            line_character = None
            for character in self.scene_characters:
                if character.id == line.character_id:
                    line_character = character
            if (line.action_type == 'enter'):
                self.screen_characters += 1
                self._render_character(line_character)
            else:
                self.screen_characters -= 1
                self._remove_character(line_character)

    def _load_characters(self):
        json_file_path = 'assets/json/characters.json'

        with open(json_file_path) as json_file:
            character_data_dict = json.load(json_file)

        for character_id in self.current_scene.character_ids:
            for character in character_data_dict:
                if (character['id'] == character_id):
                    char_id = character['id']
                    char_name = character['name']
                    char_image = character['image']
                    character_obj = Character(char_id, char_name, char_image)
                    self.scene_characters.append(character_obj)

    def _render_character(self, character):
        # Load image from character as kivy object
        image_file_path = 'assets/characters/' + character.image
        # Position character based off # of characters on screen
        pos = self._position_character()
        new_character = Image(
            source=image_file_path,
            pos_hint=pos,
            size_hint_y= None,
            height= 500,
            id=str(character.id)
        )
        self.ids.float.add_widget(new_character)

    # Returns a Kivy position as a dictionary (x and top)
    def _position_character(self):
        return self.screen_positions[self.screen_characters - 1]

    def _remove_character(self, character):
        self.ids.float.remove_widget(character)

    def load_assessment(self):
        if self.user:
            self.manager.screens[3].ids = {
                'user': self.user, 'module_number': self.module_number, 'assessment': None}
        else:
            self.manager.screens[3].ids = {
                'module_number': self.module_number, 'assessment': None}

        self.manager.current = 'assessment_manager'

    def __str__(self):
        str_module = 'Module: ' + str(self.module_number) + '\n'
        str_scene = ''
        for i, scene in enumerate(self.scenes):
            str_scene += 'Scene: ' + str(i) + str(scene) + '\n'
        return (str_module + str_scene)


class Scene:
    def __init__(self, character_ids, background_image, script):
        self.character_ids = character_ids
        self.background_image = background_image
        self.script = script

    def __str__(self):
        scene_str = ''
        for script_action in self.script:
            scene_str += str(script_action)
        return scene_str
