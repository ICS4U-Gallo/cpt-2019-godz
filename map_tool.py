import csv
import sys
import os

class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

        self.compact_list = [self.x, self.y, self.width, self.height]

class Session_manager:
    def __init__(self):
        
        if len(sys.argv) == 4 and sys.argv[1] == "n": # main.py n w h

            self.session_WIDTH = sys.argv[2]
            self.session_HEIGHT = sys.argv[3]
        
        elif len(sys.argv) == 3 and sys.argv[1] == "l": # main.py l directory
            
            self.complete_dir = f"saves/{sys.argv[2]}"
            self.load_prev_session()

        else:
            raise ValueError("""
            Run script by (cpt_map_tool.py n/l) \"n\" for new map, \"l\" for laoding a previous map
            creating a new map requires file.py n width height
            loading an old map requires file.py l csv_file.csv """)

        self.unsaved_point = []
        self.loaded_points = []

        self.unsaved_changes = False

    def load_prev_session(self):
        
        with open(self.complete_dir) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")

        self.session_WIDTH, self.session_HEIGHT = csv_reader[0][0], csv_reader[0][1]

        for row in range(1, len(csv_reader)):
            
            row = csv_reader[row]

            self.loaded_points.append(Box(row[0], row[1], row[2], row[3]))

    def save_current_sesssion(self):

        with open(self.complete_dir) as csv_file:

            csv_writer = csv.writer(csv_file, delimiter=",")

            while len(self.unsaved_point) > 0:

                csv_writer.writerow(self.unsaved_point[0].compact_list)

                del self.unsaved_point[0]
    
    def add_new_box(self, x, y, w, h):
        
        if w < 0:
        
        if h < 0:

        self.unsaved_point.append(Box(x, y, w, h))
    
    def rm_box(self, x, y):

        for box in self.unsaved_point:
            if 
