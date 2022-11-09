import pygame as pg
import math
from typing import Union
from classes_other import (
    Car
)


from config import (
    WIDTH,
    HEIGHT,
    PLAYER_IMAGE,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    SPEED_PLAYER,
    BRAKE_LIGHTS,
    ACELERATION,
    SCROLL_SPEED,
    BRAKE_DECEL,
    ANGLE_ROTATE,
    MAX_ANGLE,
    DRIVING_AREA_SIZE
)

class Player(Car):
    def __init__(self) -> None:
        super().__init__()
        self._x = WIDTH // 5
        self._y = HEIGHT // 2
        self.model = PLAYER_IMAGE
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.brakes_light = False
        self.brake_model = BRAKE_LIGHTS


    def get_rect(self):
        """Create and return Rect object based on self attributes"""
        x_cord = self.x
        y_cord = self.y
        if self.rotation < 0:
            y_cord = self.y + self.width // 2 * self.get_tan_abs(self.rotation) + 10
        return pg.Rect(x_cord, y_cord, self.width, self.height)


    @staticmethod
    def get_tan_abs(angle) -> float:
        """Get tangens value of given angle"""
        return math.tan(math.radians(abs(angle)))

    @staticmethod
    def get_tan(angle) -> float:
        """Get tangens value of given angle"""
        return math.tan(math.radians(angle))

    def move_forward(self) -> None:
        """Move car forward depending on the car's rotation"""
        if self.x + self.speed < WIDTH - PLAYER_WIDTH:
            self.x += self.speed
            if self.speed < self.max_speed:
                self.speed += ACELERATION
            self.move_sideways()

    def move_sideways(self) -> None:
        """Move sideways if there is rotation != 0"""
        tan_angle = self.get_tan_abs(self.rotation)
        if self.rotation > 0 and self.y - self.speed * tan_angle > DRIVING_AREA_SIZE[0]:
            self.y -= (self.speed + SCROLL_SPEED) * tan_angle
        if self.rotation < 0 and self.y + self.speed * tan_angle < DRIVING_AREA_SIZE[1] - PLAYER_WIDTH * self.get_tan_abs(self.rotation) //2:
            self.y += (self.speed + SCROLL_SPEED) * tan_angle

    def no_acceleration(self) -> None:
        """Speed down if no acceleration"""
        if self.speed > SPEED_PLAYER and (new_speed := self.x + self.speed) < WIDTH:
            if self.speed - self.decelaration >= SPEED_PLAYER:
                self.speed -= self.decelaration
                self.x = new_speed
        else:
            if self.x - self.decelaration > 0:
                self.x -= self.decelaration * 6
        self.move_sideways()


    #TODO fix moving sideways while self.speed == 0
    def brake(self) -> None:
        """Massive speed down"""
        if self.speed > SPEED_PLAYER and self.x + self.speed < WIDTH:
            self.move_sideways()
            if (new_speed:=self.speed - self.decelaration * 3) >= SPEED_PLAYER:
                self.speed = new_speed
                self.x += self.speed
        elif not self.speed :
            self.move_sideways()
            if self.x - BRAKE_DECEL > 0:
                self.x -= BRAKE_DECEL
        self.brakes_light = True
        # drifting mode to be added

    def rotate(self, negative: int):
        """
        Rotate image depending on negative value:
        negative=0:     rotate left
        negative=1:     rotate right
        """
        rotated_image = pg.transform.rotate(PLAYER_IMAGE, self.rotation)
        rotated_image_brake = pg.transform.rotate(BRAKE_LIGHTS, self.rotation)
        new_rect = rotated_image.get_rect(center=(self.model.get_rect(topleft=(self.x, self.y)).center))
        self.model = rotated_image
        self.brake_model = rotated_image_brake
        self.rotation += ANGLE_ROTATE * (-1) ** negative
        self.x, self.y = new_rect.topleft

    def rotate_left(self) -> None:
        """Rotate left image left"""
        if self.rotation < MAX_ANGLE:
            self.rotate(negative=0)

    def rotate_right(self) -> None:
        """Rotate right image right"""
        if self.rotation > -MAX_ANGLE:
            self.rotate(negative=1)

    #TODO fix rotation back
    def rotate_back(self, is_collision: pg.Rect) -> None:
        if is_collision == "upper":
            self.rotate_right()
            #TODO adjust bounces to the y speed (speed impact)
            self.y += 1
        elif self.rotation < 0 and is_collision == "lower":
            self.rotate_left()
            self.y -= 1
        elif is_collision == "lower":
            self.y -= 1