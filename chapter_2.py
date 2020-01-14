import arcade
import settings


class Character(arcade.Sprite):
    pass



class Platform(arcade.Sprite):
    def __init__(self, filename, x, y):
        super().__init__(filename, x, y)



class Chapter2View(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu = True
        self.in_game = False

        self.list_of_platforms = arcade.SpriteList()

        self.player = Character(":resources:/images/animated_characters/male_adventurer/maleAdventurer_idle.png", center_x=100, center_y=100)

        self.physics = arcade.PhysicsEnginePlatformer(self.player, self.list_of_platforms, 2)   

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        pass 

    def on_draw(self):
        arcade.start_render()
        if self.menu is True:
             arcade.draw_text("Chapter 2", settings.WIDTH/2, settings.HEIGHT/2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
             arcade.draw_text("""You're in highschool now, avoid the projectiles
                        \nby using the arrows to move around""", settings.WIDTH/2,
                         settings.HEIGHT/4, arcade.color.BLACK, font_size=15,
                         anchor_x="center")

        
        if self.in_game is True:
            self.player.draw()

    def on_key_press(self, key, modifiers):
        #self.director.next_view()

        if key == arcade.key.ENTER:
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
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    arcade.set_background_color(arcade.color.AIR_SUPERIORITY_BLUE)

    my_view = Chapter2View()
    my_view.director = FakeDirector(close_on_next_view=True)
    my_view.setup()
    window.show_view(my_view)
    arcade.run()

