from queue import Queue
from time import sleep

import pygame

from objects.brick import Brick
from objects.tower import Tower
from views.point import Point
from views.rectangle import Rectangle


class MoveObject:

    def __init__(self, brick, from_tower, to_tower):
        self.brick = brick
        self.from_tower = from_tower
        self.to_tower = to_tower


class WindowVisualizer:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.running = False

        self.padding_width = 100
        self.padding_height = 100

        ############### Bottom Box Width Size
        self.bottom_box_height = 10
        self.bottom_box_width = (self.width - self.padding_width / 2)
        #######################################
        self.color = (255, 0, 0)

        self.objects = []
        self.bricks = []
        self.towers = []
        self.selected_brick = None
        self.moves_queue = Queue()
        self.run_algo = False
        self.number_of_bricks = 3


    def set_bricks_number(self,n):
        self.number_of_bricks = n


    def add_object(self, view):
        self.objects.append(view)

    def start(self):

        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption('Tower Of Hanoi [Mario]')
        self.running = True
        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((255, 255, 255))

            if not self.run_algo:
                bottom_bar = Rectangle(Point(self.padding_width / 2,
                                             (self.height - (self.padding_height / 2)) - self.bottom_box_height),
                                       self.bottom_box_width - self.padding_width / 2, self.bottom_box_height,
                                       "Bottom Bar", color=(98, 102, 99))
                self.add_object(bottom_bar)

                self.draw_towers_bricks()
                self.solve(self.number_of_bricks, self.towers[0], self.towers[2], self.towers[1])
                self.run_algo = not self.run_algo

            if not self.moves_queue.empty():
                if self.selected_brick is None:
                    move_object = self.moves_queue.get()
                    self.selected_brick = move_object.brick
                    from_tower = move_object.from_tower
                    to_tower = move_object.to_tower

                    self.move_bricks_to_tower(self.selected_brick, from_tower, to_tower)
                    self.selected_brick.can_move = True

            if self.selected_brick is not None and self.selected_brick.can_move is False:
                self.selected_brick = None

            self.draw_all_objects()
            pygame.display.flip()
            sleep(1 / 100000)
        pygame.quit()

    def draw_towers_bricks(self):
        total_bars = 3

        brick_height = 10
        brick_width = 10
        bar_width = 10
        bar_height = 100
        # calculate Bar Height For Bricks Number
        bar_height = max(bar_height, (brick_height * (self.number_of_bricks + 2)))

        total_available_width = (self.width - self.padding_width)

        total_bricks_in_bar = (bar_height / brick_height) - 3
        total_bricks_in_bar = min(total_bricks_in_bar, self.number_of_bricks)
        max_brick_width = bar_width + (brick_width * total_bricks_in_bar)

        vertical_bar_spacing = (total_available_width - (total_bars * max_brick_width)) / total_bars
        vertical_bar_padding = total_available_width - (vertical_bar_spacing * total_bars)
        vertical_bar_padding = vertical_bar_padding / total_bars
        for i in range(total_bars):
            vertical_bars = Tower(
                Point((self.padding_width / 2) + (vertical_bar_padding / 2 + (vertical_bar_padding * i)) + (
                        vertical_bar_spacing / 2 + (vertical_bar_spacing * i)),
                      (self.height - (self.padding_height / 2)) - self.bottom_box_height - bar_height),
                bar_width, bar_height
                , f"Tower No {i}")
            vertical_bars.color = (237, 180, 235)
            self.add_object(vertical_bars)
            self.towers.append(vertical_bars)

        number_of_bricks = self.number_of_bricks - 1
        ist_tower: Tower = self.towers[0]
        for i in range(number_of_bricks + 1):
            bWidth = (brick_width + brick_width * (total_bricks_in_bar - i) + ist_tower.width)
            brick = Brick(Point((ist_tower.get_bottom_border_point().x - bWidth / 2),
                                (ist_tower.get_bottom_border_point().y - 5 - (i * brick_height))),
                          bWidth, brick_height, self.towers[0], f"Brick No {i + 1}")

            brick.color = (168, 50 + (i * 5), 30 + (i * 5))
            self.add_object(brick)
            self.bricks.append(brick)

    def draw_all_objects(self):
        for i in self.objects:
            i.draw(self.screen)

    def move_bricks_to_tower(self, brick, from_tower, tower):
        brick.move_to(from_tower, tower)

    def solve(self, n, source, destination, auxiliary):

        if n == 1:
            self.moves_queue.put(
                MoveObject(self.bricks[self.number_of_bricks - n], source, destination))
            return
        self.solve(n - 1, source, auxiliary, destination)
        self.moves_queue.put(
            MoveObject(self.bricks[self.number_of_bricks - n], source, destination))
        self.solve(n - 1, auxiliary, destination, source)
