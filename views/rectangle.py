from abc import ABC

import pygame

from views.point import Point
from views.view import View, ViewStatus


class Rectangle(View, ABC):

    def __init__(self, point: Point, width, height, name, color=(255, 255, 255)):
        super().__init__(point, width, height, name, color)

    def draw(self, screen, color=(255, 255, 255)):
        if self.can_move:
            if self.view_status is not ViewStatus.Ideal:
                is_reach_position = self.get_center_point().is_same_point_move(self.destination, self.view_status)

                if is_reach_position and self.view_status is not ViewStatus.PutInToTower:
                    if not self.move_queue.empty():
                        self.view_status = self.move_queue.get()



                elif self.view_status == ViewStatus.PutInToTower:
                    self.put_view_in_tower()
                elif self.view_status == ViewStatus.MoveUp:
                    self.move_vertical(self.move_speed * -1)

                elif self.view_status == ViewStatus.MoveDown:
                    self.move_vertical(self.move_speed * 1)

                elif self.view_status == ViewStatus.MoveRight:
                    self.move_Horizontal(self.move_speed * 1)

                elif self.view_status == ViewStatus.MoveLeft:
                    self.move_Horizontal(self.move_speed * -1)
            else:
                self.can_move = False
        pygame.draw.rect(screen, self.color,
                         pygame.Rect(self.point.x,
                                     self.point.y,
                                     self.width, self.height))

    def put_view_in_tower(self):
        pass
