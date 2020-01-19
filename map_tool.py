import csv
import sys
import os
import arcade

class Box(arcade.Sprite):
	sprite_dimension = 20
	def __init__(self, x, y):
		super().__init__(filename="sprites/test_wall_sprite.png", center_x=x, center_y=y)

		self.left_x = self.center_x - (self.sprite_dimension / 2)
		self.bottom_y = self.center_y - (self.sprite_dimension / 2)

		self.right_x = self.center_x + (self.sprite_dimension / 2)
		self.top_y = self.center_y + (self.sprite_dimension / 2)
		
		self.compact_list = [self.center_x, self.center_y]

class Session_manager:
	def __init__(self):
		
		self.block_size = 20
		self.half_block = self.block_size / 2 

		self.blocks = arcade.SpriteList()
		
		self.goal = None
		if len(sys.argv) == 5 and sys.argv[1] == "n": # main.py n filename.csv w h
			
			self.WIDTH = int(sys.argv[3])
			self.HEIGHT = int(sys.argv[4])
			
			self.complete_dir = f"levels/{sys.argv[2]}"
		
		elif len(sys.argv) == 3 and sys.argv[1] == "l": # main.py l directory
			
			self.complete_dir = f"levels/{sys.argv[2]}"
			self.load_prev_session()

		else:
			raise ValueError("""Needs map_tool.py l filename.csv --or-- map_tool.py n filename.csv file_width file_height """)

		self.unsaved_changes = False

	def load_prev_session(self):
		
		with open(self.complete_dir) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=",")
			
			count = 0

			for row in csv_reader:

				if count == 0:
					self.WIDTH, self.HEIGHT = int(row[0]), int(row[1])

				elif count == 1:	
					self.goal = arcade.Sprite(filename='sprites/test_goal_sprite.png',
								center_x=int(row[0]),
								center_y=int(row[1]))

				elif count != 0:
					self.blocks.append(Box(float(row[0]), float(row[1])))

				count += 1

	def save_current_sesssion(self):

			try:
				os.remove(self.complete_dir)
			
			except:
				pass
			
			with open(self.complete_dir, "w") as csv_file:
				file_writer = csv.writer(csv_file, delimiter=",")

				file_writer.writerow([self.WIDTH, self.HEIGHT])
				file_writer.writerow([self.goal.center_x, self.goal.center_y])

				for box in self.blocks:
					file_writer.writerow(box.compact_list)

	def add_new_box(self, x, y):
		
		left_x = x - (x % self.block_size)
		bottom_y = y - (y % self.block_size)

		x = left_x + self.half_block
		y = bottom_y + self.half_block

		b = Box(x=x, y=y)

		b.left_x = left_x 
		b.right_x =  left_x + self.block_size
		b.bottom_y = bottom_y
		b.top_y = bottom_y + self.block_size

		self.blocks.append(b)
	
	def rm_box(self, x, y):
		
		found = True

		while found:
			
			for box in self.blocks:
				if box.left_x < x and box.right_x > x:
					if box.bottom_y < y and box.top_y > y:
						self.blocks.remove(box)
						break
				
			else:
				found = False

	def add_goal(self, x, y):
		self.goal = arcade.Sprite(filename='sprites/test_goal_sprite.png',
								center_x=x,
								center_y=y)

def draw_grid(width, height, spacing):

	for r in range(0, width, spacing):
		arcade.draw_line(r, 0, r, height, arcade.color.BLACK_LEATHER_JACKET, 2)

	for c in range(0, height, spacing):
		arcade.draw_line(0, c, width, c, arcade.color.BLACK_LEATHER_JACKET, 2) 

session = Session_manager()
window = arcade.open_window(session.WIDTH, session.HEIGHT, "Map Builder")

def setup():
	arcade.set_background_color(arcade.color.WHITE)
	arcade.schedule(update, 1/60)
	arcade.run()

def update(delta_time):
	pass

@window.event
def on_draw():
	arcade.start_render()
	draw_grid(session.WIDTH, session.HEIGHT, 20)
	session.blocks.draw()
	if session.goal != None:
		session.goal.draw()

@window.event
def on_key_press(key, modifiers):
	
	if key == arcade.key.S:
		session.save_current_sesssion()

@window.event
def on_key_release(key, modifiers):
	pass

@window.event
def on_mouse_press(x, y, button, modifiers):
	
	if button == arcade.MOUSE_BUTTON_LEFT:
		session.add_new_box(x,y)
	
	elif button == arcade.MOUSE_BUTTON_RIGHT:
		session.rm_box(x,y)

	elif button == arcade.MOUSE_BUTTON_MIDDLE:
		session.add_goal(x, y)

if __name__ == '__main__':
	setup()
