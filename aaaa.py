import arcade
import settings
from datetime import datetime
import time
import json

time_game = 60
start_time = time.time()
end_time = time.time()
FRICTION = 0.5


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
        self.ball = arcade.Sprite("soccer_ball.png", scale=0.08)

        self.timer_start = 0

        self.ball.center_x = 400
        self.ball.center_y = 100
        self.goalie.center_x = 400
        self.goalie.center_y = 275
        self.shooter.center_x = 300
        self.shooter.center_y = 50
        self.radar_speed_x = 2
        self.radar_speed_y = 0
        self.start_ball_x = self.ball.center_x
        self.end_ball_x = self.ball.center_x
        self.start_ball_y = self.ball.center_y
        self.end_ball_y = self.ball.center_y + 100
        self.shot_state = 0
        self._start_time = time.time()
        self._stop_game = False
        self.name = " "
        self.submit_name = False

        self.points = 0

        self.ball_speed_x = 0
        self.ball_speed_y = 0

    def reset_game(self):
        self.shooter.center_x = 300
        self.shooter.center_y = 50
        self.radar_speed_x = 2
        self.radar_speed_y = 0
        self.ball.center_x = 400
        self.ball.center_y = 100
        self.start_ball_x = self.ball.center_x
        self.end_ball_x = self.ball.center_x
        self.start_ball_y = self.ball.center_y
        self.end_ball_y = self.ball.center_y + 100
        self.shot_state = 0
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.shooter_speed_x = 0.5
        self.shooter_speed_y = 0.5

    def get_timeleft(self):
        end_time = time.time()
        return time_game - int((end_time - self._start_time))

    def on_show(self):
        if self.menu == True:
            arcade.set_background_color(arcade.color.WHITE)

        elif self.in_game == True:
            arcade.set_background(self.timebackground)

    def on_draw(self):
        arcade.start_render()
        if self.menu is True:
            arcade.draw_rectangle_filled(settings.WIDTH / 2 - 50, settings.HEIGHT / 2 - 50, 100, 50, arcade.color.WHITE)
            arcade.draw_text("ENTER NAME AND CLICK ENTER TO START", settings.WIDTH / 2 - 50, settings.HEIGHT / 2 - 50,
                             arcade.color.BLUE, font_size=15, anchor_x="center")

            arcade.draw_text("Penalty Game", settings.WIDTH / 2, settings.HEIGHT / 2,
                             arcade.color.BLACK, font_size=30, anchor_x="center")

            arcade.draw_text(f"Hello {self.name}", 400, 100, arcade.color.BLACK, 24)

        if self.in_game is True:

            arcade.draw_texture_rectangle(settings.WIDTH / 2, settings.HEIGHT / 2, settings.WIDTH, settings.HEIGHT,
                                          self.background)
            # arcade.draw_circle_filled(int(self.ball_center_x), int(self.ball_center_y), 25, arcade.color.BLUE)
            self.goalie.draw()
            self.ball.draw()

            if self.ball_speed_x == 0 and self.ball_speed_y == 0:
                arcade.draw_line(self.ball.center_x, self.ball.center_y, self.end_ball_x, self.end_ball_y,
                                 arcade.color.WHITE)

            self.shooter.draw()

            if self.get_timeleft() > 0 and self._stop_game == False:
                arcade.draw_text("Time Left: " + str(self.get_timeleft()) + " seconds", 300, 10, arcade.color.BLACK,
                                 font_size=25, anchor_x="center")
            else:
                self._stop_game = True
                self.in_game = False
                self.menu = True
                arcade.draw_text("Game Over", 400, 300, arcade.color.WHITE, font_size=30, anchor_x="center")

            arcade.draw_text(str(self.points), 20, 20, arcade.color.WHITE, font_size=40, anchor_x="center")

    def on_update(self, delta_time):

        if self.goalie.center_x < (settings.WIDTH / 2) - 140:
            self.goalie_speed_x *= -1

        if self.goalie.center_x > (settings.WIDTH / 2) + 140:
            self.goalie_speed_x *= -1

        self.goalie.center_x += self.goalie_speed_x

        self.shooter.center_x += self.shooter_speed_x
        self.shooter.center_y += self.shooter_speed_y

        if self.ball.collides_with_sprite(self.goalie) is False:
            if self.ball.center_x > (settings.WIDTH / 2) - 150 and self.ball.center_x < (settings.WIDTH / 2) + 150:
                if self.ball.center_y > (settings.HEIGHT / 2) - 100 and self.ball.center_y < 600:
                    self.points += 1

                    self.reset_game()

        else:
            self.reset_game()

        print(self.points)

        if self.shooter.center_x >= self.ball.center_x and self.shooter.center_y >= self.ball.center_y:
            self.shooter_speed_x = 0
            self.shooter_speed_y = 0

        self.timer_start += delta_time

        if self.end_ball_x < (settings.WIDTH / 2) - 300:
            self.radar_speed_x *= -1

        if self.end_ball_x > (settings.WIDTH / 2) + 300:
            self.radar_speed_x *= -1

        self.end_ball_x += self.radar_speed_x

        if self.end_ball_y < (settings.HEIGHT / 2) - 100:
            self.radar_speed_y *= -1

        if self.end_ball_y > (settings.HEIGHT / 2) + 100:
            self.radar_speed_y *= -1

        self.end_ball_y += self.radar_speed_y

        if self.ball.center_y >= self.end_ball_y:
            self.ball_speed_x = 0
            self.ball_speed_y = 0

        self.ball.center_x += self.ball_speed_x
        self.ball.center_y += self.ball_speed_y

    def on_key_press(self, key, modifiers):
        # self.director.next_view()
        if key == arcade.key.ENTER:
            self.menu = False
            self.in_game = True
            self.submit_name = True

        if key == arcade.key.SPACE and self.shot_state == 0:
            self.radar_speed_x = 0
            self.radar_speed_y = 2
            self.shot_state = 1


        elif key == arcade.key.SPACE and self.shot_state == 1:
            self.radar_speed_y = 0
            self.shot_state = 2

            self.ball_speed_x = (self.end_ball_x - self.ball.center_x) / 30
            self.ball_speed_y = (self.end_ball_y - self.ball.center_y) / 30

        if self.menu is True and key != arcade.key.ENTER and key != arcade.key.BACKSPACE and self.submit_name is False:
            self.name += chr(key)

        elif self.menu is True and key == arcade.key.BACKSPACE and self.submit_name is False:
            self.name = self.name[:-1]

    def on_key_release(self, key, modifiers):
        if key == arcade.key.ENTER:
            with open('scores.json', 'r') as f:
                scores = json.loads(f.read())

            scores.setdefault(key,[]).append(self.name)

            with open("scores.json", "w") as f:
                json.dump(scores, f)

            #with open('scores.json', 'w', encoding='utf-8') as f:
             #   json.dump(scores, f, ensure_ascii=False, indent=4)


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
