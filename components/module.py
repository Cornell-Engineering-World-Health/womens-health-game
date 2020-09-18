class Module:
    # instances

    # **kwargs for json
    def __init__(self, module_number, **kwargs):
        self.module_number = module_number
        self.scenes = []
        self.present_characters = []
        self.current_line = 0
        self.current_scene = 0

    # changed from replay
    def play_current_line(self):
        pass

    # can use play_current_line within this fn
    def advance_to_next_line(self):
        pass

    def render_scene(self):
        # kivy
        print("rendering...")
