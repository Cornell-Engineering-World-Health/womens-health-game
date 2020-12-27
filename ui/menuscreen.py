from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from  components.modulecard import ModuleCard
import json

from util.store import init_user

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        self.admin = self.manager.screens[1].ids.admin
        self.user = self.ids.user
        self.app.title = self.user['first_name']+' '+self.user['last_name']
        with open("assets/json/module_list.json") as file:
            data = json.load(file)
        self.modules = data["modules"]

        # initialize user in local storage
        init_user(self.user)
        self.render_cards()

    def render_cards(self):
        grid = self.manager.screens[6].ids.grid_module_card
        grid.clear_widgets()
        for module in self.modules:
            card = ModuleCard(screen_manager=self.manager, user= self.user, module=module)
            grid.add_widget(card)

    # navigate back to dashboard
    def back(self):
        self.manager.current = 'dashboard'

    def on_leave(self):
        grid = self.manager.screens[6].ids.grid_module_card
        grid.clear_widgets()
