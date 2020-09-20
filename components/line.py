class Line:
    def __init__(self, character, text, audio):
        self.text = text
        self.character = character
        self.audio = audio

    def execute(self):
        print("%s: %s", self.character, self.text)
        # play audio

    def __str__(self):
        return (str(self.character) + ': ' + self.text)
