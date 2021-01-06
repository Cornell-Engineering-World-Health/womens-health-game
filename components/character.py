class Character:
    def __init__(self, id, name, character_idle, character_talking):
        self.id = id
        self.name = name
        self.is_talking = False

        #set the right filepath to the character images directory
        prefix = 'assets/characters/'

        self.character_idle = prefix + character_idle
        self.character_talking = prefix + character_talking
        self.current_mouth = None
        self.character_widget = None

    def talk(self):
        self.is_talking = True
        self.current_mouth = self.character_talking
        self._try_update_widget()

    def stop(self):
        self.is_talking = False
        self.current_mouth = self.character_idle
        self._try_update_widget()

    def _try_update_widget(self):
        if self.character_widget is not None:
            self.character_widget.source = self.current_mouth

    def __str__(self):
        return (self.name + ' (' + str(self.id) + ')')
