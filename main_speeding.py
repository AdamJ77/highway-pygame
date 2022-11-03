
import pygame as pg
import math
from collections import Counter
import random

from itertools import product

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
    bg_tiles,
    SCROLL_SPEED,
    TRUCK_HEIGHT,
    TRUCK_WIDTH,
    TRUCK_IMAGE,
    LAMPS_IMAGE,
    lamp_tiles,
    LAMPS_WIDTH,
    BRAKE_LIGHTS,
    AREA_SURFACE
)

pg.display.set_caption("Highway ride")


class Game:
    pass


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
        if self.x - self.decelaration > 0:
            self.x -= self.decelaration * 6

    # or classmethod Truck


class Truck(Car):
    def __init__(self) -> None:
        super().__init__()
        self.model = TRUCK_IMAGE
        self.width = TRUCK_WIDTH
        self.height = TRUCK_HEIGHT



class Player(Car):
    def __init__(self) -> None:
        super().__init__()
        self._x = WIDTH // 5
        self._y = HEIGHT // 2
        self.model = PLAYER_IMAGE
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = SPEED_PLAYER
        self.decelaration = FRICTION_DECEL
        self.brakes_light = False
        self.brake_model = BRAKE_LIGHTS


    def get_rect(self):
        """Create and return Rect object based on self attributes"""
        x_cord = self.x
        y_cord = self.y
        if self.rotation < 0:
            y_cord = self.y + self.width // 2 * self.get_tan(self.rotation)
        return pg.Rect(x_cord, y_cord, self.width, self.height)


    @staticmethod
    def get_tan(angle) -> float:
        """Get tangens value of given angle"""
        return math.tan(math.radians(abs(angle)))

    def move_forward(self) -> None:
        """Move car forward depending on the car's rotation"""
        if self.x + self.speed < WIDTH - PLAYER_WIDTH:
            self.x += self.speed
            if self.speed < self.max_speed:
                self.speed += ACELERATION
            self.move_sideways()

    def move_sideways(self) -> None:
        """Move sideways if there is rotation != 0"""
        tan_angle = self.get_tan(self.rotation)
        if self.rotation > 0 and self.y - self.speed * tan_angle > DRIVING_AREA_SIZE[0]:
            self.y -= (self.speed + SCROLL_SPEED) * tan_angle
        if self.rotation < 0 and self.y + self.speed * tan_angle < DRIVING_AREA_SIZE[1]:
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
    def rotate_back(self) -> None:
        if self.rotation > 0:
            self.rotate_right()
        if self.rotation < 0:
            self.rotation += ROTATION_BACK_SPEED_ANGLE
            self.model = pg.transform.rotate(PLAYER_IMAGE, self.rotation)


def input_player(player: Player) -> None:
    """Check if certain keys were pressed or not"""
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
    elif not keys_pressed[pg.K_w] and not keys_pressed[pg.K_SPACE]:
        player.no_acceleration()
    if not keys_pressed[pg.K_s]:
        player.brakes_light = False
    if keys_pressed[pg.K_SPACE]:
        player.constant_speed()
    #TODO check if necessary
    # elif not keys_pressed[pg.K_a] and not keys_pressed[pg.K_d] and player.rotation != 0:
    #     player.rotate_back()


def draw_tiremarks(player: Player):
    pass



def update_screen(player: Player, truck: Truck) -> None:
    """Updates screen images' positions"""
    player_model = player.brake_model if player.brakes_light else player.model
    WIN.blit(player_model, (player.x, player.y))
    WIN.blit(truck.model, (truck.x, truck.y))

    # testing rect surface for further implementation of collisions

    # colors = get_random_colors()
    # rect_player = player.get_rect()
    # rect_truck = truck.get_rect()
    # WIN.blit(AREA_SURFACE, (0,0))
    # pg.draw.rect(AREA_SURFACE, colors, rect_truck)

    # WIN.blit(LAMP_IMAGE, (300, 750))
    pg.display.update()



def scroll_background(scroll_speed_bg: int):
    for index in range(bg_tiles):
        WIN.blit(HIGHWAY_IMAGE, (index * HIGHWAY_IMAGE_WIDTH + scroll_speed_bg, 0))
        scroll_speed_bg -= SCROLL_SPEED # -5
    return scroll_speed_bg



#TODO fix lamps
def scroll_lamps(scroll_speed_lamp: int):
    for index in range(lamp_tiles):
        WIN.blit(LAMPS_IMAGE, (index * LAMPS_WIDTH + scroll_speed_lamp, 0))
        scroll_speed_lamp -= SCROLL_SPEED
    return scroll_speed_lamp



CHANCE_OF_SPAWN = 0.1
def spawn_traffic(density):
    chance = random.random()
    if chance < CHANCE_OF_SPAWN:
        pass



def check_collision(game: Game, player: Player, traffic_cars: list):
    rect_player = player.get_rect()
    for car in traffic_cars:
        rect_car = car.get_rect()
        return True if rect_player.colliderect(rect_car) else False



def get_corner_of_collision(player: Player) -> object:
    pl_centr_x, pl_centr_y = player.get_center_point()
    boundaries_x = [pl_centr_x + PLAYER_WIDTH // 2, pl_centr_x - PLAYER_WIDTH // 2]
    boundaries_y = [pl_centr_y + PLAYER_HEIGHT // 2, pl_centr_y - PLAYER_HEIGHT // 2]
    prod = product(boundaries_x, boundaries_y)
    return prod


def get_random_colors():
    """Return RGB list color"""
    return [random.randint(0, 255) for _ in range(3)]



def main(*args, **kwargs):
    clock = pg.time.Clock()
    pg.init()
    run = True

    #TODO game not definied yet
    game1 = Game()
    player = Player()
    truck1 = Truck()
    scroll_speed_bg = 0
    scroll_speed_lamp = 0
    traffic_cars = [truck1]

    while run:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        # background scrolling and rendering additional images of highway
        scroll_speed_bg = scroll_background(scroll_speed_bg)
        if abs(scroll_speed_bg) > HIGHWAY_IMAGE_WIDTH:
            scroll_speed_bg = 0


        # lamps rendering
        # TODO fix optimization
        # scroll_speed_lamp = scroll_lamps(scroll_speed_lamp)
        # if abs(scroll_speed_lamp) > HIGHWAY_IMAGE_WIDTH:
        #     scroll_speed_lamp = 0


        # player actions
        input_player(player)

        # ai actions
        truck1.constant_speed()
        # truck1.no_acceleration()

        print(check_collision(game1, player, traffic_cars))

        # testing classmethod slomo
        # if player.x > HIGHWAY_IMAGE_WIDTH // 2:
        #     player.slomo_test()

        #update screen
        update_screen(player, truck1)

        #TODO logging
        #print(player.rotation)

        # print(player.get_center_point())


        # pg.draw.circle(WIN, black, tuple(player.get_center_point()), 20)
    pg.quit()


if __name__ == "__main__":
    main()