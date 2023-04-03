class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_same_point(self, point):
        return self.x == point.x and self.y == point.y

    def is_same_point_move(self, point, move_type):
        from views.view import ViewStatus
        if move_type == ViewStatus.MoveRight or move_type == ViewStatus.MoveLeft:
            return self.x == point.x
        elif move_type == ViewStatus.MoveDown or move_type == ViewStatus.MoveUp:
            return self.y == point.y
        else:
            return self.is_same_point(point)

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def get_point_difference_x(self, point):
        return self.x - point.x

    def get_point_difference_y(self, point):
        return self.y - point.y
