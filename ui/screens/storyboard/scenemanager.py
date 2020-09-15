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

# import widgets
from kivy.uix.screenmanager import *
from ui.widgets.scene.character import Character

# import layouts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

# import buttons
from kivy.uix.button import *
from ui.widgets.welcome_button import WelcomeButton

# import behaviors
from kivy.uix.behaviors import *


class SceneManagerScreen(Screen):
    def __init__(self, **kwargs):
        super(SceneManagerScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()
        self.screen_setup()
        # Game state
        self.state = 0

        # Scene variables
        self.scene_actions = []
        self.characters = []

    def ui_layout(self):
        self.clear_widgets()

        # Screen variables
        self.scene_num = 0
        self.character = 9

        # Layout declarations
        boxlayout = BoxLayout(orientation="vertical", pos=(0, self.y+500))
        anchor_left = AnchorLayout(anchor_x='left', anchor_y='center')
        anchor_right = AnchorLayout(anchor_x='right', anchor_y='center')

        def callback(instance):
            # How to view list of all properties of instance?
            if (instance.text == '>>'):
                self.scene_num += 1
            if (instance.text == '<<'):
                if (self.scene_num != 0):
                    self.scene_num -= 1
            scene_label.text = 'Scene ' + str(self.scene_num)
            self.load_scene(self.scene_num)

        # Widget declarations
        scene_label = MDLabel(text='Scene ' + str(self.scene_num),
                              font_style='H4', halign='center')

        # What properties can we declare in the button constructor
        nextButton = Button(text='>>', font_size=50, size_hint=(0.1, 0.3))
        nextButton.bind(on_press=callback)

        prevButton = Button(text='<<', font_size=50, size_hint=(0.1, 0.3))
        prevButton.bind(on_press=callback)

        # Adding widgets to layouts
        boxlayout.add_widget(scene_label)
        # anchor_left.add_widget(scene_label)
        anchor_left.add_widget(prevButton)
        anchor_right.add_widget(nextButton)

        # Adding layouts to screen
        self.add_widget(boxlayout)
        self.add_widget(anchor_left)
        self.add_widget(anchor_right)

        self.do_layout()

    def screen_setup(self):
        sm = ScreenManager()

    def load_scene(self, scene_num):
        print('Loading scene ' + str(scene_num))

    def change_screen(self, screen):
        self.manager.current = screen
