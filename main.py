from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from android.permissions import request_permissions, Permission

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=50)
        self.label = MDLabel(text="A34 Master Tool Ready", halign="center", font_style="H4")
        button = MDRaisedButton(
            text="START SESSION", 
            pos_hint={"center_x": .5}, 
            on_release=self.ask_permissions
        )
        layout.add_widget(self.label)
        layout.add_widget(button)
        screen = MDScreen()
        screen.add_widget(layout)
        return screen

    def ask_permissions(self, instance):
        request_permissions([
            Permission.CAMERA, Permission.RECORD_AUDIO, 
            Permission.ACCESS_FINE_LOCATION, Permission.BODY_SENSORS,
            Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE
        ])
        self.label.text = "Permissions Requested"

if __name__ == "__main__":
    MainApp().run()
