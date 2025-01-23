from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window


from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

WINDOW_WIDTH = 564
WINDOW_HEIGHT = 317
Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
Window.resizable = True 

resource_add_path('D:\\New folder (2)\debug-font')
LabelBase.register(DEFAULT_FONT, 'DebugF.otf')

def enforce_window_size(instance, width, height):
    if width != WINDOW_WIDTH or height != WINDOW_HEIGHT:
        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

Window.bind(on_resize=enforce_window_size)


class ScreenOne(Screen):
    def change_button_color(self):
        self.ids.start_button.background_color = (1, 1, 1, 1)
        self.ids.start_button.color = (20/255, 158/255, 126/255, 1)
    
    def change_label_color(self):
        self.ids.title_label.color = (20/255, 158/255, 126/255, 1)
    
    def change_screen(self):
        self.manager.current = 'screen_two'

class ScreenTwo(Screen):
    def on_enter(self):
        self.ids.game_start_label.text = "Game Start"
        Clock.schedule_once(self.goto_next_screen, 1)

    def goto_next_screen(self, *args):
        self.manager.current = 'screen_three'

    # def go_back(self):
    #   self.manager.current = 'screen_one'

class ScreenThree(Screen):
    def go_back(self):
        self.manager.current = 'screen_one'


class PageoneApp(App) :
    def build(self):
        return Builder.load_file('pageone.kv')

if __name__ =='__main__':
    PageoneApp().run()

