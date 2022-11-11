
import pygame as pg
from collections import Counter
import random
from itertools import product
from typing import Union
from typing import Optional
import numpy as np

from class_player import Player
from classes_other import Game, Truck, Car, ColorCar, Location
from utils import (
    get_random_colors,
    scroll_background,
    scroll_lamps,
    create_color_cars_dict
)
from config import (
    WIN,
    WIDTH,
    HEIGHT,
    DRIVING_AREA_SIZE,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    HIGHWAY_IMAGE_WIDTH,
    AREA_SURFACE,
    CAR_HEIGHT,
    CAR_WIDTH,
    SPAWN_LOCATIONS
)

pg.display.set_caption("Highway ride")

def draw_tiremarks(player: Player):
    pass


# PLAYER HANDLING
def input_player(
    player: Player,
    is_collision: Union[pg.Rect, bool],
    upper: pg.Rect,
    traffic_cars: Optional[np.array]
    ) -> None:
    """Handle player's event"""

    keys_pressed = pg.key.get_pressed()
    if keys_pressed[pg.K_w] and not keys_pressed[pg.K_s]:
        player.move_forward()
    if keys_pressed[pg.K_a]:
       player.rotate_left()
    if keys_pressed[pg.K_d]:
        player.rotate_right()
    if keys_pressed[pg.K_s]:
        player.brake()
    if not keys_pressed[pg.K_w] and not keys_pressed[pg.K_SPACE] and not keys_pressed[pg.K_s]:
        player.no_acceleration()
    if not keys_pressed[pg.K_s]:
        player.brakes_light = False
    if keys_pressed[pg.K_SPACE]:
        player.constant_speed()
        player.speed = 0
    if is_collision:
        boundary = "upper" if is_collision is upper else "lower"
        player.rotate_back(boundary)

    if keys_pressed[pg.K_q]:
        rect_player = player.get_rect()
        for car in traffic_cars:
            car_rect = car.get_rect()
            pg.draw.rect(AREA_SURFACE, (255,255,255), car_rect, 1)
        pg.draw.rect(AREA_SURFACE, (255,255,255), rect_player, 1)



# SCREEN UPDATING
def update_screen(
    player: Player,
    traffic_cars: np.array
    ) -> None:
    """Updates screen images' positions"""

    player_model = player.brake_model if player.brakes_light else player.model
    WIN.blit(player_model, (player.x, player.y))
    cars_to_pop = []
    for index, car in enumerate(traffic_cars):
        if not car.isOut:
            WIN.blit(car.model, (car.x, car.y))
        else:
            cars_to_pop.append(index)
    traffic_cars = np.delete(traffic_cars, cars_to_pop)
    # testing rect surface for further implementation of collisions
    # colors = get_random_colors()
    # rect_player = player.get_rect()
    # rect_truck = truck.get_rect()
    # area_down = pg.Rect(0, DRIVING_AREA_SIZE[1] - PLAYER_WIDTH * player.get_tan_abs(player.rotation) + 10, WIDTH, 10)
    # area_up = pg.Rect(0, DRIVING_AREA_SIZE[0], WIDTH, 10)
    # upper, lower = create_boundaries()
    WIN.blit(AREA_SURFACE, (0,0))
    # pg.draw.rect(AREA_SURFACE, (0,0,0), upper)
    # pg.draw.rect(AREA_SURFACE, (0,0,0), lower)
    # pg.draw.rect(AREA_SURFACE, (255,255,255), rect_player, 1)
    # pg.draw.rect(AREA_SURFACE, (255, 255, 255), area_down)
    # pg.draw.rect(AREA_SURFACE, (255, 255, 255), area_up)
    # WIN.blit(LAMP_IMAGE, (300, 750))
    pg.display.update()
    return traffic_cars

def create_color_car(
    col_val,
    traffic_cars: np.array,
    spawn_locations):
    """Create Car instance with given color and set random empty location"""

    new_car = Car()
    new_car.width = CAR_WIDTH
    new_car.height = CAR_HEIGHT
    new_car.model = col_val
    location = random.choice(spawn_locations)
    new_car.x, new_car.y = location.spawn_location
    return new_car


def spawn_traffic(
    prob_of_spawn: int,
    density: int,
    car_colors: dict,
    traffic_cars: np.array,
    spawn_locations: tuple):
    """Density parameter is max num of cars created"""

    if len(traffic_cars) >= density:
        return traffic_cars
    chance_of_spawn = random.randint(0, 1000)
    if chance_of_spawn < prob_of_spawn:
        col_val = random.choice(list(car_colors.values()))
        new_car = create_color_car(col_val, traffic_cars, spawn_locations)
        traffic_cars = np.append(traffic_cars, new_car)
    return traffic_cars


def move_traffic(traffic_cars: np.array):
    for car in traffic_cars:
        car.no_acceleration()

