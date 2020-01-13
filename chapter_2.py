import math
import arcade
import settings
import csv


PLAYER_SPEED = 15.0
PLAYER_JUMP = 20.0
PLAYER_GRAVITY = 1.0

class Point:
    def __init__(self,x ,y):
        self.x = x
        self.y = y

class Keyboard_controller:
    def __init__(self):

        self.A = False
        self.D = False
        self.space = False


class Platform(arcade.Sprite):
    n_image_scale = 1
    platform_size = [20, 20]

    def __init__(self, x, y, filename):
        
        self.file_extension = "png"
        self.path = f"sprites/{filename}.{self.file_extension}"

        super().__init__(center_x=x, center_y=y, filename=self.path)


class Platform_manager:
    all = arcade.SpriteList()

    def __init__(self, level_num):

        self.path = "levels"
        self.file_extension = "csv"

        self.complete_path = f"{self.path}/level{level_num}.{self.file_extension}"

        with open(self.complete_path) as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=",")

            count = 0

            for row in csv_reader:
                
                if count != 0:
                    self.all.append(Platform(float(row[0]), float(row[1]), "test_wall_sprite"))
                
                else:
                    count += 1


class Grapple:
    reduction_factor = 0.1

    def __init__(self,Player_pointer, target_pos):

        self.player_pointer = Player_pointer
        self.target_pos = target_pos
    
    def distance_delta(self):
        p = self.player_pointer._position
        
        delta_x = p.x - self.target_pos.x
        delta_y = p.y - self.target_pos.y

        return Point(delta_x * self.reduction_factor, delta_y * self.reduction_factor)    


class Player(arcade.Sprite):
    n_image_scale = 2
    n_player_size = [20, 20]

    def __init__(self, sprite_dir, starting_x, starting_y):
        super().__init__(scale=Player.n_image_scale, filename=sprite_dir, center_x=starting_x, center_y=starting_y)

        self.allowing_jumps = True

    def screen_location(self):

        x = self.center_x - (settings.WIDTH / 2)
        x1 = self.center_x + (settings.WIDTH / 2)

        y = self.center_y - (settings.HEIGHT / 2)
        y1 = self.center_y - (settings.HEIGHT / 2)

        return x, x1, y, y1


class Chapter1View(arcade.View):
    def __init__(self, player_pointer):

        super().__init__()

        self.player = player_pointer

        self.platform_manager = Platform_manager(1)

        self.key_control = Keyboard_controller()

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.platform_manager.all, PLAYER_GRAVITY)

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)
    
    def on_draw(self):
        arcade.start_render()
    
        self.player.draw()
   
        self.platform_manager.all.draw()
        
    def on_key_press(self, key, modifiers):
        #self.director.next_view()

        if key == arcade.key.D:
            self.player._set_change_x(PLAYER_SPEED)

        if key == arcade.key.A:
            self.player._set_change_x(-PLAYER_SPEED)

        if key == arcade.key.SPACE and self.physics_engine.jumps_since_ground <= 2:
            self.physics_engine.jump(PLAYER_JUMP)

    def on_key_release(self, key, modifiers):
        
        if key == arcade.key.A:
            self.player._set_change_x(0)

        if key == arcade.key.D:
            self.player._set_change_x(0)

    def on_update(self, delta_time:float):
        
        self.physics_engine.update()

        x, x1, y, y1 = self.player.screen_location()
        arcade.set_viewport(x, x1, y, y1)
        
if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.

    You can ignore this whole section. Keep it at the bottom
    of your code.

    It is advised you do not modify it unless you really know
    what you are doing.
    """

    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    
    player = Player("sprites/test_char_sprite.png", 300 ,50)

    my_view = Chapter1View(player)
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
