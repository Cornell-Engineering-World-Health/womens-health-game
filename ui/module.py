from components.action import Action
from components.line import Line
from components.character import Character

import json
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel

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
        self.current_line = None
        self.current_scene = 0

    # built in kivy function that runs before scene is loaded
    def on_pre_enter(self, *args):

        # loads the current user data into user if they exist

        # EDIT (Shaf): changed condition from len(self.manager.screens[2].ids) > 0
        # to len(self.manager.screens[2].ids) > 1
        # Pre-existing id: MDLabel (dialogue label)
        if len(self.manager.screens[2].ids) > 1:
            self.user = self.manager.screens[2].ids.user
            self.module_number = self.manager.screens[2].ids.module_number
            self.app.title = "Health Friend [Game]  ::  " + \
                self.user['first_name'] + " " + self.user['last_name']
        else:
            self.app.title = "Health Friend [Game]  ::  EWH"
        # self.app.add_widget(
        #     MDLabel(text='Game')
        # )
        self._load_module(self.module_number)
        self.render_scene()

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
                    character = script_line['character_id']
                    action_type = script_line['action_type']
                    script.append(Action(character, action_type))
                else:
                    character = script_line['character_id']
                    text = script_line['dialogue']
                    audio_file = script_line['dialogue_file']
                    script.append(Line(character, text, audio_file))
            scene = Scene(character_ids, background_image, script)
            self.scenes.append(scene)
            self.current_scene = self.scenes[0]

    # changed from replay
    def play_current_line(self, line):
        if (type(line) == Line):
            # Show dialogue text as kivy label
            self.current_line = line.text
        else:
            if (line.action_type == 'enter'):
                self._render_character(line.character)
            else:
                self._remove_character(line.character)

    def _load_character(self, character_id):
        json_file_path = 'assets/json/characters.json'

        with open(json_file_path) as json_file:
            character_data_dict = json.load(json_file)
        
        for character in character_data_dict:
            if character['id'] == character_id:
                char_id = character['id']
                char_name = character['name']
                char_image = character['image']
                character_obj = Character(char_id, char_name, char_image)
                self.scene_characters.append(character_obj)
                return character_obj
        return None

    def _render_character(self, character):
        # Load image from character as kivy object
        character_obj = self._load_character(character)

        # character_image = character['image']
        image_file_path = 'assets/characters' + character_obj.name + '.json'
        pass

    def _remove_character(self, character):
        pass

    # can use play_current_line within this fn
    def advance_to_next_line(self, line):
        pass

    def render_scene(self):
        # kivy
        scene = self.current_scene
        script = scene.script
        # Add helper method here that loads in all character objects needed
        # for this scene
        for script_line in script:
            self.play_current_line(script_line)
        self.scene_characters = []

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