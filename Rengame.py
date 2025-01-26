from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

WINDOW_WIDTH = 564
WINDOW_HEIGHT =317
Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
# Window.resizable = True 

resource_add_path('D:\\New folder (2)\debug-font')
LabelBase.register(DEFAULT_FONT, 'DebugF.otf')


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



class ScreenThree(Screen):

    def __init__(self, **kwargs):
        super(ScreenThree, self).__init__(**kwargs)
        self.ryu_speed = 5  
        self.ryu1_speed = 5
        self.ryu_initial_x = Window.width 
        self.ryu1_initial_x = -200

        self.hero_facing_right = True
        self.monster_active = False  
        self.hero_shooting = False

       
        Window.bind(on_key_down=self.on_key_down)

    def on_enter(self):
        self.ids.monster_image.opacity = 0
        self.ids.monster_image_left.opacity = 0

        self.ids.monster_image.pos = (Window.width + 100, 120)
        self.ids.monster_image_left.pos = (-200, 120)

        # Clock.schedule_interval(self.animate_monsters, 0.02)
        Clock.schedule_once(self.start_monster_right, 2)
        Clock.schedule_once(self.start_monster_left, 4)
        
        self.monster_active = True

        Window.bind(on_key_down=self.on_key_down)


    def on_leave(self):
        Clock.unschedule(self.animate_monster_right)
        Clock.unschedule(self.animate_monster_left)
        Window.unbind(on_key_down=self.on_key_down)
        
    def on_key_down(self, window, key, scancode, codepoint, modifier):
        print(f"Key pressed: {key}")  # ตรวจสอบการกดปุ่ม
        if key == 275:  # ลูกศรขวา
            print("Right arrow key pressed!")
            self.hero_shoot("right")
        elif key == 276:  # ลูกศรซ้าย
            print("Left arrow key pressed!")
            self.hero_shoot("left")

    def start_monster_right(self, *args):
        # เริ่ม ฝั่งขวา
        self.ids.monster_image.opacity = 1
        Clock.schedule_interval(self.animate_monster_right, 0.02)

    def start_monster_left(self, *args):
        # เริ่ม ฝั่งซ้าย
        self.ids.monster_image_left.opacity = 1
        Clock.schedule_interval(self.animate_monster_left, 0.02)

    def animate_monster_right(self, dt):
        if self.ids.monster_image.x + self.ids.monster_image.width > 0:
            self.ids.monster_image.x -= self.ryu_speed
            if self.ids.monster_image.opacity == 1 and self.check_collision(self.ids.hero_image, self.ids.monster_image):
                self.game_over()

    def animate_monster_left(self, dt):
        if self.ids.monster_image_left.x < Window.width:
            self.ids.monster_image_left.x += self.ryu1_speed
            if self.ids.monster_image_left.opacity == 1 and self.check_collision(self.ids.hero_image, self.ids.monster_image_left):
                self.game_over()

    def hero_shoot(self, direction):
        if not self.hero_shooting:  # ตรวจสอบว่าไม่กำลังยิงอยู่
            self.hero_shooting = True  # ตั้งค่า flag ว่ากำลังยิง
            if direction == "right":
                self.ids.hero_image.source = "fight_R.png"
                if self.check_collision(self.ids.hero_image, self.ids.monster_image):
                    self.ids.monster_image.opacity = 0
                    Clock.unschedule(self.animate_monster_right)

            elif direction == "left":
                self.ids.hero_image.source = "fight_L.png"
                if self.check_collision(self.ids.hero_image, self.ids.monster_image_left):
                    self.ids.monster_image_left.opacity = 0
                    Clock.unschedule(self.animate_monster_left)

           
            Clock.schedule_once(self.reset_hero_image, 0.2)  # เปลี่ยนภาพ



    def reset_hero_image(self, *args):
        # self.ids.hero_image.canvas.clear()  # ล้าง canvas ก่อนเปลี่ยนภาพ
        self.ids.hero_image.source = "lauren.png"
        print("Image reset to lauren.png")  # ตรวจสอบว่าเปลี่ยนหรือยัง
        self.hero_shooting = False 
    
    def check_collision(self, widget1, widget2):
        w1_x, w1_y = widget1.pos
        w1_width, w1_height = widget1.size
        w2_x, w2_y = widget2.pos
        w2_width, w2_height = widget2.size

        return not (
            w1_x + w1_width < w2_x or
            w1_x > w2_x + w2_width or
            w1_y + w1_height < w2_y or
            w1_y > w2_y + w2_height
        )

    def game_over(self):
        # หยุดการทำงานของ Clock
        Clock.unschedule(self.animate_monster_right)
        Clock.unschedule(self.animate_monster_left)

        self.monster_active = False  # ปิดสถานะการเคลื่อนไหวของมอนสเตอร์
        self.ids.game_over_label.opacity = 1
        Clock.schedule_once(self.return_to_home, 2)

    def return_to_home(self, *args):
        self.manager.current = 'screen_one'

    def go_back(self):
        self.manager.current = 'screen_one'


class PageoneApp(App) :
    def build(self):
        return Builder.load_file('pageone.kv')

if __name__ =='__main__':
    PageoneApp().run()

