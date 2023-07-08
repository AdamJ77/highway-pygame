import math

import pygame as pg

from classes_other import Car
from config import (ACELERATION, ANGLE_ROTATE, BRAKE_DECEL, BRAKE_LIGHTS,
                    HEIGHT, MAX_ANGLE, MAX_SPEED_PLAYER, PLAYER_HEIGHT,
                    PLAYER_IMAGE, PLAYER_WIDTH, SCROLL_SPEED, SPEED_PLAYER,
                    WIDTH)


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
        self.speed_x = SPEED_PLAYER
        self.speed_y = (self.speed_x + SCROLL_SPEED) * self.get_tan_abs(self.rotation)

    def get_rect(self):
        """
        Create and return Rect object based on self attributes
        Upper rect (red)
        """
        y_cord = self.y
        if self.rotation > 0:
            y_cord += 10
        if self.rotation < 0:
            y_cord = self.y + self.get_height() // 2 * self.get_tan_abs(self.rotation)
        return pg.Rect(self.x + PLAYER_WIDTH // 2, y_cord + 10, self.width // 2, self.height - 15)

        # if self.rotation != 0:
            # y_cord = self.y + self.get_sin(self.rotation) * self.get_height() // 2
        # return pg.Rect(self.x + PLAYER_WIDTH // 2, y_cord, self.width // 2, self.height)
    
    def get_rect_2(self):
        """ Second collision rectangle (blue)"""
        if self.rotation < 0:
            rect = pg.Rect(self.x + 15 * self.get_tan_abs(self.rotation), self.y + 25 * self.get_tan_abs(self.rotation), PLAYER_WIDTH // 2, self.get_height() // 2)
        elif self.rotation > 0:
            rect = pg.Rect(self.x + 15 * self.get_tan_abs(self.rotation), self.y + self.get_height() // 2, PLAYER_WIDTH // 2, self.get_height() // 2 - 15 * self.get_tan_abs(self.rotation))
        else:
            rect = pg.Rect(self.x, self.y + 10, PLAYER_WIDTH // 2, PLAYER_HEIGHT - 15)
        return rect
        
    def get_height(self):
        return self.model.get_height()

    def get_real_speed(self) -> float:
        """Return float compound speed (real_speed)"""
        return math.sqrt(self.speed_x ** 2 + self.speed_y ** 2)

    def set_height(self):
        self.height = PLAYER_HEIGHT + PLAYER_HEIGHT * self.get_tan_abs(self.rotation)


    @staticmethod
    def get_tan(angle) -> float:
        """Get tangens value of given angle"""
        return math.tan(math.radians(angle))

    @staticmethod
    def get_cot(angle) -> float:
        """Get tangens value of given angle"""
        tan = math.tan(math.radians(abs(angle)))
        return 1//tan
    
    def speed_up(self):
        if self.get_real_speed() < MAX_SPEED_PLAYER:
            self.speed_x += ACELERATION
            self.speed_y = self.speed_x * self.get_tan_abs(self.rotation) 

    def slow_down(self):
        self.speed_x -= self.decelaration
        self.speed_y = SPEED_PLAYER * self.get_tan_abs(self.rotation)

    def move_forward(self) -> None:
        """Move car forward depending on the car's rotation"""
        # if self.get_real_speed() > MAX_SPEED_PLAYER:
        #     # self.speed_y = MAX_SPEED_PLAYER - self.speed_x
        #     pass
        if self.x + self.speed_x < WIDTH - PLAYER_WIDTH:
            self.x += self.speed_x
            if self.speed_x < self.max_speed:
                self.speed_x += ACELERATION
        self.move_sideways()


    def move_sideways(self) -> None:
        """Move sideways if there is rotation != 0"""
        tan_angle = self.get_tan_abs(self.rotation)
        # Limits max y speed while turning
        self.speed_y = (self.speed_x + SCROLL_SPEED) * tan_angle if self.speed_y <= MAX_SPEED_PLAYER else MAX_SPEED_PLAYER 
        # y_speed = (self.speed_x + SCROLL_SPEED) * tan_angle
        self.y += self.speed_y if self.rotation <= 0 else -self.speed_y


    def no_acceleration(self) -> None:
        """Speed down if no acceleration"""
        if self.speed_x > SPEED_PLAYER + 1 and (new_x := self.x + self.speed_x) < WIDTH - PLAYER_WIDTH:
            if self.speed_x - self.decelaration >= SPEED_PLAYER:
                self.speed_x -= self.decelaration
                self.x = new_x
        else:
            self.speed_x = SPEED_PLAYER
            self.free_decelaration()
        self.move_sideways()


    def free_decelaration(self):
        if self.x - self.decelaration > 0:
            self.x -= self.decelaration * 6

    def brake(self) -> None:
        """Massive speed down"""
        if (new_speed:=self.speed_x - self.decelaration * 3) >= SPEED_PLAYER:
                self.speed_x = new_speed
                self.x += self.speed_x
        elif not self.speed_x and (new_x:= self.x - BRAKE_DECEL) > 0:
                self.x = new_x
        self.move_sideways()
        self.brakes_light = True


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

    def rotate_back(self, is_collision: str) -> None:
        if is_collision == "upper" or is_collision == "top":
            if self.rotation > 0:
                self.rotate_right()
            self.y += 1
        elif is_collision == "lower" or is_collision == "bottom":
            if self.rotation < 0:
                self.rotate_left()
            self.y -= 1

    def draw_tiremarks(self):
        pass