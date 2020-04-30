# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.widget import Widget

# kivymd imports
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

from ui.widgets.welcome_button import WelcomeButton


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        if self.util.username != '':
            self.status = 'signed_in'
        else:
            self.status = ''
        self.ui_layout()

    def ui_layout(self):
        self.clear_widgets()

        sign_in_label = MDLabel(text='Sign in or Create an Account',
                                font_style='H4', halign='center')

        self.add_widget(sign_in_label)


        self.do_layout()

    def change_screen(self, screen):
        self.manager.current = screen
