class Module:
    # instances
    # module_number = 0

    # **kwargs for json
    def __init__(self, module_number, **kwargs):
        self.module_number = module_number
        module_number += 1
        self.scenes = []
        self.chars_on_screen = []
        self.current_line = 0
        self.current_scene = 0

    # changed from replay
    def play_current_line(self):
        print(current_line)
        # do advance to next line w/o incrementing

    def advance_to_next_line(self):
        # is scene an object or a list of lines?
        # self.current_scene
        play_current_line()
        current_line += 1

    def render_scene(self):
        # kivy
        print("rendering...")
