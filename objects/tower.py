from views.point import Point
from views.rectangle import Rectangle


class Tower(Rectangle):
    def __init__(self, point: Point, width, height, name):
        super().__init__(point, width, height, name)
        self.bricks_number = 0


    def get_bottom_border_point(self):
        return Point(self.get_center_point().x, self.get_center_point().y + self.height / 2 -5)

    def add_bricks(self):
        self.bricks_number += 1

    def remove_bricks(self):
        self.bricks_number -= 1

        if self.bricks_number<=0:
            self.bricks_number=0


