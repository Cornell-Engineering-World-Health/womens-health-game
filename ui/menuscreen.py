from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from  components.modulecard import ModuleCard

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        if(self.manager.screens):
            self.admin = self.manager.screens[1].ids.admin
            self.user = self.ids.user
            self.app.title = self.user['first_name']+' '+self.user['last_name']
            self.modules = [{'id': '1', 'name':'Changes in the Body'},{'id': '2', 'name': 'Text'}] # get a list of modules
            self.render_cards()

    def render_cards(self):
        grid = self.manager.screens[6].ids.grid_module_card
        for module in self.modules:
            card = ModuleCard(screen_manager=self.manager, user= self.user, module=module)
            grid.add_widget(card)