# PHYSICS COLLISION
def check_collision_with_player(
    player_rect: pg.Rect,
    object: pg.Rect
    ) -> bool:
    """Return True if player collided with object else False"""

    return True if player_rect.colliderect(object) else False


def check_collision_cars(
    game: Game,
    player: Player,
    traffic_cars: np.array
    ) -> bool:

    rect_player = player.act_rect
    for car in traffic_cars:
        rect_car = car.get_rect()
        if rect_player.colliderect(rect_car):
            check_side_collision(rect_player, rect_car, player)
    return

def check_side_collision(
    rect_player: pg.Rect,
    rect_car: pg.Rect,
    player: Player
    ):

    # direction = None
    if rect_player.bottom >= rect_car.top and player.old_rect.bottom:
        print("bottom collision")

        # direction = "bottom"
        # constraints.update({"bottom": True})
    elif rect_player.top <= rect_car.bottom:
        print("top collision")
        # direction = "top"
        # constraints.update({"top": True})
    elif rect_player.right >= rect_car.left:
        print("right collision")
        # direction = "right"
        # constraints.update({"right": True})
    elif rect_player.left <= rect_player.right:
        # direction = "left"
        print("left collision")
        # constraints.update({"left": True})

    # constraints = {direc:(False if direc is not direction else True) for direc in ["top", "bottom", "right", "left"]}
    return

def get_corner_of_collision(player: Player) -> product:
    pl_centr_x, pl_centr_y = player.get_center_point()
    boundaries_x = [pl_centr_x + PLAYER_WIDTH // 2, pl_centr_x - PLAYER_WIDTH // 2]
    boundaries_y = [pl_centr_y + PLAYER_HEIGHT // 2, pl_centr_y - PLAYER_HEIGHT // 2]
    prod = product(boundaries_x, boundaries_y)
    return prod


def create_boundaries() -> tuple:
    upper = pg.Rect(0, 0, WIDTH, DRIVING_AREA_SIZE[0] + 25)
    lower = pg.Rect(0, HEIGHT - 170, WIDTH, 100)
    return (upper, lower)


def check_boundaries_collision(
    player: Player,
    upper: pg.Rect,
    lower: pg.Rect
    ):
    """Return True if player collided with upper or lower boundary"""

    if check_collision_with_player(player.act_rect, upper):
        return upper
    elif check_collision_with_player(player.act_rect, lower):
        return lower
    else:
        return False


def create_spawning_locations():
    loc1 = Location.location(SPAWN_LOCATIONS[0])
    loc2 = Location.location(SPAWN_LOCATIONS[1])
    loc3 = Location.location(SPAWN_LOCATIONS[2])
    return loc1, loc2, loc3


# AI actions
# maniac/police tailgating player
def automatic_following(player: Player, car: Car):
    pass






# MAIN
def main(*args, **kwargs):
    clock = pg.time.Clock()
    pg.init()
    run = True

    #TODO game not definied yet
    game1 = Game()
    player = Player()
    truck1 = Truck()
    upper_b, lower_b = create_boundaries()

    locations_objs = create_spawning_locations()
    # gen = [location.spawn_location for location in random.choice(locations_objs)]
    # print(gen)
    scroll_speed_bg = 0
    scroll_speed_lamp = 0

    traffic_cars = np.array([], dtype=object)
    traffic_cars = np.append(traffic_cars, truck1)

    # create color cars
    Car_Colors = create_color_cars_dict()

    # collisions = ["top", "bottom", "right", "left"]
    # constraints = {side:False for side in collisions}
    coll_rect = False

    while run:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.type == pg.K_q:
                coll_rect = True
            else:
                coll_rect = False

        # background scrolling and rendering additional images of highway
        scroll_speed_bg = scroll_background(scroll_speed_bg)
        if abs(scroll_speed_bg) > HIGHWAY_IMAGE_WIDTH:
            scroll_speed_bg = 0

        # lamps rendering
        # TODO fix optimization
        # scroll_speed_lamp = scroll_lamps(scroll_speed_lamp)
        # if abs(scroll_speed_lamp) > HIGHWAY_IMAGE_WIDTH:
        #     scroll_speed_lamp = 0


        player.old_rect = player.get_rect()
        for car in traffic_cars:
            car.old_rect = car.get_rect()
        traffic_cars = update_screen(player, traffic_cars)

        player.act_rect = player.get_rect()
        # collision
        is_collision = check_boundaries_collision(player, upper_b, lower_b)
        check_collision_cars(game1, player, traffic_cars)

        # player actions
        input_player(player, is_collision, upper_b, traffic_cars)

        # ai actions
        move_traffic(traffic_cars)
        traffic_cars = spawn_traffic(30, 4, Car_Colors, traffic_cars, locations_objs)

        print(len(traffic_cars) )
        # testing
        # print(constraints)

        #update screen
        # traffic_cars =

        #TODO logging

    pg.quit()


if __name__ == "__main__":
    main()