mport arcade
import settings
from datetime import datetime
from typing import List
import time
import json

time_game = 60
start_time = time.time()
end_time = time.time()


sorted_list = []



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
            arcade.set_background(self.background)

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
                self.in_game = True
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

        global points
        points = self.points
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
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        view_score = ViewScore()
        self.window.show_view(view_score)


class ViewScore(arcade.View):
    """Shows player's time after completing the maze"""

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        score = points
        arcade.draw_text(f"Your Score: {score}",
                         settings.WIDTH / 2, settings.HEIGHT / 2,
                         arcade.color.TEAL, font_size=10, anchor_x="center")

    def on_show(self):
        # Set the background color
        arcade.set_background_color(arcade.color.BONE)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        score = points
        with open("scores.json", "r") as f:
            data = json.load(f)

        data[f"score {len(data) + 1}"] = score

        with open("scores.json", 'w') as f:
            json.dump(data, f)

        # Transition to highscore view
        highscores = Highscores()
        self.window.show_view(highscores)


class Highscores(arcade.View):
    """Shows a list of scores"""

    @classmethod
    def on_show(cls):
        # Set the background color
        arcade.set_background_color(arcade.color.BONE)

    @classmethod
    def on_draw(cls):
        """Render the screen."""
        arcade.start_render()
        score = points
        height_decrease = 120
        sorted_list = []
        with open("scores.json", "r") as f:
            data = json.load(f)

        # Displaying the scores from shortest to longest times
        for values in data.values():
            sorted_list.append(values)
            sorted_list2 = merge_sort(sorted_list)
        arcade.draw_text(f"Highscores: \n", settings.WIDTH / 2,
                         settings.HEIGHT - 200,
                         arcade.color.TEAL, font_size=18, anchor_x="center")

        # Only displays 5 scores
        for i in reversed(range(0, 5)):
            arcade.draw_text(f"{i + 1}: {sorted_list2[i]} \n",
                             settings.WIDTH / 2,
                             settings.HEIGHT - 200 - height_decrease,
                             arcade.color.TEAL, font_size=18,
                             anchor_x="center")
            height_decrease -= 20

        # Display text
        arcade.draw_text(f"Your Score: {score}", settings.WIDTH / 2,
                         settings.HEIGHT / 2 - 100,
                         arcade.color.TEAL, font_size=18, anchor_x="center")
        arcade.draw_text("Click to continue", settings.WIDTH / 2,
                         settings.HEIGHT / 2 - 250,
                         arcade.color.TEAL, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.close()


def merge_sort(numbers: List[int]) -> List[int]:
    """Sorts the items in a list
    Args:
        numbers: list of integers
    Returns:
        the list of integers from smallest to largest value
    """
    # merge sort
    # Base case
    if len(numbers) == 1:
        return numbers

    midpoint = len(numbers) // 2

    # Two recursive steps
    # Mergesort left
    left_side = merge_sort(numbers[:midpoint])
    # Mergesort right
    right_side = merge_sort(numbers[midpoint:])
    # Merge the two together
    sorted_list = []

    # Loop through both lists with two markers
    left_marker = 0
    right_marker = 0
    while left_marker < len(left_side) and right_marker < len(right_side):
        # If left value less than right value, add right value to sorted
        # increase left marker
        if left_side[left_marker] > right_side[right_marker]:
            sorted_list.append(left_side[left_marker])
            left_marker += 1
        # If right value less than left value, add left value to sorted
        # increase right marker
        else:
            sorted_list.append(right_side[right_marker])
            right_marker += 1

    # Create a while loop to gather the rest of the values from either list
    while right_marker < len(right_side):
        sorted_list.append(right_side[right_marker])
        right_marker += 1

    while left_marker < len(left_side):
        sorted_list.append(left_side[left_marker])
        left_marker += 1

    # Return the sorted list
    return sorted_list


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
