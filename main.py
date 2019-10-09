import sys, logging, os, random, math, open_color, arcade, time


version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])


logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Cat Shooting Gallery"

NUM_ENEMIES = 10
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 50
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        
        super().__init__("assets/New Piskel (1).gif", 0.2)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/Cat Robot.gif", 0.4)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
    
        super().__init__("assets/target.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position  
            






class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(False)
        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        self.start = time.time()   
          

    def setup(self):
     
        


        for i in range(NUM_ENEMIES):
            x = random.randint(100,900)
            y = random.randint(100,500)
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)            

    def update(self, delta_time):
        self.bullet_list.update()
        for e in self.enemy_list:
           boolets = arcade.check_for_collision_with_list(e,self.bullet_list)
           for b in boolets:
               e.hp = e.hp - b.damage
               b.kill()
               if e.hp <= 0:
                   e.kill()
                   self.score = self.score + 100
        
                   
        

    def on_draw(self):
        arcade.start_render()
        if self.score >= 1000:
            arcade.draw_text("Congratulations! A nerd is you!", 160, 300, arcade.color.GREEN, 40)
        else:
            current = time.time()
            elapsed = self.start - current
            self.bullet_list.draw()
            self.enemy_list.draw()
            arcade.draw_text(str(elapsed), SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40, arcade.color.GREEN, 16)
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, arcade.color.GREEN, 16)
        self.player.draw()
           

    def on_mouse_motion(self, x, y, dx, dy):
     
        self.player.center_x = x
        self.player.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
                x = self.player.center_x
                y = self.player.center_y + 15
                bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
                self.bullet_list.append(bullet)


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
    



if __name__ == "__main__":
    main()