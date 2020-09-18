class Action:
    def __init__(self, character, action_type):
        self.has_been_executed = False
        self.character = character
        self.action_type = action_type

    def execute(self):
        print(self.action_type)
