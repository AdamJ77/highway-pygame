
import pygame as pg
import math
from collections import Counter

from config import (
    WIN,
    WIDTH,
    HEIGHT,
    DRIVING_AREA_SIZE,
    PLAYER_IMAGE,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    SPEED_PLAYER,
    MAX_SPEED_PLAYER,
    ACELERATION,
    SPEED_CAR_SIDEWAYS,
    FRICTION_DECEL,
    BRAKE_DECEL,
    ANGLE_ROTATE,
    ROTATION_BACK_SPEED_ANGLE,
    MAX_ANGLE,
    HIGHWAY_IMAGE,
    HIGHWAY_IMAGE_WIDTH,
    tiles,
    SCROLL_SPEED,
    TRUCK_HEIGHT,
    TRUCK_WIDTH,
    TRUCK_IMAGE
)

pg.display.set_caption("Highway ride")

class Car:
    def __init__(self) -> None:
        self._x = 600
        self._y = 300
        self.model
        self.speed = SPEED_PLAYER
        self.decelaration = FRICTION_DECEL

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
        """Speed down if no acceleration"""
        if self.speed > SPEED_PLAYER and self.x + self.speed < WIDTH:
            if self.speed - self.decelaration >= SPEED_PLAYER:
                self.speed -= self.decelaration
                self.x += self.speed
        else:
            if self.x - self.decelaration > 0:
                self.x -= self.decelaration * 6

class Truck(Car):
    def __init__(self) -> None:
        # self._x = 900
        # self._y = 400
        self.model = TRUCK_IMAGE
        super().__init__()

class Player(Car):
    def __init__(self) -> None:
        self._x = WIDTH // 5
        self._y = HEIGHT // 2
        self.rotation = 0
        self.model = PLAYER_IMAGE
        self.speed = SPEED_PLAYER
        self.decelaration = FRICTION_DECEL
        # self.speed



    def get_tan(self) -> float:
        """Convert angle rotation of the player from the x axis to value of tangens of it"""
        return math.tan(math.radians(abs(self.rotation)))

    def move_forward(self) -> None:
        """Move car forward depending on the car's rotation"""
        if self.x + self.speed < WIDTH - PLAYER_WIDTH:
            self.x += self.speed
            if self.speed < MAX_SPEED_PLAYER:
                self.speed += ACELERATION
            self.move_sideways()

    def move_sideways(self) -> None:
        """Move sideways if there is rotation != 0"""
        if self.rotation > 0 and self.y - self.speed * self.get_tan() > DRIVING_AREA_SIZE[0]:
            self.y -= (self.speed + SCROLL_SPEED) * self.get_tan()
        if self.rotation < 0 and self.y + self.speed * self.get_tan() < DRIVING_AREA_SIZE[1]:
            self.y += (self.speed + SCROLL_SPEED) * self.get_tan()

    def no_acceleration(self) -> None:
        """Speed down if no acceleration"""
        if self.speed > SPEED_PLAYER and self.x + self.speed < WIDTH:
            if self.speed - self.decelaration >= SPEED_PLAYER:
                self.speed -= self.decelaration
                self.x += self.speed
        else:
            if self.x - self.decelaration > 0:
                self.x -= self.decelaration * 6
        self.move_sideways()

    def brake(self) -> None:
        """Massive speed down"""
        if self.speed > SPEED_PLAYER and self.x + self.speed < WIDTH:
            self.move_sideways()
            if self.speed - self.decelaration * 5 >= SPEED_PLAYER:
                self.speed -= self.decelaration * 5
                self.x += self.speed
            else:
                self.speed = SPEED_PLAYER
        elif not self.speed:
            if self.x - BRAKE_DECEL > 0:
                self.x -= BRAKE_DECEL
        # drifting mode to be added

    def rotate_left(self) -> None:
        """Rotate left image by ANGLE_ROTATE angle and increase rotation value"""
        if self.rotation < MAX_ANGLE:
            rotated_image = pg.transform.rotate(PLAYER_IMAGE, self.rotation)
            new_rect = rotated_image.get_rect(center=(self.model.get_rect(topleft=(self.x, self.y)).center))
            self.model = rotated_image
            self.rotation += ANGLE_ROTATE
            self.x, self.y = new_rect.topleft

    def rotate_right(self) -> None:
        """Rotate right image by ANGLE_ROTATE angle and decrease rotation value"""
        if self.rotation > -MAX_ANGLE:
            rotated_image = pg.transform.rotate(PLAYER_IMAGE, self.rotation)
            new_rect = rotated_image.get_rect(center=(self.model.get_rect(topleft=(self.x, self.y)).center))
            self.model = rotated_image
            self.rotation -= ANGLE_ROTATE
            self.x, self.y = new_rect.topleft

    def rotate_back(self) -> None:
        if self.rotation > 0:
            self.rotate_right()
        if self.rotation < 0:
            self.rotation += ROTATION_BACK_SPEED_ANGLE
            self.model = pg.transform.rotate(PLAYER_IMAGE, self.rotation)


def move_player(player: Player) -> None:
    keys_pressed = pg.key.get_pressed()
    # counter = Counter(keys_pressed)
    if keys_pressed[pg.K_w]:
        player.move_forward()
    if keys_pressed[pg.K_a]:
       player.rotate_left()
    if keys_pressed[pg.K_d]:
        player.rotate_right()
    if keys_pressed[pg.K_s]:
        player.brake()
    elif not keys_pressed[pg.K_w]:
        player.no_acceleration()
    elif not keys_pressed[pg.K_a] and not keys_pressed[pg.K_d] and not keys_pressed[pg.K_w]:
        player.rotate_back()


def draw_tiremarks(player: Player):
    pass

def update_screen(player: Player, truck: Truck) -> None:
    """Updates screen images' positions"""
    WIN.blit(player.model, (player.x, player.y))
    WIN.blit(truck.model, (truck.x, truck.y))
    # WIN.blit(LAMP_IMAGE, (300, 750))
    pg.display.update()

def scroll_background(scroll_speed_bg):
    for index in range(tiles):
            WIN.blit(HIGHWAY_IMAGE, (index * HIGHWAY_IMAGE_WIDTH + scroll_speed_bg, 0))
            scroll_speed_bg -= SCROLL_SPEED # -5
    return scroll_speed_bg

def scroll_lamps(scroll_speed_):
    pass




def main(*args, **kwargs):
    clock = pg.time.Clock()
    pg.init()
    run = True
    player = Player()
    truck1 = Truck()
    scroll_speed_bg = 0
    while run:
        clock.tick(120)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        scroll_speed_bg = scroll_background(scroll_speed_bg)
        if abs(scroll_speed_bg) > HIGHWAY_IMAGE_WIDTH:
            scroll_speed_bg = 0
        move_player(player)
        truck1.no_acceleration()
        update_screen(player, truck1)
        print(player.rotation)
    pg.quit()


if __name__ == "__main__":
    main()