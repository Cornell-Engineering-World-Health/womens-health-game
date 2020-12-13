class Picture:
    def __init__(self, name, src, action_type):
        self.name = name
        self.src = src
        self.action_type = action_type
        # action_type == 'enter': name (str), src (str)
        # action_type == 'exit': name (str), src (str)
        # action_type == 'clear': name (List(str)), src (List(str))

    def __str__(self):
        return ('[Image] ' + str(self.src))

    def set_pos(self):
        # set position
        pass
