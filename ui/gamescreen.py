from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

class GameScreen(Screen):
	def __init__(self, **kw):
		super().__init__(**kw)
		self.app = MDApp.get_running_app()

	def on_pre_enter(self, *args):
		print(self.manager.screens[2], '\n', self.manager.screens[2].ids)
		self.user = self.manager.screens[2].ids.user
		self.app.title = "Health Friend: " + self.user['first_name'] + " " + self.user['last_name']

