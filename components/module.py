class Module:
    # instances

    # **kwargs for json
    def __init__(self, module_number):
        self.module_number = module_number
        self.scenes = []
        self.present_characters = []
        self.current_line = 0
        self.current_scene = 0

        self._load(self.module_number)

    def _load(module_number):
        print('loading')

    # changed from replay
    def play_current_line(self):
        pass

    # can use play_current_line within this fn
    def advance_to_next_line(self):
        pass

    def render_scene(self):
        # kivy
        print("rendering...")

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
