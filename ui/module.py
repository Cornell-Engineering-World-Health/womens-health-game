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

language = "english"

class Module(Screen):
    # instances

    # **kwargs for json
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

        self.user = None
        
        # Current module
        self.module_number = 0

        # Audio path (define switch language - English or Hindi)
        self.audio_path = 'assets/audio/' + language + '/'

        # List of scenes in the current module
        self.scenes = []

        # All the character objects
        self.characters = []

        #character widgets currently on the screen
        self.character_widgets = []

        # Array of available positions on the screen
        self.screen_positions = []

        # Number of characters currently on the screen
        self.screen_characters = 0

        # Current scene object
        self.current_scene = None

        """
        The current background widget that's visible, used to know what to remove
        between scenes
        """
        self.current_background_wiget = None

        """
        The current line in the script that is going to be played,
        we start at -1 because we automatically increment the line # at the start
        of the function.
        """
        self.script_iterator = -1

        # Index of current scene
        self.scene_iterator = 0

        # character id mapped to mouth widget
        self.id_to_mouth = {}
        # image name mapped to image widgets
        self.images = {}

        self.next_icon = None
        self.prev_icon = None
        self.replay_icon = None
        self.module_icon = None

        #first line that is spoken
        self.first_line = None

    # built in kivy function that runs before scene is loaded
    def on_pre_enter(self, *args):
        
        # loads the current user data into user if they exist
        # Pre-existing id: float (FloatLayout id)l
        if len(self.ids) > 1:
            self.user = self.ids.user
            self.module_number = self.ids.module_number
            self.app.title = "Health Friend: " + \
                self.user['first_name'] + " " + self.user['last_name']
        else:
            print("failed to retrieve user")
            self.app.title = "Health Friend [Game]  ::  EWH"

        # Init and loading functions for module
        self.load_local_storage()
        self.init_module_ui()
        self.load_module(self.module_number)
        self.load_characters()
        self.init_game_buttons()

         #set up initial scene information
        self.current_scene = self.scenes[self.scene_iterator]
        self.set_current_background()
        
        #repeat the line that we stopped at
        target_script_iterator = self.script_iterator - 1
        self.script_iterator = -1
        for i in range(-1, target_script_iterator):
            #auto advance prevents the audio from playing, so we can script right through it
            self.advance_line(None, auto_advance= True)
    
        print("current scene: " + str(self.scene_iterator))

        self.advance_line(None)

    def load_local_storage(self):
        try:
            state = current_module_state(self.user['id'], self.module_number)

            if(state is not None):
                print("STATE", state)
                self.module_number = state['module_id']

                if(state['scene_id'] < len(self.scenes)):
                    self.scene_iterator = state['scene_id']
                    
                self.script_iterator = state['line_id']
        except:
            print("failed to load state")
            
    # Screen positioning: assuming maximum of 7 characters on screen at one time
    def init_module_ui(self): 
        self.screen_positions = [
            {'x': 0, 'top': 0.7},
            {'x': -0.2, 'top': 0.6},
            {'x': 0.2, 'top': 0.6},
            {'x': -0.4, 'top': 0.4},
            {'x': 0.4, 'top': 0.4},
            {'x': 0, 'top': 0.4},
        ]

    def init_game_buttons(self):
        if(not self.module_icon is None):
            return #we already loaded the module, don't add new buttons

        self.next_icon = MDIconButton(
            icon='assets/game/next-arrow.png',
            pos_hint={'x': 0.92},
            size_hint=(0.08, 0.1),
            user_font_size='64sp',
            on_press=self.advance_line
        )

        #only add this icon when you can go back
        self.prev_icon = MDIconButton(
            icon='assets/game/prev-arrow.png',
            pos_hint={'x': 0},
            size_hint=(0.08, 0.1),
            user_font_size='64sp',
            on_press=self.previous_line
        )

        self.replay_icon = MDIconButton(
            icon='assets/game/redo.png',
            pos_hint={'center_x': 0.5, 'center-y': 0.5},
            size_hint=(0.08, 0.1),
            user_font_size='64sp',
            on_press=self.replay_line
        )

        self.module_icon = MDIconButton(
            icon='assets/game/modules.png',
            pos_hint={'x': 0, 'top': 1},
            size_hint=(0.08, 0.1),
            user_font_size='64sp',
            on_press=self.load_module_screen
        )
        
        self.ids.float.add_widget(self.next_icon, 1)
        self.ids.float.add_widget(self.replay_icon, 1)
        self.ids.float.add_widget(self.module_icon, 1)
        self.ids.float.add_widget(self.prev_icon, 1)
        self.prev_icon_present = True

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

                    if self.first_line is None:
                        self.first_line = len(script) - 1
                elif script_line['type'] == 'picture':
                    name = script_line['name']
                    src = script_line.get('src')
                    action_type = script_line['action_type']
                    script.append(Picture(name, src, action_type))
            scene = Scene(character_ids, background_image, script)
            self.scenes.append(scene)
            

    def load_characters(self):

        #if you revisit this scene, make sure you don't load the characters twice
        if(len(self.characters) > 0): 
            return

        json_file_path = 'assets/json/characters.json'

        with open(json_file_path) as json_file:
            character_data_dict = json.load(json_file)

        # for character_id in self.current_scene.character_ids:
        for character in character_data_dict:
            # if (character['id'] == character_id):
            char_id = character['id']
            char_name = character['name']
            char_image = character['image']
            char_mouth_pos = (character['mouth_offset_top'],character['mouth_offset_x'],character['mouth_size'])
            character_obj = Character(char_id, char_name, char_image, char_mouth_pos)
            self.characters.append(character_obj)

    def set_current_background(self):

        #if there is a background already present, remove it
        if(not self.current_background_wiget is None):
            self.ids.float.remove_widget(self.current_background_wiget)

        image_file_path = 'assets/backgrounds/' + self.current_scene.background_image
        background = Image(
            source=image_file_path,
            keep_ratio=False,
            allow_stretch=True,
            id=str(image_file_path)
        )

        #adding 20 allows the background to be behind all other components
        self.ids.float.add_widget(background, 20) 
        self.current_background_wiget = background

    # Plays the current line and advances the script_iterator
    # Callback parameter added for Kivy on_press callback
    def advance_line(self, callback, auto_advance=False):
        print("current scene: " + str(self.scene_iterator))
        print("currnet line: " + str(self.script_iterator))
        if(self.script_iterator == 1 and self.scene_iterator == 0):
            #you are for the first time advancing the line, so add the prev widget
            self.ids.float.add_widget(self.prev_icon, 1)
            self.prev_icon_present = True
        elif(self.script_iterator == 0 and self.scene_iterator == 0 and not self.prev_icon is None):
            self.ids.float.remove_widget(self.prev_icon)
            self.prev_icon_present = False
        elif(not self.prev_icon_present):
            self.ids.float.add_widget(self.prev_icon, 1)
            self.prev_icon_present = True            

        self.script_iterator += 1

        if (self.script_iterator < len(self.current_scene.script)):
            update_module_state(self.user['id'], self.module_number, self.scene_iterator, self.script_iterator)
            # Check if a line has been executed already
            event = self.current_scene.script[self.script_iterator]

            if (type(event) == Line):
                if not auto_advance:
                    self.play_line(event)

                # update module state (user_id, module_id, scene, line)
            elif (type(event) == Action):
                self.execute_action(event)

                if not auto_advance:
                    self.advance_line(callback)
            elif (type(event) == Picture):
                self.play_picture_line(event)

                if not auto_advance:
                    self.advance_line(callback)
            else:
                print("ERROR: unhandled type " + str(event))
        elif (self.scene_iterator + 1 < len(self.scenes)):
            #advance the scene, reset the script
            self.scene_iterator += 1
            self.script_iterator = -1

            self.current_scene = self.scenes[self.scene_iterator]
            self.set_current_background()
            self.advance_line(callback)
        else:
            # Set script iterator to end of script
            self.script_iterator = len(self.current_scene.script) - 1
            # update module state to complete (user_id, module_id)
            complete_module_state(self.user['id'], self.module_number)
            # Advance to assessment
            self.load_assessment()

        #do this step to keep the buttons above everything else
        self.ids.float.remove_widget(self.replay_icon)
        self.ids.float.add_widget(self.replay_icon)
                
    # Rewinds the line that was just played and plays the prev line
    # Callback parameter added for Kivy on_press callback
    def previous_line(self, callback):

        # stop any sounds that are currently playing
        if not self.sound is None:
            self.sound.stop()

        if self.script_iterator > 0:
            self.script_iterator -= 1
        elif self.scene_iterator > 0:
            self.scene_iterator -= 1
            self.current_scene = self.scenes[self.scene_iterator]
            self.set_current_background()

            #set the line to the last line in the previous scene
            self.script_iterator = len(self.current_scene.script) - 1

        line = self.current_scene.script[self.script_iterator]

        # Remove character if it just entered, or add character if it was just removed
        if (type(line) == Action):
            line_character = None
            for character in self.characters:
                if character.id == line.character_id:
                    line_character = character
                    break
            if (line.action_type == 'enter'):
                self._remove_character(line_character)
            else:
                self._render_character(line_character)
            
            #continue rewinding until someone says something
            self.previous_line(callback)

        # Play previous line
        elif (type(line) == Line):
            self.play_line(line)
            update_module_state(self.user['id'], self.module_number, self.scene_iterator, self.script_iterator)

        # Remove it if it was added; render if it was removed
        elif (type(line) == Picture):
            if (line.action_type == 'enter'):
                self._remove_picture(line.name)
            elif (line.action_type == 'exit'):
                self._render_picture(line.name, line.src)
            elif (line.action_type == 'clear'):
                for name, src in zip(line.name, line.src):
                    self._render_picture(name, src)

            #continue rewinding until someone says something
            self.previous_line(callback)
        else:
            print("invalid type when trying to rewind: " + type(line))  

        if(self.script_iterator == self.first_line and self.scene_iterator == 0):
            #you are at the beginning, so remove prev icon
            self.ids.float.remove_widget(self.prev_icon)   
            self.prev_icon_present = False     

    def replay_line(self, callback):
        if not self.sound is None:
            self.sound.stop()
        
        line = self.current_scene.script[self.script_iterator]
        self.play_line(line)

    def execute_action(self, action):
        action_character = None
        for character in self.characters:
            if character.id == action.character_id:
                action_character = character
                break
        if (action.action_type == 'enter'):
            self._render_character(action_character)
        elif (action.action_type == 'exit'):
            self._remove_character(action_character)
        else:
            print("error: invalid action type")

    def play_line(self, line):
        self.play_audio(line.audio_file)
        # Animate mouth
        for character in self.characters:
            if character.id == line.character_id:
                self._animate_mouth(character)
                break

    def play_picture_line(self, picture):
        if (picture.action_type == 'enter'):
            self._render_picture(picture.name, picture.src)
        elif (picture.action_type == 'exit'):
            self._remove_picture(picture.name)
        elif (picture.action_type == 'clear'):
            for name in picture.name:
                self._remove_picture(name)
            

    def play_audio(self, audio):
        self.ids.float.remove_widget(self.next_icon)

        audio_file = self.audio_path + audio
        # Disable next/prev buttons
        try:
            self.sound = SoundLoader.load(audio_file)
            self.sound.bind(on_stop=self.on_audio_finish)
            self.sound.play()
        except:
            print("failed to play sound")
    
    # Callback function for when audio is finished playing
    def on_audio_finish(self, sound):
        # Enable next/prev buttons   
        self.sound.unload()
        self.sound = None
        # Stop character animation
        self._stop_talking()
        self.ids.float.add_widget(self.next_icon, 1)

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

        self.character_widgets.append(new_character)
        self.ids.float.add_widget(new_character, 3)
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
        self.ids.float.add_widget(current_mouth, 3)
        self.id_to_mouth[character.id] = current_mouth # add mouth to id-mouth map

    def _animate_mouth(self, character):
        character.talk()
        self.id_to_mouth[character.id].source = character.current_mouth # change source of the rendered mouth

    def _stop_talking(self):
        # stop whoever is talking
        for c in self.characters:
            if c.is_talking:
                c.stop()
                self.id_to_mouth[c.id].source = c.current_mouth

    # Returns a Kivy position as a dictionary (x and top)
    def _position_character(self):
        if self.screen_characters == len(self.screen_positions):
            self.screen_characters = 0
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
                        self.character_widgets.remove(widget)
                except:
                    pass
    
    # Render picture with default position in the middle.
    def _render_picture(self, name, src):
        pos = {'x': 0, 'top': 0.35}
        image = Image(
            source=src,
            pos_hint=pos,
            size_hint_y= None,
            height= 500,
            id=name
        )
        self.ids.float.add_widget(image, 3)
        self.images[name] = image
    
    # Remove picture
    def _remove_picture(self, name):
        self.ids.float.remove_widget(self.images[name])
        del self.images[name]

    def unload_screen(self):
        #stop any audio
        if(self.sound is not None):
            self.sound.stop()

        for character in self.character_widgets:
            self.ids.float.remove_widget(character)

        #remove all character mouths from the screen
        for character in self.id_to_mouth:
            self.ids.float.remove_widget(self.id_to_mouth[character])

        self.screen_characters = 0
        self.character_widgets = []
        self.id_to_mouth = {}

    # Go to module selection screen
    # Callback parameter added for Kivy on_press callback
    def load_module_screen(self, callback):
        self.unload_screen()
        
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