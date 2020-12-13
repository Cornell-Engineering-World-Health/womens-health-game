from components.action import Action
from components.line import Line
from components.character import Character
from components.picture import Picture

import json
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from util.store import update_module_state, complete_module_state, current_module_state


class Module(Screen):
    # instances

    # **kwargs for json
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

        self.user = None
        # Current module
        self.module_number = 0
        # Audio path (define swhich language - English or Hindi)
        self.audio_path = 'assets/audio/english/'
        # Boolean checking if a sound is playing
        self.is_sound = False
        # List of scenes in the current module
        self.scenes = []
        # All the character objects in the scene
        self.scene_characters = []
        # Array of available positions on the screen (3 total)
        self.screen_positions = []
        # Number of characters currently on the screen
        self.screen_characters = 0
        # Current scene object
        self.current_scene = None
        # The current line in the script that is going to be played
        self.script_iterator = -1
        # List of lines (not actions) that have been executed
        self.lines = []
        # The index of the line that was executed; default is -1
        self.line_iterator = -1
        # character id mapped to mouth widget
        self.id_to_mouth = {}
        # image name mapped to image widgets
        self.images = {}

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

        # Init and loading functions for module
        self.load_local_storage()
        self.init_module_ui()
        self.load_module(self.module_number)
        self.load_characters()
        self.load_background()
        self.init_game_buttons()

    # TODO: load in current state and override other values
    def load_local_storage(self):
        state = current_module_state(self.user['id'], self.module_number)
        print("STATE", state)
        pass

    # Screen positioning: assuming maximum of 3 characters on screen at one time
    def init_module_ui(self):
        # 3 character positions on screen at once
        self.screen_positions.append({'x': -0.3, 'top': 0.45})
        self.screen_positions.append({'x': 0, 'top': 0.6})
        self.screen_positions.append({'x': 0.3, 'top': 0.45})

    def init_game_buttons(self):
        next_icon = MDIconButton(
            icon='assets/game/next-arrow.png',
            pos_hint={'x': 0.92, 'center-y': 0.5},
            size_hint=(0.08, 0.1),
            user_font_size='64sp',
            on_press=self.advance_line
        )
        prev_icon = MDIconButton(
            icon='assets/game/prev-arrow.png',
            pos_hint={'x': 0, 'center-y': 0.5},
            size_hint=(0.08, 0.1),
            user_font_size='64sp',
            on_press=self.previous_line
        )
        module_icon = MDIconButton(
            icon='assets/game/modules.png',
            pos_hint={'x': 0, 'top': 1},
            size_hint=(0.08, 0.1),
            user_font_size='64sp',
            on_press=self.load_module_screen
        )
        self.ids.float.add_widget(next_icon)
        self.ids.float.add_widget(prev_icon)
        self.ids.float.add_widget(module_icon)

    def load_module(self, module_number):
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
                elif script_line['type'] == 'line':
                    character_id = script_line['character_id']
                    text = script_line['dialogue']
                    audio_file = script_line['dialogue_file']
                    script.append(Line(character_id, text, audio_file))
                elif script_line['type'] == 'picture':
                    name = script_line['name']
                    src = script_line.get('src')
                    action_type = script_line['action_type']
                    script.append(Picture(name, src, action_type))
            scene = Scene(character_ids, background_image, script)
            self.scenes.append(scene)
            self.current_scene = self.scenes[0]

    def load_characters(self):
        json_file_path = 'assets/json/characters.json'

        with open(json_file_path) as json_file:
            character_data_dict = json.load(json_file)

        for character_id in self.current_scene.character_ids:
            for character in character_data_dict:
                if (character['id'] == character_id):
                    char_id = character['id']
                    char_name = character['name']
                    char_image = character['image']
                    char_mouth_pos = (character['mouth_offset_top'],character['mouth_offset_x'],character['mouth_size'])
                    character_obj = Character(char_id, char_name, char_image, char_mouth_pos)
                    self.scene_characters.append(character_obj)

    def load_background(self):
        image_file_path = 'assets/backgrounds/' + self.current_scene.background_image
        background = Image(
            source=image_file_path,
            keep_ratio=False,
            allow_stretch=True,
            id=str(image_file_path)
        )
        self.ids.float.add_widget(background)

    # Plays the current line and advances the script_iterator
    # Callback parameter added for Kivy on_press callback
    def advance_line(self, callback):
        # Check if a sound is currently playing; advance if no sound playing
        if (not self.is_sound):
            self.script_iterator += 1
            if (self.script_iterator < len(self.current_scene.script)):
                # Check if a line has been executed already
                line = self.current_scene.script[self.script_iterator]
                if (type(line) == Line):
                    self.lines.append(line)
                    self.line_iterator += 1
                # print('Executing: ' + str(line))
                self.play_line(line)
                # update module state (user_id, module_id, scene, line)
                update_module_state(self.user['id'], self.module_number, 0, self.line_iterator)
            else:
                # Set script iterator to end of script
                self.script_iterator = len(self.current_scene.script) - 1
                # update module state to complete (user_id, module_id)
                complete_module_state(self.user['id'], self.module_number)
                # Advance to assessment
                self.load_assessment()

    # Rewinds the line that was just played and plays the prev line
    # Callback parameter added for Kivy on_press callback
    def previous_line(self, callback):
        # Check if a sound is currently playing; rewind if no sound playing
        if (not self.is_sound):
            if (self.script_iterator >= 0):
                # Undo line that was just played
                line = self.current_scene.script[self.script_iterator]
                # print('Rewinding: ' + str(line))
                # If an Action was just played:
                # Remove character if it just entered, or add character if it was just removed
                if (type(line) == Action):
                    line_character = None
                    for character in self.scene_characters:
                        if character.id == line.character_id:
                            line_character = character
                    if (line.action_type == 'enter'):
                        self._remove_character(line_character)
                    else:
                        self._render_character(line_character)
                # If current line was a Line:
                # Play previous line
                elif (type(line) == Line):
                    # Check if a line in the script has been executed yet
                    if (self.line_iterator > 0):
                        self.line_iterator -= 1
                        self.lines.pop()
                        # self.play_line(self.lines[self.line_iterator])
                    else:
                        # Update tracking variables
                        self.lines = []
                        self.line_iterator = -1
                # If current line is a Picture:
                # remove it if it was added; render if it was removed
                elif (type(line) == Picture):
                    if (line.action_type == 'enter'):
                        self._remove_picture(line.name)
                    elif (line.action_type == 'exit'):
                        self._render_picture(line.name, line.src)
                    elif (line.action_type == 'clear'):
                        for name, src in zip(line.name, line.src):
                            self._render_picture(name, src)
                self.script_iterator -= 1

    def play_line(self, line):
        if (type(line) == Line):
            # print('Playing: ' + str(line))
            self.play_audio(line.audio_file)
            # Animate mouth
            for character in self.scene_characters:
                if character.id == line.character_id:
                    self._animate_mouth(character)
        elif (type(line) == Action):
            line_character = None
            for character in self.scene_characters:
                if character.id == line.character_id:
                    line_character = character
            if (line.action_type == 'enter'):
                self._render_character(line_character)
            else:
                self._remove_character(line_character)
        elif (type(line) == Picture):
            if (line.action_type == 'enter'):
                self._render_picture(line.name, line.src)
            elif (line.action_type == 'exit'):
                self._remove_picture(line.name)
            elif (line.action_type == 'clear'):
                for name in line.name:
                    self._remove_picture(name)
            

    def play_audio(self, audio):
        audio_file = self.audio_path + audio
        # Disable next/prev buttons
        self.is_sound = True
        sound = SoundLoader.load(audio_file)
        sound.bind(on_stop=self.on_audio_finish)
        sound.play()

    # Callback function for when audio is finished playing
    def on_audio_finish(self, sound):
        # Enable next/prev buttons
        self.is_sound = False
        sound.unload()
        # Stop character animation
        self._stop_talking()

    def _render_character(self, character):
        # Load image from character as kivy object
        image_file_path = 'assets/characters/' + character.image
        # Position character based off current # of characters on screen
        pos = self._position_character()
        new_character = Image(
            source=image_file_path,
            pos_hint=pos,
            size_hint_y= None,
            height= 500,
            id=str(character.id)
        )
        self.ids.float.add_widget(new_character)
        self._render_mouth(character) # render mouth separately
        self.screen_characters += 1

    def _render_mouth(self, character):
        character_pos = dict(self._position_character())
        character_pos['top'] -= character.mouth_offset_top
        character_pos['x'] -= character.mouth_offset_x
        character.mouth_pos = character_pos # update character's mouth position
        current_mouth = Image(
            source=character.current_mouth,
            pos_hint=character.mouth_pos,
            size_hint_y= character.mouth_size,
            height= 500,
            id='mouth_'+str(character.id)
        )
        self.ids.float.add_widget(current_mouth)
        self.id_to_mouth[character.id] = current_mouth # add mouth to id-mouth map

    def _animate_mouth(self, character):
        character.talk()
        self.id_to_mouth[character.id].source = character.current_mouth # change source of the rendered mouth

    def _stop_talking(self):
        # stop whoever is talking
        for c in self.scene_characters:
            if c.is_talking:
                c.stop()
                self.id_to_mouth[c.id].source = c.current_mouth

    # Returns a Kivy position as a dictionary (x and top)
    def _position_character(self):
        return self.screen_positions[self.screen_characters]

    def _remove_character(self, character):
        for widget in self.ids.float.children:
            # Check if widget has associated ID (not a button)
            if widget.id:
                try:
                    # self.ids.float.remove_widget(widget) if (int(widget.id) == character.id)
                    if (int(widget.id) == character.id):
                        self.ids.float.remove_widget(widget)
                        self.screen_characters -= 1
                        self.ids.float.remove_widget(self.id_to_mouth[character.id])
                        del self.id_to_mouth[character.id] # delete id-mouth mapping
                except:
                    pass
    
    # Render picture with default position in the middle.
    def _render_picture(self, name, src):
        pos = {'x': 0, 'top': 0.5}
        image = Image(
            source=src,
            pos_hint=pos,
            size_hint_y= None,
            height= 500,
            id=name
        )
        self.ids.float.add_widget(image)
        self.images[name] = image
    
    # Remove picture
    def _remove_picture(self, name):
        self.ids.float.remove_widget(self.images[name])
        del self.images[name]

    # Go to module selection screen
    # Callback parameter added for Kivy on_press callback
    def load_module_screen(self, callback):
        self.manager.current = 'menu_screen'

    def load_assessment(self):
        if self.user:
            self.manager.screens[4].ids = {
                'user': self.user, 'module_number': self.module_number, 'assessment': None}
        else:
            self.manager.screens[4].ids = {
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
