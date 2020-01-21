import arcade 
import settings
from datetime import datetime
from typing import List
import time
import json

time_game = 60  # length of game "time"
start_time = time.time()
end_time = time.time()

sorted_list = []  # Sorted list of scores

class Chapter3View(arcade.View):  # Chapter3View class
    
    def __init__(self):
        super().__init__()
        self.menu = True
        self.in_game = False     
        
        # background image
        self.background = arcade.load_texture("55087377-stock-vector-soccer-goal.jpg")
        
        self.shooter = arcade.Sprite("malePerson_idle.png")  # Character Sprite
        
        # Speed of shooter in x and y axis
        self.shooter_speed_y = 0.5 
        self.shooter_speed_x = 0.5 
        
        # Location of shooter in x and y axis
        self.shooter.center_x = 300
        self.shooter.center_y = 50
        
        # goalie sprite
        self.goalie = arcade.Sprite("maleAdventurer_idle.png", scale=1.3)
        
        # Location of goalie x and y axis
        self.goalie.center_x = 400
        self.goalie.center_y = 275
        
        # Speed of goalie in x-axis
        self.goalie_speed_x = 1
        
        self.ball = arcade.Sprite("soccer_ball.png", scale=0.08)  # ball sprite
        
        # Position of ball in x and y axis
        self.ball.center_x = 400
        self.ball.center_y = 100
        
        self.start_ball_x = self.ball.center_x
        self.end_ball_x = self.ball.center_x
        self.start_ball_y = self.ball.center_y
        self.end_ball_y = self.ball.center_y + 100
        
        # Speed of ball in x and y axis
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        
        # Speed of line in x and y axis
        self.radar_speed_x = 2
        self.radar_speed_y = 0
        self.shot_state = 0  # number of times SPACE has been pressed
        self._start_time = time.time()  # begin time
        self._stop_game = False  # Game starts method
        self.name = " "  # name you enter on the beginning of the screen
        self.submit_name = False  # name you type
        self.timer_start = 0
        self.points = 0  # Number of points the game starts with

    def reset_game(self):
        """ reset function which resets the part of the game 
            where the ball is shot. Game goes back to originall 
            ball positon, player postion, goalie position
            and radar postion.
        """
        
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
        """ Function that states how much time is left as shown on the screen
        """
        end_time = time.time()
        return time_game - int((end_time - self._start_time))

    def on_show(self):
        # background is set as the color white when game is in menu.
        if self.menu is True:
            arcade.set_background_color(arcade.color.WHITE)

        # background is set as the in game image when it is in game.
        elif self.in_game is True:
            arcade.set_background(self.background) 

    def on_draw(self):
        """ Draw function of the menu and in game images and characters
        """
        arcade.start_render()
        if self.menu is True:
            arcade.draw_rectangle_filled(settings.WIDTH / 2 - 50, 
                                         settings.HEIGHT / 2 - 50, 
                                         100, 50, arcade.color.WHITE)
            arcade.draw_text("ENTER NAME AND CLICK ENTER TO START", 
                             settings.WIDTH / 2 - 50, 
                             settings.HEIGHT / 2 - 50, 
                             arcade.color.BLUE, 
                             font_size=15,
                             anchor_x="center")

            arcade.draw_text("Penalty Game", settings.WIDTH / 2, 
                             settings.HEIGHT / 2,
                             arcade.color.BLACK, font_size=30, 
                             anchor_x="center")

            arcade.draw_text(f"Hello {self.name}", 400, 100, 
                             arcade.color.BLACK, 24)
            arcade.draw_text("Click the screen with mouse to quit and see your score", 
                             100, 450, arcade.color.BLACK, 
                             15)

        if self.in_game is True:
            # When it is in the game, draw these characters and images
            arcade.draw_texture_rectangle(settings.WIDTH / 2, 
                                          settings.HEIGHT / 2, 
                                          settings.WIDTH, 
                                          settings.HEIGHT, self.background)
            self.goalie.draw()
            self.ball.draw()

            if self.ball_speed_x == 0 and self.ball_speed_y == 0:
                arcade.draw_line(self.ball.center_x, self.ball.center_y, 
                                 self.end_ball_x, 
                                 self.end_ball_y, arcade.color.WHITE)

            self.shooter.draw()

            if self.get_timeleft() > 0 and self._stop_game is False:
                arcade.draw_text("Time Left: " + str(self.get_timeleft()) + " seconds",
                                 300, 10, arcade.color.BLACK, font_size=25, 
                                 anchor_x="center")
            else:
                self._stop_game = True
                self.in_game = True
                arcade.draw_text("Game Over", 400, 300, 
                                 arcade.color.WHITE, font_size=30, 
                                 anchor_x="center")
            arcade.draw_text(str(self.points), 20, 20, arcade.color.WHITE, 
                             font_size=40, anchor_x="center")
            arcade.draw_text("Click Space to aim, and the second time you press it, it will shoot", 
                             100, 500, arcade.color.BLACK, 
                             15)
            arcade.draw_text("Click the screen with mouse to quit and see your score", 
                             100, 450, arcade.color.BLACK, 
                             15)

    def on_update(self, delta_time):
        
        # goalie moves from one post to another
        if self.goalie.center_x < (settings.WIDTH / 2) - 140:
            self.goalie_speed_x *= -1

        if self.goalie.center_x > (settings.WIDTH / 2) + 140:
            self.goalie_speed_x *= -1

        self.goalie.center_x += self.goalie_speed_x
        
        # makes the shooter move diagonally
        self.shooter.center_x += self.shooter_speed_x
        self.shooter.center_y += self.shooter_speed_y

        # if ball doesn't collide with the goalie
        if self.ball.collides_with_sprite(self.goalie) is False:
            # if the ball is in between the two posts
            if self.ball.center_x > (settings.WIDTH / 2) - 150 and self.ball.center_x < (settings.WIDTH / 2) + 150:
            # if the ball is under the length of the crossbar   
                if self.ball.center_y > (settings.HEIGHT / 2) - 100 and self.ball.center_y < 600:
                    # points represents goals
                    self.points += 1
                    # reset game when ball reaches goal
                    self.reset_game()

        else:
            # no goal and game resets
            self.reset_game()

        # global variable for points
        global points
        points = self.points

        # shooter reaches the initial postion of ball, stop his movement
        if self.shooter.center_x >= self.ball.center_x and self.shooter.center_y >= self.ball.center_y:
            self.shooter_speed_x = 0
            self.shooter_speed_y = 0

        # starting the timer in the game
        self.timer_start += delta_time

        # (x) radar speed changes as it hits right side of screen
        if self.end_ball_x < (settings.WIDTH / 2) - 300:
            self.radar_speed_x *= -1
        # (x) radar speed changes as it hits left side of screen
        if self.end_ball_x > (settings.WIDTH / 2) + 300:
            self.radar_speed_x *= -1

        self.end_ball_x += self.radar_speed_x

        # (y) radar speed changes as it hits top of screen
        if self.end_ball_y < (settings.HEIGHT / 2) - 100:
            self.radar_speed_y *= -1

        # (y) radar speed changes as it hits bottom of screen
        if self.end_ball_y > (settings.HEIGHT / 2) + 100:
            self.radar_speed_y *= -1

        self.end_ball_y += self.radar_speed_y

        """ once ball reaches its final position,
            ball's speed of x and y is 0
        """
        if self.ball.center_y >= self.end_ball_y:
            self.ball_speed_x = 0
            self.ball_speed_y = 0

        # displays the movement of the ball
        self.ball.center_x += self.ball_speed_x
        self.ball.center_y += self.ball_speed_y

    def on_key_press(self, key, modifiers):
        # self.director.next_view()
        if key == arcade.key.ENTER:
            self.menu = False
            self.in_game = True
            self.submit_name = True

        """ press space once, x axis of radar stops moving
            and y axis of radar starts moving
        """
        if key == arcade.key.SPACE and self.shot_state == 0:
            self.radar_speed_x = 0
            self.radar_speed_y = 2
            self.shot_state = 1

        # press space again, y axis of radar stops
        elif key == arcade.key.SPACE and self.shot_state == 1:
            self.radar_speed_y = 0
            self.shot_state = 2

            self.ball_speed_x = (self.end_ball_x - self.ball.center_x) / 30
            self.ball_speed_y = (self.end_ball_y - self.ball.center_y) / 30
        
        # type in name where it says name using keyboard
        if self.menu is True and key != arcade.key.ENTER and key != arcade.key.BACKSPACE and self.submit_name is False:
            self.name += chr(key)
        # using backspace to delete words 
        elif self.menu is True and key == arcade.key.BACKSPACE and self.submit_name is False:
            self.name = self.name[:-1]
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # game stops and you see your score
        view_score = ViewScore()
        self.window.show_view(view_score)

class ViewScore(arcade.View):
    
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
        # Add the time to highscore list
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

        # Displaying the scores from shortest to longest scores
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
        arcade.draw_text("Click to Quit", settings.WIDTH / 2,
                         settings.HEIGHT / 2 - 250,
                         arcade.color.TEAL, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # press the mouse again and window closes
        self.window.close()

def merge_sort(numbers: List[int]) -> List[int]:
    """Sorts the scores of players in a list from greatest to least
        also uses recursion
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
