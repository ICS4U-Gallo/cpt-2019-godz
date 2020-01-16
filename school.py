import arcade
import random
import settings
import os
import time
from typing import List

GAME_TIME = 15 # in seconds
startTime = time.time()
endTime = time.time()


class Fish(arcade.Sprite):
    """
    Class to keep track of a fish's location and vector and id.
    """
    def __init__(self, filename, sprite_scaling, id):
        super().__init__(filename, sprite_scaling)
        self.center_x = 0
        self.center_y = 0
        self.change_x = 0
        self.change_y = 0
        self._id = id
  
    def get_id(self) -> int:
        return self._id
  
    def set_id(self, value: int):
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
        if self.top >settings.HEIGHT:
            self.change_y *= -1
      

class JoeView3(arcade.View):
    """
    Displays the game
    """
    def __init__(self):
        super().__init__()
        # Sprite lists
        self.all_sprites_list = None
        self._fish_list = None
        # Set up the player
        self.player_sprite = None
        self.init_game()
        self._startTime = time.time()
        self._stopGame = False
        self._caught_list = []

    def make_fish(self, id: int):
        """
    Function to make a new, random fish with id and location and vector
    """
    fish = Fish("Fish.png", 0.05, id)
        
    # Starting position of the fish.
    fish.center_x  = random.randrange(10,settings.WIDTH)
    fish.center_y  = random.randrange(10,settings.HEIGHT)
    # Speed and direction of fish
    randX=random.randrange(-4, 5)
    if randX==0:
        randX=random.randrange(-4, 5)
    randY=random.randrange(-4, 5)
    if randY==0:
        randY=random.randrange(-4, 5)
        fish.change_x = randX
        fish.change_y = randY
        return fish
    
    def get_timeleft(self):
        """
        The time left in seconds before the game is over
        """
        endTime = time.time()
        return GAME_TIME-int((endTime - self._startTime))
    
    def display_caught_fish(self, fishes: List[Fish]):
        """
        Displays the fish that have been caught already in order of the fish's id
        """
        sorted_fishes = self.sort_by_id(fishes)
        output = ''
        for fish in sorted_fishes:
            output = output + str(fish.get_id()) + ","
        arcade.draw_text("Fish Caught: " + output[:-1], 10, 50, arcade.color.WHITE, font_size= 14)
        
    def sort_by_id(self, fishes: List[Fish])-> List[Fish]:
        """
        Uses bubble sort to sort the list of fishes by its id
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
            arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
            if self.get_timeleft() > 0 and self._stopGame == False:
                arcade.draw_text("Time Left: " + str(self.get_timeleft()) + " seconds", 300, 10, arcade.color.WHITE, font_size=16, anchor_x="center")
            else:
                self._stopGame = True
            if len(self._fish_list) != 0:
                arcade.draw_text("Game Over", 400, 300, arcade.color.RED, font_size = 40, anchor_x="center")
            if len(self._fish_list) == 0:
                self._stopGame = True
                arcade.draw_text("You Win", 400, 300, arcade.color.GREEN, font_size = 40, anchor_x="center")
            
    def on_update(self, delta_time):
        if self._stopGame == False:
            self.all_sprites_list.update()
        else:
            for fish in self.all_sprites_list:
                fish.intensity='dim'
                fish.alpha=64
            
        
    def on_key_press(self, key, modifiers):
        self.director.next_view()
        
    def on_mouse_press(self, x, y, button, modifiers):
        pass
    
    def on_mouse_motion(self, x, y, dx, dy):
        if self._stopGame == False:
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y
        
            # Generate a list of all sprites that collided with the player.
            hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self._fish_list)
            # Loop through each colliding sprite, remove it, and add to the score.
            for fish in hit_list:
                #self.score += 1
                fish.kill()
                self._caught_list.append(fish)
        else:
            pass
    
    #Recursive call to create 30 fish at random position
    def create_fishs(self, count: int):
        fish = self.make_fish(count)
        self._fish_list.append(fish)
        self.all_sprites_list.append(fish)
        if count == 1:
            return
        else:
            self.create_fishs(count-1)
            
    def init_game(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self._fish_list = arcade.SpriteList()
        self.create_fishs(30)
        # Set up the player
        #self.score = 0
        self.player_sprite = arcade.Sprite("Player.png", 1)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.all_sprites_list.append(self.player_sprite)
        
        
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
    my_view = JoeView3()
    my_view.director = FakeDirector(close_on_next_view=True)
    window.show_view(my_view)
    arcade.run()
