from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from  components.card import Card

class Dashboard(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        if(self.manager.screens):
            self.users = self.manager.screens[1].ids.users
            self.admin = self.manager.screens[1].ids.admin
            self.app.title = self.admin['email']
            self.render_cards()

    def render_cards(self):
        grid = self.manager.screens[2].ids.grid_card
        for user in self.users:
            card = Card(screen_manager=self.manager,id=user['_id'], first_name=user['first_name'], last_name=user['last_name'], village_name=user['village_name'])
            grid.add_widget(card)

    def on_leave(self):
        grid = self.manager.screens[2].ids.grid_card
        grid.clear_widgets()
