
import random
from typing import Optional, Union

import numpy as np
import pygame as pg

from class_player import Player
from classes_other import Chopper, Cloud, Game, Police, Truck, distance
from collisions import collisions
from config import (AREA_SURFACE, CLOUD_DENSITY, HIGHWAY_IMAGE_WIDTH,
                    NUM_OF_TRAFFIC, PROBABILITY_OF_SPAWN,
                    PROBABILITY_OF_SPAWN_CLOUD, WIN)
from utils import (create_boundaries, create_cloud, create_color_cars_dict,
                   create_spawning_locations, create_traffic_car,
                   get_random_car, get_random_colors, scroll_background,
                   scroll_lamps)

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
    if keys_pressed[pg.K_c]:
        AREA_SURFACE.fill(pg.Color(0,0,0,0))
    if keys_pressed[pg.K_p]:
        police_car.turn_police_lights_on()
    # else:
    #     police_car.turn_police_ligths_off()


def debug(
    player: Player,
    traffic_cars: np.array,
    police_car: Police,
    upper_b: pg.Rect,
    lower_b: pg.Rect
    ) -> None:
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
        pg.draw.rect(AREA_SURFACE, (255, 0, 0), rect_player, 2)
        pg.draw.rect(AREA_SURFACE, (0, 255, 0), pg.Rect(player.x, player.y, player.width, player.height), 1)
        pg.draw.rect(AREA_SURFACE, (127, 127, 127), upper_b, 1 )
        pg.draw.rect(AREA_SURFACE, (127, 127, 127), lower_b, 1 )

    # police_car.constant_speed()
    # police_car.free_decelaration()
    # police_car.turn_police_lights_on()
    # print(police_car.rotation, police_car.x, police_car.y)
    # police_car.change_line()

def show_moving_objects(array: np.array) -> np.array:
    """
    Display every object in array. Pop object if outside of screen.
    """
    objects_to_pop = []
    for index, object in enumerate(array):
        if not object.isOut:
            WIN.blit(object.model, (object.x, object.y))
        else:
            objects_to_pop.append(index)
    return np.delete(array, objects_to_pop)

# SCREEN UPDATING
def update_screen(
    player: Player,
    traffic_cars: np.array,
    police: Police,
    chopper: Chopper,
    clouds: np.array
    ) -> None:
    """
    Updates screen images' positions.
    Mind the sequence of displaying not to overwrite any object
    """

    player_model = player.brake_model if player.brakes_light else player.model
    traffic_cars = show_moving_objects(traffic_cars)

    WIN.blit(player_model, (player.x, player.y))
    WIN.blit(police.model, (police.x, police.y))
    WIN.blit(chopper.model, (chopper.x, chopper.y))
    WIN.blit(chopper.turbine_image, chopper.turbine_rect)

    clouds = show_moving_objects(clouds)
    WIN.blit(AREA_SURFACE, (0,0))

    pg.display.update()
    return traffic_cars, clouds


# TRAFFIC
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


def spawn_traffic(
    prob_of_spawn: int,
    density: int,
    car_colors: dict,
    traffic_cars: np.array,
    spawn_locations: list) -> np.ndarray:
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


def spawn_clouds(
    prob_of_spawn: int,
    density: int,
    clouds: np.ndarray[Cloud]) -> np.ndarray:
    """
    Spawn clouds
    """
    if len(clouds) >= density:
        return clouds
    chance_of_spawn = random.randint(0, 1000)
    if chance_of_spawn < prob_of_spawn:
        cloud = create_cloud()
        clouds = np.append(clouds, cloud)
    return clouds


def move_traffic(traffic_cars: np.array):
    for car in traffic_cars:
        car.free_decelaration()


def move_clouds(clouds: np.array):
    for cloud in clouds:
        cloud.move()


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
    chopper = Chopper()

    upper_b, lower_b = create_boundaries()
    locations_objs = create_spawning_locations()
    Car_Colors = create_color_cars_dict()

    scroll_speed_bg = 0
    scroll_speed_lamp = 0

    traffic_cars = np.array([], dtype=object)
    traffic_cars = np.append(traffic_cars, truck1)

    clouds = np.array([], dtype=object)

    while run:
        pg.display.flip()
        clock.tick(40)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        # background scrolling and rendering additional images of highway
        scroll_speed_bg = scroll_background(scroll_speed_bg)
        if abs(scroll_speed_bg) > HIGHWAY_IMAGE_WIDTH:
            scroll_speed_bg = 0

        # DISPLAY OBJECTS ON SCREEN
        traffic_cars, clouds = update_screen(player, traffic_cars, police_car, chopper, clouds)
        
        # CHECK IF PLAYER COLLIDED WITH BOUNDARY OR CAR
        collisions(player, traffic_cars, upper_b, lower_b, chopper)

        # CHOPPER TURBINES TEST
        chopper.rotate_turbine()

        # CHOPPER MOVING TEST
        if chopper.isMoving:
            chopper.moveToDestination()
            if chopper.onDestination():
                chopper.isMoving = False

        # CLOUDS
        clouds = spawn_clouds(PROBABILITY_OF_SPAWN_CLOUD, CLOUD_DENSITY, clouds)
        move_clouds(clouds)

        # CHECK FOR PLAYER'S INPUT
        input_player(player, police_car)

        # TRAFFIC
        move_traffic(traffic_cars)
        traffic_cars = spawn_traffic(PROBABILITY_OF_SPAWN, NUM_OF_TRAFFIC, Car_Colors, traffic_cars, locations_objs)

        # DEBUG
        debug(player, traffic_cars, police_car, upper_b, lower_b)
    pg.quit()


if __name__ == "__main__":
    main()



#   def __getattr__(self, _attr):
#         if hasattr(self.env, _attr):
#             return getattr(self.env, _attr)
#         else:
#             raise AttributeError