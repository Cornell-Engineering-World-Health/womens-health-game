class Action:
    def __init__(self, character, action):
        self.has_been_executed = False
        self.character = character
        self.action_type = action

    def execute(self):
        print(self.action_type)
