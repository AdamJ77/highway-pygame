import pygame as pg
from enum import Enum, auto
import math
# from class_player import Player

from config import (
    SPEED_PLAYER,
    MAX_SPEED_PLAYER,
    FRICTION_DECEL,
    SCROLL_SPEED,
    TRUCK_IMAGE,
    TRUCK_HEIGHT,
    TRUCK_WIDTH,
    POLICE_CAR_IMAGE,
    POLICE_CAR_HEIGHT,
    POLICE_CAR_WIDTH,
    POLICE_CAR_IMAGE_LIGHTS_B,
    POLICE_CAR_IMAGE_LIGHTS_R,
    FREQUENCY_OF_POLICE_LIGHTS,
    ANGLE_ROTATE,
    MAX_ANGLE_TRAFFIC_CHANGE_LINE,
    TIME_OF_TURN
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
        self.line = None        # 1 - upper line, 2 - middle line, 3 - lower line
        self.time_of_turn = 1
        self.still_change = True

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

    def free_decelaration(self) -> None:
        if self.x + self.width < 0:
            self.isOut = True
        self.x -= self.decelaration * 6
        self.move_sideways()

    @staticmethod
    def get_tan_abs(angle) -> float:
        """Get tangens value of given angle"""
        return math.tan(math.radians(abs(angle)))

    def move_sideways(self) -> None:
        """Move sideways if there is rotation != 0"""
        tan_angle = self.get_tan_abs(self.rotation)
        if self.rotation > 0:
            self.y -= (self.speed + SCROLL_SPEED) * tan_angle
        if self.rotation < 0:
            self.y += (self.speed + SCROLL_SPEED) * tan_angle

    def rotate(self, negative: int):
        """
        Rotate image depending on negative value:
        negative=0:     rotate left
        negative=1:     rotate right
        """
        rotated_image = pg.transform.rotate(self.model, self.rotation)
        new_rect = rotated_image.get_rect(center=(self.model.get_rect(topleft=(self.x, self.y)).center))
        self.model = rotated_image
        self.rotation += (-1) ** negative
        self.x, self.y = new_rect.topleft

    def rotate_left(self) -> None:
        """Rotate left image left"""
        # if self.rotation < MAX_ANGLE_TRAFFIC_CHANGE_LINE:
        self.rotate(negative=0)

    def rotate_right(self) -> None:
        """Rotate right image right"""
        # if self.rotation > -MAX_ANGLE_TRAFFIC_CHANGE_LINE:
        self.rotate(negative=1)

    def change_line(self):
        # if self.still_change:
            if self.time_of_turn < 10:
                # if self.rotation > -20:
                self.rotate_right()
            self.time_of_turn += 1
            # if self.time_of_turn >= 200:
            #     if self.rotation != 0:
            #         self.rotate_left()
            #     else:
            #         self.time_of_turn = 1
            #         self.still_change = False
        # elif self.time_of_turn < 2 * TIME_OF_TURN and self.rotation != 0:
        #     self.rotate_left()
        #     self.move_sideways()
        #     self.time_of_turn += 1
        # else:
        #     self.time_of_turn = 1
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

    def __init__(self, spawn_loc, line_value) -> None:
        self.spawn_location = spawn_loc
        self.car_occupying = None
        self.line_value = line_value

    @classmethod
    def location(cls, location, line_val):
        return cls(location, line_val)



class Police(Car):
    def __init__(self) -> None:
        super().__init__()
        self.x = 1500
        self.model = POLICE_CAR_IMAGE
        self.width = POLICE_CAR_WIDTH
        self.height = POLICE_CAR_HEIGHT
        self.changing_lights = 1

    def follow_car(self, car: Car):
        pass

    def turn_police_lights_on(self):
        if self.changing_lights % FREQUENCY_OF_POLICE_LIGHTS != 0:
            self.changing_lights += 1
            return
        self.changing_lights = 1
        self.model = POLICE_CAR_IMAGE_LIGHTS_B if self.model == POLICE_CAR_IMAGE_LIGHTS_R else POLICE_CAR_IMAGE_LIGHTS_R

    def turn_police_ligths_off(self):
        self.model = POLICE_CAR_IMAGE

    def free_decelaration(self):
        if self.x - self.decelaration > 0:
            self.x -= self.decelaration * 6
        self.move_sideways()


    def automatic_following(other: Car):
        pass