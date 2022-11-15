
import pygame as pg
import random
from typing import Union
from typing import Optional
import numpy as np

from class_player import Player
from classes_other import Game, Truck, Police
from utils import (
    get_random_colors,
    scroll_background,
    scroll_lamps,
    create_color_cars_dict,
    create_spawning_locations,
    create_boundaries,
    get_random_car,
    create_traffic_car
)
from config import (
    WIN,
    HIGHWAY_IMAGE_WIDTH,
    AREA_SURFACE,
)

pg.display.set_caption("Highway ride")


# PLAYER HANDLING
def input_player(
    player: Player,
    police_car: Police
    ) -> None:
    """
    Handle player's keyboard event
    """
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


    if keys_pressed[pg.K_p]:
        police_car.turn_police_lights_on()
    # else:
    #     police_car.turn_police_ligths_off()


def debug(
    player: Player,
    traffic_cars: np.array,
    police_car: Police
    ):
    """
    Check for debug functions :
    q - draw all cars' rectangles
    """
    keys_pressed = pg.key.get_pressed()
    if keys_pressed[pg.K_q]:
        rect_player = player.get_rect()
        for car in traffic_cars:
            car_rect = car.get_rect()
            pg.draw.rect(AREA_SURFACE, (255,255,255), car_rect, 1)
        pg.draw.rect(AREA_SURFACE, (255,255,255), rect_player, 1)

    # police_car.constant_speed()
    police_car.free_decelaration()
    # police_car.turn_police_lights_on()
    print(police_car.rotation, police_car.x, police_car.y)
    police_car.change_line()


# SCREEN UPDATING
def update_screen(
    player: Player,
    traffic_cars: np.array,
    police: Police
    ) -> None:
    """
    Updates screen images' positions
    """
    player_model = player.brake_model if player.brakes_light else player.model
    cars_to_pop = []
    for index, car in enumerate(traffic_cars):
        if not car.isOut:
            WIN.blit(car.model, (car.x, car.y))
        else:
            cars_to_pop.append(index)
    traffic_cars = np.delete(traffic_cars, cars_to_pop)

    WIN.blit(player_model, (player.x, player.y))
    WIN.blit(police.model, (police.x, police.y))
    WIN.blit(AREA_SURFACE, (0,0))
    pg.display.update()
    return traffic_cars


def check_location(
    spawn_locations: list):
    """
    Check if randomly chosen location is still occupied by prev spawned car
    """
    location = random.choice(spawn_locations)
    if prev_car:= location.car_occupying:
        if prev_car.x + prev_car.width + 10 >= location.spawn_location[0]:
            return None
    return location

# TRAFFIC
def spawn_traffic(
    prob_of_spawn: int,
    density: int,
    car_colors: dict,
    traffic_cars: np.array,
    spawn_locations: list):
    """
    Density parameter is max num of cars created
    """
    if len(traffic_cars) >= density:
        return traffic_cars
    chance_of_spawn = random.randint(0, 1000)
    if chance_of_spawn < prob_of_spawn:
        location = check_location(spawn_locations)
        if not location:
            return traffic_cars
        chosen_model_car = get_random_car(car_colors)
        new_car = create_traffic_car(chosen_model_car, location)
        traffic_cars = np.append(traffic_cars, new_car)
    return traffic_cars


def move_traffic(traffic_cars: np.array):
    for car in traffic_cars:
        car.free_decelaration()


# PHYSICS COLLISION
def check_collision_with_player(
    player_rect: pg.Rect,
    object: pg.Rect
    ) -> bool:
    """
    Return True if player collided with object else False
    """
    return True if player_rect.colliderect(object) else False


def check_collision_cars(
    player: Player,
    traffic_cars: np.array
    ) -> bool:
    """
    Check if player's rect collided with other car's rect
    """
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
    """Check from on which side was collision"""
    # direction = None
    if rect_player.bottom >= rect_car.top:
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
    return


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


def collisions(
    player: Player,
    traffic_cars: np.array,
    upper: pg.Rect,
    lower: pg.Rect
    ):
    is_collision = check_boundaries_collision(player, upper, lower)
    if is_collision:
        boundary = "upper" if is_collision is upper else "lower"
        player.rotate_back(boundary)
    check_collision_cars(player, traffic_cars)


# AI actions
# maniac/police tailgating player


# MAIN
def main(*args, **kwargs):
    pg.init()
    clock = pg.time.Clock()
    run = True

    #TODO game not definied yet
    game1 = Game()
    player = Player()
    truck1 = Truck()
    police_car = Police()

    upper_b, lower_b = create_boundaries()
    locations_objs = create_spawning_locations()
    Car_Colors = create_color_cars_dict()

    scroll_speed_bg = 0
    scroll_speed_lamp = 0

    traffic_cars = np.array([], dtype=object)
    traffic_cars = np.append(traffic_cars, truck1)


    while run:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        # background scrolling and rendering additional images of highway
        scroll_speed_bg = scroll_background(scroll_speed_bg)
        if abs(scroll_speed_bg) > HIGHWAY_IMAGE_WIDTH:
            scroll_speed_bg = 0

        # UPDATE CARS IMAGES
        traffic_cars = update_screen(player, traffic_cars, police_car)

        # CHECK IF PLAYER COLLIDED WITH BOUNDARY OR CAR
        collisions(player, traffic_cars, upper_b, lower_b)

        # CHECK FOR PLAYER'S INPUT
        input_player(player, police_car)

        # TRAFFIC
        move_traffic(traffic_cars)
        traffic_cars = spawn_traffic(20, 4, Car_Colors, traffic_cars, locations_objs)

        # DEBUG
        debug(player, traffic_cars, police_car)
    pg.quit()


if __name__ == "__main__":
    main()