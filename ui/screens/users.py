# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout


from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable


#backend imports
from util.firebase import firebase


class UserScreen(Screen):
    def __init__(self, **kwargs):
        super(UserScreen, self).__init__(name=kwargs.get('name'))     

    def ui_layout(self):
        
        layout = FloatLayout(size=(300, 300))
        layout.clear_widgets()

        # LOGOUT
        logout_button = Button(text='Log Out', font_size=30, size_hint=(.2, .05), pos_hint=({'x':.5, 'y':.7}))
        logout_button.bind(on_press=self.on_logout)

        layout.add_widget(logout_button)
        return layout

    def on_logout(self, instance):
        firebase.auth().signOut()
        self.manager.screens[0].ids.users = []
        self.change_screen('login')

    def render_table(self):
        #print("RENDER", self.users[0]['_id'])
        self.data_tables = MDDataTable(
            column_data=[
            ("ID", dp(45)), ("First Name", dp(30)), ("Last Name", dp(30)), ("Village", dp(30))
            ],
            row_data=[
                (f"{self.users[i]['_id']}",  f"{self.users[i]['first_name']}", f"{self.users[i]['last_name']}", f"{self.users[i]['village_name']}") for i in range(len(self.users))
            ],
            check=True
            )
        return self.data_tables

    def on_check_press(self, instance_table, current_row):
        print(instance_table, current_row)

    def on_pre_enter(self):
        self.users = self.manager.screens[0].ids.users
        table = self.render_table()
        self.add_widget(table)


    def change_screen(self, screen):
        self.manager.current = screen

