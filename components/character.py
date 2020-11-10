class Character:
    def __init__(self, id, name, image, mouth_pos):
        self.id = id
        self.name = name
        self.is_talking = False
        self.image = image
        self.idle_mouth = 'assets/character-mouths/idle_neutral.png'
        self.talking_mouth = 'assets/character-mouths/anim_neutral.gif'
        self.current_mouth = 'assets/character-mouths/idle_neutral.png'
        self.mouth_offset_top, self.mouth_offset_x, self.mouth_size = mouth_pos

    def talk(self):
        self.is_talking = True
        self.current_mouth = self.talking_mouth

    def stop(self):
        self.is_talking = False
        self.current_mouth = self.idle_mouth

    def __str__(self):
        return (self.name + ' (' + str(self.id) + ')')
