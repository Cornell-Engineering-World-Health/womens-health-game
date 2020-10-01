class Action:
    def __init__(self, character_id, action_type):
        self.has_been_executed = False
        self.character_id = character_id
        self.action_type = action_type

    def execute(self):
        print(self.action_type)

    def __str__(self):
        if self.has_been_executed:
            return ('[Action] Character ' + str(self.character_id) + ': ' + self.action_type
                + ' (Executed)')
        return ('[Action] Character ' + str(self.character_id) + ': ' + self.action_type
                + ' (Not executed)')
