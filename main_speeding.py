
import pygame as pg
import math
from collections import Counter
import random
from itertools import product

from class_player import Player
from classes_other import Game, Truck
from utils import (
    get_random_colors,
    scroll_background,
    scroll_lamps
)
from config import (
    WIN,
    WIDTH,
    HEIGHT,
    DRIVING_AREA_SIZE,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    HIGHWAY_IMAGE_WIDTH,
    AREA_SURFACE
)

pg.display.set_caption("Highway ride")

def draw_tiremarks(player: Player):
    pass


# PLAYER HANDLING
def input_player(player: Player, is_collision: bool) -> None:
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
    if is_collision:
        player.rotate_back()




# SCREEN UPDATING
def update_screen(player: Player, truck: Truck) -> None:
    """Updates screen images' positions"""
    player_model = player.brake_model if player.brakes_light else player.model
    WIN.blit(player_model, (player.x, player.y))
    WIN.blit(truck.model, (truck.x, truck.y))

    # testing rect surface for further implementation of collisions

    # colors = get_random_colors()
    # rect_player = player.get_rect()
    # rect_truck = truck.get_rect()
    upper, lower = create_boundaries(player)
    WIN.blit(AREA_SURFACE, (0,0))
    pg.draw.rect(AREA_SURFACE, (0,0,0), upper)
    pg.draw.rect(AREA_SURFACE, (0,0,0), lower)
    # WIN.blit(LAMP_IMAGE, (300, 750))
    pg.display.update()


CHANCE_OF_SPAWN = 0.1
def spawn_traffic(density):
    chance = random.random()
    if chance < CHANCE_OF_SPAWN:
        pass

# PHYSICS COLLISION
def check_collision_with_player(player_rect: pg.Rect, object: pg.Rect):
    return True if player_rect.colliderect(object) else False


def check_collision_cars(game: Game, player: Player, traffic_cars: list) -> bool:
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


def create_boundaries(player: Player) -> tuple:
    upper = pg.Rect(0, 0, WIDTH, DRIVING_AREA_SIZE[0] + 25)
    lower = pg.Rect(0, HEIGHT - player.width * player.get_tan(player.rotation), WIDTH, 100)
    return upper, lower


def check_boundaries_collision(player: Player, upper: pg.Rect, lower: pg.Rect):
    """Return True if player collided with upper or lower boundary"""
    player_rect = player.get_rect()
    if check_collision_with_player(player_rect, upper) or check_collision_with_player(player_rect, lower):
        return True
    else:
        return False


# MAIN
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
        upper_b, lower_b = create_boundaries(player)
        is_collision = check_boundaries_collision(player, upper_b, lower_b)
        print(is_collision)
        # player actions
        input_player(player, is_collision)

        # ai actions
        truck1.constant_speed()
        # truck1.no_acceleration()

        # print(check_collision_cars(game1, player, traffic_cars))

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