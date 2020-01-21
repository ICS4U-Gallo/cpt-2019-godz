import arcade
import settings
import csv
import time
import os

PLAYER_SPEED = 15.0
PLAYER_JUMP = 20.0
PLAYER_FRICTION = 0.8
PLAYER_GRAVITY = 1.0


class Leaderboard_manager:
    def __init__(self):
        self.leaderboard_filename = "first_chapter.csv"
        self.leaderboard_dir = "leaderboards"

        self.complete_path = f"{self.leaderboard_dir}/{self.leaderboard_filename}"

        self.leaderboards = []

        self.show = False

        self.display_upto = 5

        with open(self.complete_path) as csv_file:
            board = csv.reader(csv_file, delimiter=",")
            for row in board:
                self.leaderboards.append([float(row[0]), str(row[1])])

        self.chart_location = Point(0, 0)

        self.chart_spacing = 40

    def recursive_merge_sort(self, scores: list) -> list:

        new_list = []

        n = len(scores)

        if n == 1:
            return scores

        middle = n//2

        left_side = self.recursive_merge_sort(scores[:middle])
        right_side = self.recursive_merge_sort(scores[middle:])

        left_count = 0
        right_count = 0

        while left_count != len(left_side) and right_count != len(right_side):

            if left_side[left_count][0] <= right_side[right_count][0]:
                new_list.append(left_side[left_count])
                left_count += 1

            elif right_side[right_count][0] <= left_side[left_count][0]:
                new_list.append(left_side[left_count])
                right_count += 1

        if right_count != len(right_side):

            for num in right_side[right_count:]:

                new_list.append(num)

        else:

            for num in left_side[left_count:]:

                new_list.append(num)

        return new_list

    def linear_search(self, target_name: str):

        for score in self.leaderboards:

            if score[1] == target_name:
                return score

        else:
            return None  # The error case for score not found

    def get_chart_location(self, x: int, x1: int, y: int):
        self.chart_location.x = (x + x1) / 2
        self.chart_location.y = y + (settings.HEIGHT / 2)

    def draw(self):

        count = 0

        for score in self.leaderboards:

            temp_str = f"\"{score[1]}\" completed in: {score[0]}"
            arcade.draw_text(temp_str,
                            self.chart_location.x,
                            self.chart_location.y - (count * self.chart_spacing),
                            arcade.color.WHEAT,
                            font_size=25,
                            anchor_x="center",
                            anchor_y="bottom")

            if count is self.display_upto:
                break

            count += 1

    def save(self):

        self.leaderboards = self.recursive_merge_sort(self.leaderboards)

        if os.path.exists(self.complete_path):
            os.remove(self.complete_path)

        with open(self.complete_path, "w") as csv_file:
            file_writer = csv.writer(csv_file, delimiter=",")

            for row in self.leaderboards:
                file_writer.writerow(row)

    def add_player(self, time: float, name: str):
        self.leaderboards.append([time, name])


