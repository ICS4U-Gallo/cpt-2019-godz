import arcade

import settings

from menu import MenuView
from chapter_1 import Chapter1View
from chapter_2 import Chapter2View
from chapter_3 import Chapter3View
from chapter_4 import JoeView4

class Director(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.view_index = 0
        self.views = [
            MenuView,
            Chapter1View,
            Chapter2View,
            Chapter3View,
            JoeView4
        ]
        self.next_view()

    def next_view(self):
        next_view = self.views[self.view_index]()
        next_view.director = self
        self.show_view(next_view)
        self.view_index = (self.view_index + 1) % len(self.views)


def main():
    window = Director(settings.WIDTH, settings.HEIGHT, "CPT Structure")
    arcade.run()


if __name__ == "__main__":
    main()
