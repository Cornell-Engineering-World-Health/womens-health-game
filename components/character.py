class Character:
    def __init__(self, **kwargs):
        self.id = id
        self.name = name
        # image
        self.active_mouth = None
        self.is_talking = False
        self.image = image

    def talk(self):
        self.is_talking = True
        # talk
