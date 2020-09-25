class Line:
    def __init__(self, character, text, audio_file):
        self.character = character
        self.text = text
        self.audio_file = audio_file

    def execute(self):
        print("%s: %s", self.character, self.text)
        # play audio

    def __str__(self):
        return ('[Line] Character: ' + str(self.character) + ': ' + self.text)
