class Character:
    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.active_mouth = None
        self.is_talking = False
        self.image = image

    def talk(self):
        self.is_talking = True
        # talk

    def __str__(self):
        return (self.name + ' (' + str(self.id) + ')')
