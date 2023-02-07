import math
from collections import Counter
from importlib.util import set_loader

import pygame as pg

WIDTH, HEIGHT = 1900, 1000

PLAYER_WIDTH, PLAYER_HEIGHT = WIDTH // 4, HEIGHT // 7
WIN = pg.display.set_mode((WIDTH, HEIGHT))
PLAYER_IMAGE = pg.transform.rotate(pg.image.load("images/player_car_new.png"), -90)

DRIVING_AREA_SIZE = (HEIGHT//5, 4*HEIGHT//5)


SPEED_PLAYER = 0
MAX_SPEED_PLAYER = 20
ACELERATION = 0.5

SPEED_CAR_SIDEWAYS = 5
FRICTION_DECEL = 0.5     # decelaration caused by friction and no acceleration
BRAKE_DECEL = 10

ANGLE_ROTATE = 2
ROTATION_BACK_SPEED_ANGLE = 2
MAX_ANGLE = 45

pg.display.set_caption("Highway ride")

class Car:
    def __init__(self) -> None:
        self._x
        self._y
        self.model


class Player(Car):
    def __init__(self) -> None:
        self._x = PLAYER_WIDTH
        self._y = HEIGHT // 2
        self.rotation = 0
        self.image = PLAYER_IMAGE
        self.speed = SPEED_PLAYER
        self.decelaration = FRICTION_DECEL
        self.rect = pg.Rect(self.x, self.y, 0, 0)

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
    
    # def rect(self):
        # return self.rect
    
    
    def point(self):
        return (self.x, self.y + PLAYER_HEIGHT // 2)

    def get_tan(self) -> float:
        """Convert angle rotation of the player from the x axis to value of tangens of it"""
        return math.tan(math.radians(abs(self.rotation)))

    def rotate_left(self) -> None:
        if self.rotation < MAX_ANGLE:
            self.image = pg.transform.rotate(PLAYER_IMAGE, self.rotation)
            self.rotation += ANGLE_ROTATE

    def rotate_right(self) -> None:
        if self.rotation > -MAX_ANGLE:
            self.image = pg.transform.rotate(PLAYER_IMAGE, self.rotation)
            self.rotation -= ANGLE_ROTATE


def rotate_around_point(image, angle, point):
    # Get the rectangle of the image
    rect = image.get_rect()
    
    # Translate the rectangle so that the point to rotate around becomes the origin
    rect.center = point
    rect = rect.move(-rect.width / 2, -rect.height / 2)
    
    # Perform the rotation
    rotated_image = pg.transform.rotate(image, angle)
    rot_rect = rotated_image.get_rect(center=rect.center)
    
    # Translate the rectangle back to its original position
    rot_rect = rot_rect.move(rect.width / 2, rect.height / 2)
    
    return rotated_image, rot_rect



def move_player(player: Player, rotation_point: tuple[int]) -> None:
    keys_pressed = pg.key.get_pressed()
    # if keys_pressed[pg.K_a]:
        # player.image, player.rect = rotate_around_point(player.image, 3, rotation_point)
    #    player.rotate_left()
    if keys_pressed[pg.K_d]:
        player.image, player.rect = rotate_around_point(player.image, -3, rotation_point)
        # player.rotate_right()


def update_screen(player: Player) -> None:
    """Updates screen images' positions"""
    WIN.blit(player.image, player.rect)
    pg.display.update()



def main(*args, **kwargs):
    clock = pg.time.Clock()
    pg.init()
    run = True
    player = Player()
    scroll_speed_bg = 0


    while run:
        clock.tick(40)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        rotation_point = (PLAYER_WIDTH, player.image.get_rect().height / 2)
        move_player(player, rotation_point)
        update_screen(player)
        print(player.point())
    pg.quit()


if __name__ == "__main__":
    main()