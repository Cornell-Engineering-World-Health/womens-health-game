import json
import os.path


class Module:
    # instances

    # **kwargs for json
    def __init__(self, module_number):
        print('Init module')
        self.module_number = module_number
        self.scenes = []
        self.present_characters = []
        self.current_line = 0
        self.current_scene = 0

        self._load(self.module_number)

    def _load(self, module_number):
        self._parse_json(module_number)
        print('loading')

    def _parse_json(self, module_number):
        json_file_path = 'module' + str(module_number) + '.json'
        # module_file_path = os.path.join('/json/', json_file)
        with open('./json/' + json_file_path) as json_file:
            json_data = json.load(json_file)
            print(json_data)

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

    def __main__(self):
        self.__init__(self, 0)


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
