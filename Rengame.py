from kivy.app import App

# from kivy.uix.button import Button
# from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

resource_add_path('D:\\New folder (2)\debug-font')
LabelBase.register(DEFAULT_FONT, 'DebugF.otf')

class ScreenOne(Screen):
    def change_screen(self):
        self.manager.current = 'screen_two'

class ScreenTwo(Screen):
    pass


class PageoneApp(App) :
    def build(self):
        return Builder.load_file('pageone.kv')

if __name__ =='__main__':
    PageoneApp().run()

