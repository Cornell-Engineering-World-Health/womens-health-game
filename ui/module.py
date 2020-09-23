from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen


class Module(Screen):
    # instances

    # **kwargs for json
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

        self.user = None
        self.module_number = 0
        self.scenes = []
        self.present_characters = []
        self.current_line = 0
        self.current_scene = 0

    # built in kivy function that runs before scene is loaded
    def on_pre_enter(self, *args):

        # loads the current user data into user if they exist

        if len(self.manager.screens[2].ids) > 0:
            self.user = self.manager.screens[2].ids.user
            self.module_number = self.manager.screens[2].ids.module_number
            self.app.title = "Health Friend [Game]  ::  " + self.user['first_name'] + " " + self.user['last_name']
        else:
            self.app.title = "Health Friend [Game]  ::  EWH"
        self._load(self.module_number)
    

    def _load(self, module_number):
        print('loading', module_number)

    # changed from replay
    def play_current_line(self):
        pass

    # can use play_current_line within this fn
    def advance_to_next_line(self):
        pass

    def render_scene(self):
        # kivy
        print("rendering...")

    def load_assessment(self):
        if self.user:
            self.manager.screens[3].ids = {'user': self.user, 'module_number': self.module_number, 'assessment': None}
        else:
            self.manager.screens[3].ids = {'module_number': self.module_number, 'assessment': None}

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
        for script_action in script:
            scene_str += str(script_action)
        return scene_str
