from views.point import Point
from views.rectangle import Rectangle
from views.view import ViewStatus


class Brick(Rectangle):
    def __init__(self, point: Point, width, height, tower, name):
        super().__init__(point, width, height, name)
        self.current_tower = tower
        self.last_tower = tower
        tower.add_bricks()

    def move_to(self,from_tower, to_tower):
        from_tower.remove_bricks()
        point = to_tower.get_top_border_point()
        point.y -= 20
        self.last_tower=self.current_tower
        self.current_tower = to_tower
        self.destination = point
        # 1 To Move Up
        if self.get_center_point().get_point_difference_y(point) > 0:
            self.move_queue.put(ViewStatus.MoveUp)

        if self.get_center_point().get_point_difference_x(point) < 0:
            self.move_queue.put(ViewStatus.MoveRight)

        if self.get_center_point().get_point_difference_y(point) < 0:
            self.move_queue.put(ViewStatus.MoveDown)

        if self.get_center_point().get_point_difference_x(point) > 0:
            self.move_queue.put(ViewStatus.MoveLeft)

        self.move_queue.put(ViewStatus.PutInToTower)
        if not self.move_queue.empty():
            self.view_status = self.move_queue.get()
        else:
            self.view_status = ViewStatus.Ideal

    def put_view_in_tower(self):
        self.current_tower.add_bricks()
        destination = Point(self.current_tower.get_center_point().x,
                            self.current_tower.get_bottom_border_point().y - ((self.current_tower.bricks_number - 1)
                                                                              * self.height
                                                                              )
                            )
        super().move_to(destination)
