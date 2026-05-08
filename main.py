from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window

class MainApp(MDApp):
    def build(self):
        # Set the theme colors for a modern look
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Light"

        # Create the main layout
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=50,
            adaptive_size=False
        )

        # Add a title label
        self.label = MDLabel(
            text="Samsung A34 Python App",
            halign="center",
            font_style="H4"
        )

        # Add an interactive button
        button = MDRaisedButton(
            text="CLICK ME",
            pos_hint={"center_x": .5},
            on_release=self.on_button_click
        )

        layout.add_widget(self.label)
        layout.add_widget(button)

        screen = MDScreen()
        screen.add_widget(layout)
        return screen

    def on_button_click(self, instance):
        self.label.text = "Buildozer Success!"
        self.label.theme_text_color = "Custom"
        self.label.text_color = (0, 0.7, 0, 1) # Green color

if __name__ == "__main__":
    MainApp().run()

