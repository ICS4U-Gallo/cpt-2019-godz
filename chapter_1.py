import math
import arcade
import settings
import csv


PLAYER_SPEED = 15.0
PLAYER_JUMP = 20.0
PLAYER_GRAVITY = 1.0

class Point:
    """ Convience class representing an x,y cordinate pair"""

    def __init__(self,x ,y):
        self.x = x
        self.y = y


class Platform_manager:
    """ Class responsible for loading prebuilt levels"""

    all = arcade.SpriteList()

    def __init__(self, filename):

        self.csv_path = "levels"
        self.csv_filename = filename
        self.csv_path = f"{self.csv_path}/{self.csv_filename}"

        self.sprite_filename = "test_wall_sprite.png"
        self.sprite_path = "sprites"
        self.sprite_path = f"{self.sprite_path}/{self.sprite_filename}"

        self.sprite_scaling = 1

        with open(self.csv_path) as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=",")

            count = 0

            # Note, the first row of the csv file is meant to be the map width and height in pixels
            for row in csv_reader:        
                if count > 0:
                    s = arcade.Sprite(center_x=float(row[0]),
                                    center_y=float(row[1]),
                                    filename=self.sprite_path,
                                    scale=self.sprite_scaling)
                    self.all.append(s)
                
                else: count += 1


class Player(arcade.Sprite):
    def __init__(self, starting_x, starting_y):

        self.sprite_scaling = 1
        
        #All caps to prevent the overriding of inhereted attributes
        self.SPEED = 15.0 
        self.JUMP = 20.0
        self.GRAVITY = 1.0

        self.character_path = "sprites"
        self.character_sprite = "test_char_sprite.png"
        self.character_sprite_path = f"{self.character_path}/{self.character_sprite}"

        super().__init__(filename=self.character_sprite_path,
                        center_x=starting_x,
                        center_y=starting_y,
                        scale=self.sprite_scaling)


    def screen_location(self):
        """Returns two x,y pairs represeting the camera view relative to the player"""


        x = self.center_x - (settings.WIDTH / 2)
        x1 = self.center_x + (settings.WIDTH / 2)

        y = self.center_y - (settings.HEIGHT / 2)
        y1 = self.center_y + (settings.HEIGHT / 2)

        return x, x1, y, y1


class Chapter1View(arcade.View):
    def __init__(self):

        super().__init__()

        self.player = Player(starting_x=300 ,starting_y=50)

        self.platform_manager = Platform_manager("level1.csv")

        # Initializing a physics engine instance.
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.platform_manager.all)
        self.physics_engine.gravity_constant = self.player.GRAVITY

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

        # Adjusting the viewport (camera)
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

    my_view = Chapter1View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
