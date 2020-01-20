import arcade
import random
import settings
import os
import time
from typing import List

GAME_TIME = 15  # in seconds


class Fish(arcade.Sprite):
    """
    Class to keep track of a fish's location and vector and id.
    """
    def __init__(self, filename, sprite_scaling, id: int):
        """Initialize the fish class

        Args:
        filename: The filename of the image
        sprite_scaling: Image Scaling
        id: Fish ID
        """
        super().__init__(filename, sprite_scaling)
        self.center_x = 0
        self.center_y = 0
        self.change_x = 0
        self.change_y = 0
        self._id = id

    def get_id(self) -> int:
        """
        get the id of the fish
        returns: fish id
        """
        return self._id

    def set_id(self, value: int):
        """
        set the id of the fish
        Args:
            value: The fish id
        """
        self._id = value

    def update(self):
        # Move the fish
        self.center_x += self.change_x
        self.center_y += self.change_y
        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1
        if self.right > settings.WIDTH:
            self.change_x *= -1
        if self.bottom < 0:
            self.change_y *= -1
        if self.top > settings.HEIGHT:
            self.change_y *= -1


class JoeView4(arcade.View):
    """
    1) Displays the game
    2) creates 30 random fish at the start of the game
    3) Displays a timer to let the user know how long he has left
    4) Arranges all the caught fish into a list then sorts them
    5) Search for lucky id 10
    6) Displays a win or a loss
    """

    def __init__(self):
        """
        Initialize the view class to initialize the class variables such as fish_list or stopGame
        Call init_game to start the game
        """
        super().__init__()
        # Sprite lists
        self.all_sprites_list = None
        self._fish_list = None
        # Set up the player
        self.player_sprite = None
        self.init_game()
        self._startTime = time.time()
        self._endTime = time.time()
        self._stopGame = False
        self._caught_list = []

    def make_fish(self, id: int) -> Fish:
        """
        Function to make a new, random fish with id and location and vector
        Args:
            id: the fish id
        Returns:
            Fish object
        """
        fish = Fish("Fish.png", 0.05, id)
        # Starting position of the fish.
        fish.center_x = random.randrange(10, settings.WIDTH)
        fish.center_y = random.randrange(10, settings.HEIGHT)
        # Speed and direction of fish
        randX = random.randrange(-4, 5)
        if randX == 0:
            randX = random.randrange(-4, 5)
        randY = random.randrange(-4, 5)
        if randY == 0:
            randY = random.randrange(-4, 5)
        fish.change_x = randX
        fish.change_y = randY
        return fish

    def get_timeleft(self) -> int:
        """
        The time left in seconds before the game is over
        Returns:
            The time left in the game
        """
        self._endTime = time.time()
        return GAME_TIME-int((self._endTime - self._startTime))

    def display_caught_fish(self, fishes: List[Fish]):
        """
        Displays the fish that have been caught already in order of the fish's id
        Args:
            fishes: A list of the fish objects that have been caught
        """
        sorted_fishes = self.sort_by_id(fishes)
        output = ''
        for fish in sorted_fishes:
            output = output + str(fish.get_id()) + ","
        arcade.draw_text("Fish Caught: " + output[:-1], 10, 50, arcade.color.WHITE, font_size=14)

    def sort_by_id(self, fishes: List[Fish]) -> List[Fish]:
        """
        Uses bubble sort to sort the list of fishes by its id
        Args:
            fishes: A list of the fish objects that have been caught
        Returns:
            A new sorted list of the caught fish
        """
        is_sorted = False
        times_through = 0
        while not is_sorted:
            is_sorted = True
            # loop through and compare two elements at a time
            for i in range(len(fishes) - 1 - times_through):
                a = fishes[i].get_id()
                b = fishes[i+1].get_id()
                # if the two elements are out of order, swap them
                if a > b:
                    fishes[i].set_id(b)
                    fishes[i+1].set_id(a)
                    is_sorted = False
            times_through += 1
        # return the sorted list
        return fishes

    def on_show(self):
        arcade.set_background_color(settings.BACKGROUND_COLOUR)

    def on_draw(self):
            arcade.start_render()
            self.all_sprites_list.draw()
            # Put the text on the screen.
            output = "Fish Left: {}".format(len(self._fish_list))
            self.display_caught_fish(self._caught_list)
            found = self.binary_Search(self._caught_list, 10)
            arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
            found_output = f"Lucky Number 10 Caught: {found}"
            if self.get_timeleft() > 0 and self._stopGame is False:
                arcade.draw_text("Time Left: " + str(self.get_timeleft()) + " seconds", 300, 10, arcade.color.WHITE, font_size=16, anchor_x="center")
            else:
                self._stopGame = True
                arcade.draw_text(found_output, 10, 80, arcade.color.WHITE, 14)
                if len(self._fish_list) != 0:
                    arcade.draw_text("Game Over", 400, 300, arcade.color.RED, font_size=40, anchor_x="center")
            if len(self._fish_list) == 0:
                self._stopGame = True
                arcade.draw_text(found_output, 10, 80, arcade.color.WHITE, 14)
                arcade.draw_text("You Win", 400, 300, arcade.color.GREEN, font_size=40, anchor_x="center")

    def on_update(self, delta_time):
        if self._stopGame is False:
            self.all_sprites_list.update()
        else:
            for fish in self.all_sprites_list:
                fish.intensity = 'dim'
                fish.alpha = 64

    def on_key_press(self, key, modifiers):
        self.director.next_view()

    def on_mouse_motion(self, x, y, dx, dy):
        if self._stopGame is False:
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y
            # Generate a list of all sprites that collided with the player.
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self._fish_list)
            # Loop through each colliding sprite, remove it, and add to the caught list
            for fish in hit_list:
                fish.kill()
                self._caught_list.append(fish)
        else:
            pass

    def create_fishs(self, count: int):
        """
        Recursive call to create a number of fish
        Args:
            count: the number of fish to create
        """
        fish = self.make_fish(count)
        self._fish_list.append(fish)
        self.all_sprites_list.append(fish)
        if count == 1:
            return
        else:
            self.create_fishs(count-1)

    def init_game(self):
        """
        Set up the game and initialize the variables.
        """
        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self._fish_list = arcade.SpriteList()
        self.create_fishs(30)
        # Set up the player
        self.player_sprite = arcade.Sprite("Player.png", 1)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.all_sprites_list.append(self.player_sprite)

    def binary_Search(self, data: List[Fish], target: int) -> bool:
        """
        Searches the list of caught fish for the target
        Args:
            data: A list of the fish to search through
            target: The id of the fish to search for
        Returns:
            A True or a False depending on if the target was in the data
        """
        min = 0
        max = len(data) - 1
        found = False
        while min <= max and not found:
            mid = (min + max) // 2  # floor
            if data[mid].get_id() == target:
                found = True
            else:
                if data[mid].get_id() > target:
                    max = mid - 1
                elif data[mid].get_id() < target:
                    min = mid + 1
        return found


if __name__ == "__main__":
    from utils import FakeDirector
    window = arcade.Window(settings.WIDTH, settings.HEIGHT)
    my_view = JoeView4()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