class Point:
    """ Convience class representing an x,y cordinate pair"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Timer:

    def __init__(self):

        self.start = round(time.time(), 2)

        self.timer_location = [0, 0]

    def get_time_elapsed(self) -> float:
        return round(time.time() - self.start, 2)

    def get_timer_location(self, x, y):
        self.timer_location[0] = x + 5
        self.timer_location[1] = y + 5


class Platform_manager:
    """ Class responsible for loading prebuilt levels"""

    platform_list = arcade.SpriteList()

    def __init__(self, filename: str):

        # csv_dir is the file directory where the prebuilt levels are located
        self.csv_dir = "levels"

        # csv_filename is the name of the desired level
        self.csv_filename = filename

        # Stitching together the directory and file name for a useable pathway
        self.csv_path = f"{self.csv_dir}/{self.csv_filename}"

        # Same proccess as the csv file loading
        self.sprite_filename = "test_wall_sprite.png"
        self.sprite_dir = "sprites"
        self.sprite_path = f"{self.sprite_dir}/{self.sprite_filename}"

        self.goal_filename = "test_goal_sprite.png"
        self.goal_sprite_path = f"{self.sprite_dir}/{self.goal_filename}"

        self.sprite_scaling = 1

        with open(self.csv_path) as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=",")

            # count is used to ignore the first and second row, being the level dimensions, and goal location repsectively
            count = 0

            for row in csv_reader:

                if count > 1:
                    # Create an arcade sprite object for everyplatform in the csv file
                    s = arcade.Sprite(center_x=float(row[0]),
                                center_y=float(row[1]),
                                filename=self.sprite_path,
                                scale=self.sprite_scaling)

                    # Add it to the platform manager's list of all platforms
                    self.platform_list.append(s)

                elif count == 1:
                    self.goal = arcade.Sprite(center_x=float(row[0]),
                                        center_y=float(row[1]),
                                        filename=self.goal_sprite_path,
                                        scale=self.sprite_scaling)

                count += 1


class Player(arcade.Sprite):
    """Class responsible for managing all Player related values"""

    sprite_height = 20
    sprite_width = 20

    def __init__(self, starting_x: int, starting_y: int):

        self.sprite_scaling = 1

        # All caps to prevent the overriding of inhereted attributes
        self.SPEED = 15.0
        self.JUMP = 15.0
        self.GRAVITY = 1.0

        # Stitching together a file pathway for the player's image
        self.character_path = "sprites"
        self.character_sprite = "test_char_sprite.png"
        self.character_sprite_path = f"{self.character_path}/{self.character_sprite}"

        # Initializing the arcade.Sprite parent class
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

        # Packaging the return values for easy of use
        return x, x1, y, y1


class Chapter1View(arcade.View):
    def __init__(self):

        super().__init__()

        # Initializing the player's object
        self.player = Player(starting_x=300, starting_y=50)

        # These key value pairs are used for player movenment
        self.key_pressed = {
            arcade.key.A: False,
            arcade.key.D: False,
            arcade.key.SPACE: False,
            arcade.key.TAB: False}

        # Initializing the level with the desired map (in this case level1.csv)
        self.platform_manager = Platform_manager("level1.csv")

        # Initializing a physics engine instance.
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.platform_manager.platform_list)
        self.physics_engine.gravity_constant = self.player.GRAVITY

        self.timer = Timer()

        self.leaderboard = Leaderboard_manager()

        self.completed = False

    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE_SAPPHIRE)

    def on_draw(self):
        arcade.start_render()

        self.platform_manager.platform_list.draw()
        self.platform_manager.goal.draw()
        self.player.draw()

        temp_str = f"Time: {self.timer.get_time_elapsed()}"
        arcade.draw_text(temp_str, self.timer.timer_location[0], self.timer.timer_location[1], arcade.color.AMBER, font_size=16)

        if self.leaderboard.show is True:
            self.leaderboard.draw()

    def on_key_press(self, key, modifiers):
        self.key_pressed[key] = True

    def on_key_release(self, key, modifiers):
        self.key_pressed[key] = False

    def on_update(self, delta_time: float):

        self.physics_engine.update()

        # Applying player movenment
        if self.key_pressed[arcade.key.A]:
            self.player._set_change_x(-PLAYER_SPEED)

        elif self.key_pressed[arcade.key.D]:
            self.player._set_change_x(PLAYER_SPEED)

        if self.key_pressed[arcade.key.SPACE] and self.physics_engine.can_jump(self.player.sprite_height):
            self.physics_engine.jump(PLAYER_JUMP)

        # Map completion check
        if self.player.collides_with_sprite(self.platform_manager.goal):
            self.completed = True

        if self.key_pressed[arcade.key.TAB]:
            self.leaderboard.show = True

        else:
            self.leaderboard.show = False

        if self.completed is True:
            self.leaderboard.add_player(time=self.timer.get_time_elapsed(), name="Guest")
            self.leaderboard.save()
            self.director.next_view()

        # Applying friciton to the player's movement
        self.player._set_change_x(self.player._get_change_x() * PLAYER_FRICTION)

        # Adjusting the viewport (camera)
        x, x1, y, y1 = self.player.screen_location()
        arcade.set_viewport(x, x1, y, y1)

        self.leaderboard.get_chart_location(x, x1, y)
        self.timer.get_timer_location(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

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
