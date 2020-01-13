import csv
import sys
import os
import arcade

class Box(arcade.Sprite):
	def __init__(self, x, y):
		super().__init__(filename="sprites/test_wall_sprite.png", center_x=x, center_y=y)

		self.half_sprite = 10
		self.x = self.center_x - self.half_sprite
		self.y = self.center_y - self.half_sprite
		self.compact_list = [x, y]

class Session_manager:
	def __init__(self):
		
		self.block_size = 20
		self.half_block = self.block_size / 2 

		self.points = []
		if len(sys.argv) == 5 and sys.argv[1] == "n": # main.py n filename.csv w h
			
			self.WIDTH = int(sys.argv[3])
			self.HEIGHT = int(sys.argv[4])
			
			self.complete_dir = f"levels/{sys.argv[2]}"
		
		elif len(sys.argv) == 3 and sys.argv[1] == "l": # main.py l directory
			
			self.complete_dir = f"levels/{sys.argv[2]}"
			self.load_prev_session()

		else:
			raise ValueError("""
			Run script by (cpt_map_tool.py n/l) \"n\" for new map, \"l\" for laoding a previous map
			creating a new map requires file.py n width height
			loading an old map requires file.py l csv_file.csv """)

		self.unsaved_changes = False

	def load_prev_session(self):
		
		with open(self.complete_dir) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=",")

			for row in csv_reader:
				self.WIDTH, self.HEIGHT = int(row[0]), int(row[1])
				break

			count = 0

			for row in csv_reader:
				
				if count != 0:
					self.points.append(Box(float(row[0]), float(row[1])))

				else:
					count += 1

	def save_current_sesssion(self):

			with open(self.complete_dir, "w") as csv_file:
				file_writer = csv.writer(csv_file, delimiter=",")

				file_writer.writerow([self.WIDTH, self.HEIGHT])

				for box in self.points:
					file_writer.writerow(box.compact_list)


	def add_new_box(self, x, y):
		
		true_x = x - (x % self.block_size)
		true_y = y - (y % self.block_size)

		center_x = true_x + self.half_block
		center_y = true_y + self.half_block

		self.points.append(Box(center_x, center_y))
	
	def rm_box(self, x, y):
		
		count = 0
		for box in self.points:
			if  x > box.x and x < (box.x + self.block_size):
				if y > box.y and y < (box.y + self.block_size):
					cd Code
					del self.points[count]

			count += 1

def draw_grid(width, height, spacing):

	for r in range(0, width, spacing):
		arcade.draw_line(r, 0, r, height, arcade.color.BLACK_LEATHER_JACKET, 2)

	for c in range(0, height, spacing):
		arcade.draw_line(0, c, width, c, arcade.color.BLACK_LEATHER_JACKET, 2) 

session = Session_manager()

print(session.WIDTH, session.HEIGHT)

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
	
	draw_grid(session.WIDTH, session.HEIGHT, session.block_size)

	for box in session.points:
		box.draw()

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

if __name__ == '__main__':
	setup()
