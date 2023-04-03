from abc import ABC, abstractmethod
from enum import Enum
import pygame
from views.point import Point
from queue import Queue


class ViewStatus(Enum):
    MoveUp = 1
    MoveDown = 2
    MoveLeft = 3
    MoveRight = 4
    PutInToTower = 6
    Ideal = 5


class MoveView:

    def __init__(self, view_status: ViewStatus, point: Point):
        self.view_status = view_status
        self.point = point


class View(ABC):

    def __init__(self, point: Point, width, height, name,color=(255, 255, 255)):
        self.point = point
        self.width = width
        self.height = height
        self.view_status = ViewStatus.Ideal
        self.destination = None
        self.move_speed = 1
        self.name = name
        self.move_queue = Queue()
        self.can_move = False
        self.color = color

    def __str__(self) -> str:
        return f"View {self.name} Location {self.get_center_point()}"

    def get_top_border_point(self):
        return Point(self.get_center_point().x, self.get_center_point().y - self.height / 2)

    def get_center_point(self):
        return Point(self.point.x + self.width / 2, self.point.y + self.height / 2)

    def get_bottom_border_point(self):
        return Point(self.get_center_point().x, self.get_center_point().y + self.height / 2)

    @abstractmethod
    def draw(self, screen, color=(255, 255, 255)):
        pass

    def move_vertical(self, speed):
        self.point.y += speed

    def move_Horizontal(self, speed):
        self.point.x += speed

    def move_to_up(self, point):
        self.view_status = ViewStatus.MoveUp

    def move_to(self, point):
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

        self.move_queue.put(ViewStatus.Ideal)
        if not self.move_queue.empty():
            self.view_status = self.move_queue.get()
        else:
            self.view_status = ViewStatus.Ideal
