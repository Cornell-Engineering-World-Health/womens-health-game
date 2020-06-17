# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.button import Button

# kivymd imports
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


#backend imports
from util.client import api_call
from util.firebase import firebase
import json



class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(name=kwargs.get('name'))
    
        layout = self.ui_layout()
        self.add_widget(layout)

        self.login_email = ''
        self.login_password = ''

    def ui_layout(self):
        
        layout = FloatLayout(size=(300, 300))
        layout.clear_widgets()

        # EMAIL
        email_input = TextInput(multiline=False, hint_text='email', size_hint=(.4, .05), pos_hint=({'x':.3, 'y':.65}))
        email_input.bind(text=self.on_text_email)

        # PASSWORD
        password_input = TextInput(multiline=False, hint_text='password', password= True, size_hint=(.4, .05), pos_hint=({'x':.3, 'y':.55}))
        password_input.bind(text=self.on_text_password)

        # SIGNIN
        signin_button = Button(text='Log In', font_size=30, size_hint=(.4, .05), pos_hint=({'x':.3, 'y':.45}))
        signin_button.bind(on_press=self.on_signin)

        layout.add_widget(email_input)
        layout.add_widget(password_input)
        layout.add_widget(signin_button)

        return layout


    def change_screen(self, screen):
        self.manager.current = screen

    def on_text_email(self, instance, value):
        self.login_email = value

    def on_text_password(self, instance, value):
        self.login_password = value

    # callback method makes api_calls
    def on_signin(self, instance):
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(self.login_email, self.login_password)

        # TEMP HARD CODED ADMIN_ID FOR TESTING
        res = api_call('users/admin/vr6zdoGoZucQlnf01XavCd3eO3k2')
        self.manager.screens[0].ids.users = res
        self.change_screen('users')

        


 
