from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window


from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

WINDOW_WIDTH = 564
WINDOW_HEIGHT =317
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
        self.ids.start_button.color = (1, 1, 1, 1)
    
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

    def __init__(self, **kwargs):
        super(ScreenThree, self).__init__(**kwargs)
        self.ryu_speed = 5  
        self.ryu1_speed = 5
        self.ryu_initial_x = Window.width 
        self.ryu1_initial_x = -200

    def on_enter(self):
        self.ids.monster_image.opacity = 0
        self.ids.monster_image_left.opacity = 0

        self.ids.monster_image.pos = (Window.width, 120)
        self.ids.monster_image_left.pos = (-200, 120)

        # Clock.schedule_interval(self.animate_monsters, 0.02)
        Clock.schedule_once(self.start_monster_right, 2)
        Clock.schedule_once(self.start_monster_left, 4)

    def on_leave(self):
        Clock.unschedule(self.start_monster_right)
        Clock.unschedule(self.start_monster_left)
        Clock.unschedule(self.animate_monster_right)
        Clock.unschedule(self.animate_monster_left)

    def start_monster_right(self, *args):
        # เริ่ม ฝั่งขวา
        self.ids.monster_image.opacity = 1
        Clock.schedule_interval(self.animate_monster_right, 0.02)

    def start_monster_left(self, *args):
        # เริ่ม ฝั่งซ้าย
        self.ids.monster_image_left.opacity = 1
        Clock.schedule_interval(self.animate_monster_left, 0.02)

    
    def animate_monster_right(self, dt):
        # monster ฝั่งขวา (เลื่อนซ้าย)
        if self.ids.monster_image.x + self.ids.monster_image.width > 0:
            self.ids.monster_image.pos = (
                self.ids.monster_image.x - self.ryu_speed,
                self.ids.monster_image.y
            )

    def animate_monster_left(self, dt):
        # monster ฝั่งซ้าย (เลื่อนขวา)
        if self.ids.monster_image_left.x < Window.width:
            self.ids.monster_image_left.pos = (
                self.ids.monster_image_left.x + self.ryu1_speed,
                self.ids.monster_image_left.y
            )


    def go_back(self):
        self.manager.current = 'screen_one'


class PageoneApp(App) :
    def build(self):
        return Builder.load_file('pageone.kv')

if __name__ =='__main__':
    PageoneApp().run()

