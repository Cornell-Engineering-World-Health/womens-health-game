class Character:
    def __init__(self, **kwargs):
        self.id = id
        self.name = name
        # ?????? what's the difference?
        self.active_mouth = False
        self.is_talking = False
        self.image = image

    def talk(self):
        is_talking = True
        # talk
