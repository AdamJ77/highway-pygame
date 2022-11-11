import pygame as pg
from enum import Enum, auto

from config import (
    SPEED_PLAYER,
    MAX_SPEED_PLAYER,
    FRICTION_DECEL,
    SCROLL_SPEED,
    TRUCK_IMAGE,
    TRUCK_HEIGHT,
    TRUCK_WIDTH
)


class Game:
    test_rect = False

class Car:

    speed = SPEED_PLAYER
    max_speed = MAX_SPEED_PLAYER

    def __init__(self) -> None:
        self._x: float = 600
        self._y : float= 300
        self.rotation = 0
        self.decelaration: int = FRICTION_DECEL
        self.width: int = 0
        self.height: int = 0
        self.isOut = False
        self.old_rect = None
        self.act_rect = self.get_rect()


    def get_rect(self):
        """Create and return Rect object based on self attributes"""
        return pg.Rect(self.x, self.y, self.width, self.height)

    def constant_speed(self) -> None:
        """Press and hold space to set constant speed"""
        self.speed = SCROLL_SPEED

    def get_center_point(self):
        """Return list of center point coordinates of car"""
        return [self.x + self.width // 2, self.y + self.height // 2]


    @classmethod
    def slomo_test(cls):
        cls.max_speed = MAX_SPEED_PLAYER // 2

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y

    def no_acceleration(self) -> None:
        if self.x + self.width < 0:
            self.isOut = True
        self.x -= self.decelaration * 6

    # or classmethod Truck


class ColorCar(Enum):
    CAR_RED = 1
    CAR_GREEN = 2
    CAR_PURPLE = 3
    MUSCLE_CAR_YELLOW = 4
    SEDAN_BROWN = 5


class Truck(Car):
    def __init__(self) -> None:
        super().__init__()
        self.model = TRUCK_IMAGE
        self.width = TRUCK_WIDTH
        self.height = TRUCK_HEIGHT


class Location:

    def __init__(self, spawn_loc) -> None:
        self.spawn_location = spawn_loc
        self.car_occupying = None

    @classmethod
    def location(cls, location):
        return cls(location)