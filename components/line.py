class Line:
    def __init__(self, character_id, text, audio_file):
        self.character_id = character_id
        self.text = text
        self.audio_file = audio_file

    def execute(self):
        print("%s: %s", self.character_id, self.text)
        # play audio

    def __str__(self):
        return ('[Line] Character: ' + str(self.character_id) + ': ' + self.text)
