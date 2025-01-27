from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from random import randint
from kivy.core.audio import SoundLoader

resource_add_path('D:\\New folder (2)\debug-font')
LabelBase.register(DEFAULT_FONT, 'DebugF.otf')

WINDOW_WIDTH = 564
WINDOW_HEIGHT =317
Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)
Window.resizable = False


resource_add_path('D:\\New folder (2)\debug-font')
LabelBase.register(DEFAULT_FONT, 'DebugF.otf')

def enforce_fixed_size(window, width, height):
    if width != WINDOW_WIDTH or height != WINDOW_HEIGHT:
        Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

Window.bind(on_resize=enforce_fixed_size)

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
        self.game_over_flag = False
        self.ryu_speed = 5  
        self.ryu1_speed = 5
        self.ryu_initial_x = Window.width 
        self.ryu1_initial_x = -200

        self.hero_facing_right = True
        self.monster_active = False  
        self.hero_shooting = False
        self.hero_image = None  # กำหนดค่าเริ่มต้นของ hero_image
        # self.attack_effect_right = None  # กำหนดค่าเริ่มต้นของ effect_image
        # self.attack_effect_left = None
        self.score = 0  # คะแนนเริ่มต้น
        self.monster_active = True


       
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

    def on_parent(self, instance, parent):
        # เมื่อวิวถูกเพิ่มไปยัง parent (Kivy เรียกใช้ในเวลานี้)
        if parent:
            self.hero_image = self.ids.hero_image  # เข้าถึง hero_image ที่นี่
            self.hero_attack_image_right = self.hero_attack_image_right
            self.hero_attack_image_left = self.hero_attack_image_left
            self.attack_effect_right = self.ids.attack_effect_right  # เข้าถึง effect_image ที่นี่
            self.attack_effect_left = self.ids.attack_effect_left 
            

    def on_enter(self):
        self.ids.monster_image_right.opacity = 0
        self.ids.monster_image_left.opacity = 0

        self.ids.monster_image_right.pos = (Window.width + 100, 120)
        self.ids.monster_image_left.pos = (-200, 120)

        self.ids.score_label.text = f"RYU{self.score}"  # อัปเดตคะแนน
        self.ids.monster_image_right.opacity = 1
        self.ids.monster_image_left.opacity = 1

        # เริ่มเคลื่อนที่มอนสเตอร์
        Clock.schedule_interval(self.animate_monster_right, 0.1)
        Clock.schedule_interval(self.animate_monster_left, 0.1)
        
        self.monster_active = True

        Window.bind(on_key_down=self.on_key_down)


    def on_leave(self):
        self.ids.monster_image_right.opacity = 0
        self.ids.monster_image_left.opacity = 0
        Clock.unschedule(self.animate_monster_right)
        Clock.unschedule(self.animate_monster_left)
        self.reset_monster(self.ids.monster_image_right)
        self.reset_monster(self.ids.monster_image_left)

        Window.unbind(on_key_down=self.on_key_down)
        
    def on_key_down(self, window, key, scancode, codepoint, modifier):
        print(f"Key pressed: {key}")  # ตรวจสอบการกดปุ่ม
        if key == 275:  # ลูกศรขวา
            print("Right arrow key pressed!")
            self.hero_shoot("right")  # เรียกฟังก์ชัน hero_shoot("right")
            self.ids.hero_image.opacity = 0
        elif key == 276:  # ลูกศรซ้าย
            print("Left arrow key pressed!")
            self.hero_shoot("left")  # เรียกฟังก์ชัน hero_shoot("left")
            self.ids.hero_image.opacity = 0

    def on_key_up(self, window, key, scancode):
        print(f"Key released: {key}")  # ตรวจสอบเมื่อปล่อยปุ่ม
        self.reset_hero_image()
       

    def start_monster_right(self, *args):
        # เริ่ม ฝั่งขวา
        self.ids.monster_image_right.opacity = 1
        Clock.schedule_interval(self.animate_monster_right, 0.03)

    def start_monster_left(self, *args):
        # เริ่ม ฝั่งซ้าย
        self.ids.monster_image_left.opacity = 1
        Clock.schedule_interval(self.animate_monster_left, 0.03)

    def update_monsters(self, dt):
        for monster in [self.ids.monster_image_left, self.ids.monster_image_right]:
            monster.x += 5 if "right" in monster.id else -5
            if monster.x < -monster.width or monster.x > Window.width:
                self.reset_monster(monster)
            self.check_collision()

    def animate_monster_right(self, dt):
        if self.ids.monster_image_right.opacity == 1:
            self.ids.monster_image_right.x -= self.ryu_speed
        
            monster_pos = self.ids.monster_image_right.x
            hero_pos = self.ids.hero_image.x
            distance = abs(monster_pos - hero_pos)

            if distance < 100:  # ปรับระยะนี้ตามที่ต้องการ เช่น < 100
                if self.check_collision(self.ids.hero_image, self.ids.monster_image_right):
                    self.game_over()

            


            if self.ids.monster_image_right.x < self.ids.hero_image.x + 200:  
                if self.check_collision(self.ids.hero_image, self.ids.monster_image_right):
                    self.game_over() 

            if self.ids.monster_image_right.x < -200:
                self.reset_monster(self.ids.monster_image_right)


            if self.check_collision(self.ids.hero_image, self.ids.monster_image_right):
                print("Collision detected!")
                self.game_over()  

   

    def animate_monster_left(self, dt):
        if self.ids.monster_image_left.opacity == 1:
            self.ids.monster_image_left.x += self.ryu1_speed

            monster_pos = self.ids.monster_image_left.x
            hero_pos = self.ids.hero_image.x
            distance = abs(monster_pos - hero_pos)
            
            # ตรวจจับการชนเมื่อมอนสเตอร์เข้าใกล้มากขึ้น 
            if distance < 100:  # ปรับระยะนี้ตามที่ต้องการ เช่น < 100
                if self.check_collision(self.ids.hero_image, self.ids.monster_image_left):
                    self.game_over()

            if self.check_collision(self.ids.hero_image, self.ids.monster_image_left):
                self.game_over()

            if self.ids.monster_image_left.x > self.ids.hero_image.x - 50:  
                if self.check_collision(self.ids.hero_image, self.ids.monster_image_left):
                    self.game_over()  

            if self.ids.monster_image_left.x > Window.width + 200:
                self.reset_monster(self.ids.monster_image_left)


    def reset_monster(self, monster):
            monster_name = "right" if monster is self.ids.monster_image_right else "left"
            monster.x = Window.width + randint(100, 300) if monster_name == "right" else -randint(100, 300)

    def hero_shoot(self, direction):
        if direction == "right":
            self.ids.hero_attack_image_right.opacity = 1  # แสดงภาพโจมตีขวา
            Clock.schedule_once(self.check_hit_right, 0.1)
            self.ids.hero_attack_image_left.opacity = 0  # ซ่อนภาพโจมตีซ้าย
            self.ids.hero_image.source = "fight_R.png"  # เปลี่ยนภาพตัวละครเป็นภาพโจมตี
            self.ids.hero_image.opacity = 0  # ซ่อนภาพตัวละครเมื่อโจมตี
            self.ids.attack_effect_right.source = "effect_R.png"  # เปลี่ยนเอฟเฟกต์ขวา
            self.ids.attack_effect_right.opacity = 1  # แสดงเอฟเฟกต์การโจมตี
        elif direction == "left":
            self.ids.hero_attack_image_left.opacity = 1  # แสดงภาพโจมตีซ้าย
            Clock.schedule_once(self.check_hit_left, 0.1)
            self.ids.hero_attack_image_right.opacity = 0  # ซ่อนภาพโจมตีขวา
            self.ids.hero_image.source = "fight_L.png"  # เปลี่ยนภาพตัวละครเป็นภาพโจมตี
            self.ids.hero_image.opacity = 0  # ซ่อนภาพตัวละครเมื่อโจมตี
            self.ids.attack_effect_left.source = "effect_L.png"  # เปลี่ยนเอฟเฟกต์ซ้าย
            self.ids.attack_effect_left.opacity = 1  # แสดงเอฟเฟกต์การโจมตี

    def check_hit_right(self, *args):
        if self.check_collision(self.ids.attack_effect_right, self.ids.monster_image_right):
            self.score += 1
            self.ids.score_label.text = f"RYU {self.score}"
            self.reset_monster(self.ids.monster_image_right)
        self.ids.attack_effect_right.opacity = 0

    def check_hit_left(self, *args):
        if self.check_collision(self.ids.attack_effect_left, self.ids.monster_image_left):
            self.score += 1
            self.ids.score_label.text = f"RYU  {self.score}"
            self.reset_monster(self.ids.monster_image_left)
        self.ids.attack_effect_left.opacity = 0

    def reset_hero_image(self):
        self.ids.hero_image.canvas.clear()
        self.ids.hero_image.source = "lauren.png"  # เปลี่ยนภาพกลับเป็นภาพเริ่มต้น
        self.ids.hero_image.opacity = 1  # แสดงภาพเริ่มต้น
        self.ids.hero_attack_image_right.opacity = 0  # ซ่อนภาพโจมตีขวา
        self.ids.hero_attack_image_left.opacity = 0  # ซ่อนภาพโจมตีซ้าย
        self.ids.attack_effect_right.opacity = 0  # ซ่อนเอฟเฟกต์ขวา
        self.ids.attack_effect_left.opacity = 0  # ซ่อนเอฟเฟกต์ซ้าย
        print("Image reset to lauren.png")  # ตรวจสอบว่าเปลี่ยนหรือยัง
        self.hero_shooting = False
        
    def check_collision(self, widget1, widget2):
        # print(f"Hero: {widget1.pos}, Monster: {widget2.pos}")
        if widget1.collide_widget(widget2):
            # print("Collision detected!")
            return True
        return False

    
    game_over_flag = False
    def game_over(self):
        if not self.game_over_flag:  # เรียก game_over ได้เพียงครั้งเดียว
            self.game_over_flag = True
            print("Game Over!")
            self.manager.get_screen('game_over_screen').ids.game_over_label.opacity = 1
            self.manager.get_screen('game_over_screen').ids.score_label.text = f"RYU Score  {self.score}"
            self.manager.current = "game_over_screen"  # เปลี่ยนไปหน้า game over
    
    # def game_over(self):
    #     if self.monster_active and not self.game_over_flag:  # ตรวจสอบสถานะเกมก่อน
    #         self.game_over_flag = True
    #         self.monster_active = False  # หยุดการทำงานของมอนสเตอร์
    #         Clock.unschedule(self.animate_monster_right)  # หยุดการเคลื่อนที่ของมอนสเตอร์
    #         Clock.unschedule(self.animate_monster_left)
            
        
    #         self.manager.get_screen('game_over_screen').ids.score_label.text = f"RYU Score {self.score}"
    #         self.manager.current = "game_over_screen"


    def return_to_home(self, *args):
        self.manager.current = 'screen_one'

    def go_back(self):
        self.manager.current = 'screen_one'
    
    



class GameOverScreen(Screen):
    def restart_game(self):
        """ฟังก์ชันสำหรับเริ่มเกมใหม่"""
        self.manager.get_screen('screen_three').reset_game_state()
        self.manager.current = 'screen_three'

class PageoneApp(App) :
    def build(self):
        self.sound = SoundLoader.load("D:\ShootingGame\pixel-song.mp3") 
        if self.sound:
            self.sound.loop = True  # ทำให้เสียงเล่นวน
            self.sound.play()  

        return Builder.load_file('pageone.kv')
    def reset_game(self):
        """รีเซ็ตเกมเมื่อกลับไปหน้าแรก"""
        screen_three = self.root.get_screen("screen_three")
        screen_three.game_over_flag = False
        screen_three.score = 0
        screen_three.reset_monster(screen_three.ids.monster_image_left)
        screen_three.reset_monster(screen_three.ids.monster_image_right)


if __name__ =='__main__':
    PageoneApp().run()

