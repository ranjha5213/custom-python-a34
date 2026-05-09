from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from android.permissions import request_permissions, Permission
from android import api_version, android_version

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=50)
        
        self.label = MDLabel(
            text=f"A34 Master Tool\nAndroid {android_version} (API {api_version})",
            halign="center",
            font_style="H4"
        )
        
        button = MDRaisedButton(
            text="START SESSION",
            pos_hint={"center_x": .5},
            on_release=self.request_permissions
        )
        
        layout.add_widget(self.label)
        layout.add_widget(button)
        
        screen = MDScreen()
        screen.add_widget(layout)
        return screen
    
    def request_permissions(self, instance):
        permissions = [
            Permission.CAMERA,
            Permission.RECORD_AUDIO,
            Permission.ACCESS_FINE_LOCATION,
            Permission.BODY_SENSORS,
        ]
        
        # Android 13+ (API 33+) needs media permissions
        if api_version >= 33:
            permissions.extend([
                Permission.READ_MEDIA_IMAGES,
                Permission.READ_MEDIA_VIDEO,
                Permission.READ_MEDIA_AUDIO
            ])
        else:
            permissions.extend([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
        
        request_permissions(permissions)
        self.label.text = "✓ Permissions Granted\nSession Ready"

if __name__ == "__main__":
    MainApp().run()
