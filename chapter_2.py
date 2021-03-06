import arcade
import settings
import random
import time

#Player constants
player_speed = 7
player_jump = 15
player_friction = 0.8
player_scaling = 0.4

#Bullet constants2
bullet_scaling = 0.8
bullet_speed = 10


class Character(arcade.Sprite):
    """Character class

    Attrs:
        filename (str) = name of the resource pack for character image
        center_x (int) = x position of the character
        center_y (int) = y position of the character
        scale (int) = scaling size of the image for the character
    """

    def __init__(self, filename, x, y):
        super().__init__(filename=filename, center_x=x, center_y=y, scale=player_scaling)

        # The amount of height and zoom when the character is being followed across the map
        self.camera_zoom = 500
        self.camera_height = 40

    def update_map_view(self):
        """Returns the x, x1, y, y1 positions for the window view"""
        x = self.center_x - self.camera_zoom
        x1 = self.center_x + self.camera_zoom
        y= self.camera_height - self.camera_zoom
        y1 = self.camera_height + self.camera_zoom

        return x, x1, y, y1

        
class Platforms:
    """Platform class"""

    def __init__(self):
        # Make a list of the platforms
        self.all = arcade.SpriteList()

        # Constants for the platforms
        self.resource_pack = ":resources:/images/tiles/stoneMid.png"
        self.sprite_scaling = 0.2

        self.sprite_size_w = 128
        self.sprite_size_h = 128

    def recursive_platforms(self, y, range_list): 
        """Funcction that makes platforms for the character to land on"""
        s = arcade.Sprite(filename=self.resource_pack, center_x= range_list[0], center_y=y, scale=self.sprite_scaling)
        self.all.append(s)

        range_list[0] += self.sprite_size_w * self.sprite_scaling

        if range_list[0] >= range_list[1]:
            pass
        else:
            self.recursive_platforms(y, range_list )


class Bullet(arcade.Sprite):
    """Bullet class

    Attrs:
        filename (str): name of the resource pack for the bullet image
        view_pointer (class): 
    """

    def __init__(self, filename, view_pointer):
        self.view_pointer = view_pointer
        x = self.view_pointer.camera_position[1] + 15
        y = random.randint(self.view_pointer.camera_position[2], self.view_pointer.camera_position[3])

        super().__init__(filename=filename, center_x=x, center_y=y, scale=bullet_scaling)
        

class Chapter2View(arcade.View):
    def __init__(self):
        super().__init__()
        # In menu, in game, or game over
        self.menu = True
        self.in_game = False
        self.game_over = False

        # Player image
        self.character_height = 128*0.4
        self.player = Character(":resources:/images/animated_characters/male_adventurer/maleAdventurer_idle.png", x=100, y=100)

        # Platforms 
        self.platform_manager = Platforms()

        self.platform_manager.recursive_platforms(y=50, range_list=[0,150])
        self.platform_manager.recursive_platforms(y=200, range_list=[500,1000])
        self.platform_manager.recursive_platforms(y=100, range_list=[170, 400])
        self.platform_manager.recursive_platforms(y=300, range_list=[1100, 1500])
        self.platform_manager.recursive_platforms(y=100, range_list=[1600, 1900])
        self.platform_manager.recursive_platforms(y=200, range_list=[2050, 2300])
        self.platform_manager.recursive_platforms(y=350, range_list=[2400, 2700])
        self.platform_manager.recursive_platforms(y=100, range_list=[2750, 3000])

        # Player movement
        self.key_pressed = {
            arcade.key.W: False,
            arcade.key.A: False,
            arcade.key.D: False, arcade.key.ENTER: False}  
        
        # Physics
        self.physics = arcade.PhysicsEnginePlatformer(self.player, self.platform_manager.all)   
        self.physics.gravity_constant = 0.5

        # Camera position
        self.camera_position = None

        # Bullet list
        self.bullet_list = arcade.SpriteList()
        self.bullet_sprite = ":resources:images/space_shooter/laserBlue01.png"

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE) 

    def on_draw(self):
        arcade.start_render()
        if self.menu is True:
             arcade.draw_text("Chapter 2", settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
             arcade.draw_text("""You're in highschool now, avoid the projectiles
                        \n           by using W,A,D to move around""", 
                         settings.WIDTH/2, settings.HEIGHT/3, arcade.color.BLACK, 
                         font_size=15, anchor_x="center")
             arcade.draw_text("Hit ENTER to continue", settings.WIDTH/2, 
                          settings.HEIGHT/3.6, arcade.color.BLACK, font_size=15,
                          anchor_x="center")
                
        if self.in_game is True:
            self.player.draw()
            self.platform_manager.all.draw()

            # for bullet in self.bullet_list:
                #bullet.draw()
            self.bullet_list.draw()
        
        if self.game_over is True:
            arcade.set_background_color(arcade.color.BLACK)
            arcade.draw_text("Game Over", 100, settings.HEIGHT/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text("Game Over", 500, settings.HEIGHT/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text("Game Over", 900, settings.HEIGHT/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text("Game Over", 1300, settings.HEIGHT/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text("Game Over", 1700, settings.HEIGHT/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text("Game Over", 2100, settings.HEIGHT/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text("Game Over", 2500, settings.HEIGHT/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")
            arcade.draw_text("Game Over", 2900, settings.HEIGHT/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

    def on_key_press(self, key, modifiers):
        # self.director.next_view()

        self.key_pressed[key] = True
    
    def on_key_release(self, key, modifiers):
        self.key_pressed[key] = False
        
    def on_update(self, delta_time):
        self.physics.update()

        # Player movement with keys
        if self.key_pressed[arcade.key.ENTER] == True:
            self.menu = False
            self.in_game = True
        
        if self.key_pressed[arcade.key.A]:
            self.player._set_change_x(-player_speed)

        if self.key_pressed[arcade.key.D]:
            self.player._set_change_x(player_speed)
        
        if self.key_pressed[arcade.key.W] and self.physics.can_jump(5):
            self.physics.jump(player_jump)

        self.player._set_change_x(self.player._get_change_x()*player_friction)

        # Falls off map
        if self.player.center_y <= -500:
            self.player.center_x = 100
            self.player.center_y = 100

        # Map scrolling
        if self.in_game is True:
            x, x1, y, y1 = self.player.update_map_view()

            arcade.set_viewport(x, x1, y, y1)

            self.camera_position = [x, x1, y, y1]

        # Bullet spawning
        for bullet in self.bullet_list:
            bullet.change_x = -bullet_speed
        if round(time.time(), 1) % 10 == 0 and self.in_game is True:
            self.bullet_list.append(Bullet(self.bullet_sprite, self))
        
        # Bullet collides with character
        if self.player.collides_with_list(self.bullet_list):
            self.game_over = True
        
        # Player gets to the last platform
        #if self.player.collides_with_Sprite(self.platform_manager):
          #self.game_over = True

        
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
    arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

    my_view = Chapter2View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
