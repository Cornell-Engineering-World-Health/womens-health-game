class Line:
    def __init__(self, character, dialogue, audio):
        self.dialogue = dialogue
        self.character = character
        self.audio = audio

    def execute(self):
        print("%s: %s", self.character, self.dialogue)
        # play audio
