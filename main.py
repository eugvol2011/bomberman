import os
os.environ['KIVY_IMAGE'] = 'pil'
from kivy.app import App
from kivy.core.window import Window
from menu import Menu


class BombermanApp(App):
    pass


#Window.maximize()
if __name__ == '__main__':
    BombermanApp().run()
