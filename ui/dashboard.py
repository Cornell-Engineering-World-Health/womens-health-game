from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from  components.card import Card, CardButton

class Dashboard(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        if(self.manager.screens):
            self.users = self.manager.screens[0].ids.users
            self.admin = self.manager.screens[0].ids.admin
            self.app.title = self.admin['email']
            self.render_cards()

    def render_cards(self):
        grid = self.manager.screens[1].ids.grid_card
        for user in self.users:
            card = Card(screen_manager=self.manager,first_name=user['first_name'], last_name=user['last_name'], village_name=user['village_name'])
            grid.add_widget(card)


