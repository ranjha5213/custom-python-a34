# src/main.py
from kivy.app import App
from kivy.uix.button import Button

class A34CustomApp(App):
    def build(self):
        # A simple button to test the touch interface on your Samsung
        return Button(text='A34 Python GUI Active!', 
                      background_color=(0, 0.7, 1, 1))

if __name__ == '__main__':
    A34CustomApp().run()

