import arcade
import settings
from datetime import datetime

class Chapter3View(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu = True
        self.in_game = False
        self.background = arcade.load_texture("55087377-stock-vector-soccer-goal.jpg")
        self.shooter = arcade.Sprite("malePerson_idle.png")
        self.shooter_speed_y = 0.5
        self.shooter_speed_x = 0.5
        self.goalie = arcade.Sprite("maleAdventurer_idle.png", scale=1.3)
        self.goalie_speed_x = 1
        
        self.timer_start = 0

        self.ball_center_x = 400
        self.ball_center_y = 100
        self.goalie.center_x = 400
        self.goalie.center_y = 275
        self.shooter.center_x = 300
        self.shooter.center_y = 50


    def on_show(self):
        if self.menu == True:
            arcade.set_background_color(arcade.color.WHITE)

        elif self.in_game == True:
            arcade.set_background(self.timebackground)
    
    def on_draw(self):
        arcade.start_render()
        if self.menu is True:
            arcade.draw_rectangle_filled(settings.WIDTH/2 - 50, settings.HEIGHT/2 - 50, 100,50, arcade.color.WHITE)
            arcade.draw_text("CLICK ENTER TO START", settings.WIDTH/2 - 50, settings.HEIGHT/2 - 50, 
                         arcade.color.BLUE, font_size=15, anchor_x="center")
        
        if self.menu is True:
            arcade.draw_text("Penalty Game", settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        
            

        
        if self.in_game is True:

            arcade.draw_texture_rectangle(settings.WIDTH/2, settings.HEIGHT/2, settings.WIDTH, settings.HEIGHT, self.background)
            arcade.draw_circle_filled(self.ball_center_x, self.ball_center_y, 25, arcade.color.BLUE)
            self.goalie.draw()
            
        
    
            self.shooter.draw()
    
    def on_update(self, delta_time):
        

        self.goalie.center_x += self.goalie_speed_x

        if self.goalie.center_x < (settings.WIDTH/2) - 140:
            self.goalie_speed_x *= -1
        
        if self.goalie.center_x > (settings.WIDTH/2) + 140:
            self.goalie_speed_x *= -1

        self.goalie.center_x += self.goalie_speed_x

        self.shooter.center_x += self.shooter_speed_x
        self.shooter.center_y += self.shooter_speed_y

        if self.shooter.center_x >= self.ball_center_x and self.shooter.center_y >= self.ball_center_y:
            self.shooter_speed_x = 0 
            self.shooter_speed_y = 0

        self.timer_start += delta_time
        

    


    def on_key_press(self, key, modifiers):
        #self.director.next_view()
        if key == arcade.key.ENTER:
            self.menu = False
            self.in_game = True
        

            self.menu = False
            self.in_game = True

if __name__ == "__main__":
    """This section of code will allow you to run your View
    independently from the main.py file and its Director.

    You can ignore this whole section. Keep it at the bottom
    of your code.

    It is advised you do not modify it unless you really know
    what you are doing.
    """
    from utils import FakeDirector

    window = arcade.Window(settings.WIDTH, settings.HEIGHT, "my game")

    my_view = Chapter3View()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()