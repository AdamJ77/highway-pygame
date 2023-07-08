import random
from typing import Tuple

import numpy as np
import pygame as pg
from pygame import Rect
from pygame.rect import RectType

from classes_other import Car, Cloud, ColorCar, Location
from config import (CAR_HEIGHT, CAR_IMAGE_GREEN, CAR_IMAGE_PURPLE,
                    CAR_IMAGE_RED, CAR_WIDTH, CLOUD_1_IMAGE, CLOUD_2_IMAGE,
                    DRIVING_AREA_SIZE, HEIGHT, HIGHWAY_IMAGE,
                    HIGHWAY_IMAGE_WIDTH, LAMPS_IMAGE, LAMPS_WIDTH,
                    MUSCLE_CAR_HEIGHT, MUSCLE_CAR_IMAGE_YELLOW,
                    MUSCLE_CAR_WIDTH, SCROLL_SPEED, SEDAN_CAR_HEIGHT,
                    SEDAN_CAR_IMAGE_BROWN, SEDAN_CAR_WIDTH, SPAWN_LOCATIONS,
                    WIDTH, WIN, bg_tiles, lamp_tiles)


def get_random_colors() -> list[int]:
    """Return RGB list color"""
    return [random.randint(0, 255) for _ in range(3)]


def get_random_car(car_colors: dict):
    rand_val = random.randint(1, 5)
    return car_colors.get(ColorCar(rand_val))


def scroll_background(scroll_speed_bg: int) -> int:
    for index in range(bg_tiles):
        WIN.blit(HIGHWAY_IMAGE, (index * HIGHWAY_IMAGE_WIDTH + scroll_speed_bg, 0))
        scroll_speed_bg -= SCROLL_SPEED # -5
    return scroll_speed_bg


#TODO fix lamps
def scroll_lamps(scroll_speed_lamp: int) -> int:
    for index in range(lamp_tiles):
        WIN.blit(LAMPS_IMAGE, (index * LAMPS_WIDTH + scroll_speed_lamp, 0))
        scroll_speed_lamp -= SCROLL_SPEED
    return scroll_speed_lamp


def create_color_cars_dict() -> dict:
    Car_Colors = {}
    Car_Colors[ColorCar.CAR_GREEN] = [CAR_IMAGE_GREEN, (CAR_WIDTH, CAR_HEIGHT)]
    Car_Colors[ColorCar.CAR_RED] = [CAR_IMAGE_RED, ((CAR_WIDTH, CAR_HEIGHT))]
    Car_Colors[ColorCar.CAR_PURPLE] = [CAR_IMAGE_PURPLE, (CAR_WIDTH, CAR_HEIGHT)]
    Car_Colors[ColorCar.MUSCLE_CAR_YELLOW] = [MUSCLE_CAR_IMAGE_YELLOW, (MUSCLE_CAR_WIDTH, MUSCLE_CAR_HEIGHT)]
    Car_Colors[ColorCar.SEDAN_BROWN] = [SEDAN_CAR_IMAGE_BROWN, (SEDAN_CAR_WIDTH, SEDAN_CAR_HEIGHT)]
    return Car_Colors


def create_spawning_locations() -> tuple[Location]:
    loc1 = Location.location(SPAWN_LOCATIONS[0], 1)
    loc2 = Location.location(SPAWN_LOCATIONS[1], 2)
    loc3 = Location.location(SPAWN_LOCATIONS[2], 3)
    return loc1, loc2, loc3


def create_boundaries() -> tuple[Rect | RectType, Rect | RectType]:
    upper = pg.Rect(0, 0, WIDTH, DRIVING_AREA_SIZE[0] + 25)
    lower = pg.Rect(0, DRIVING_AREA_SIZE[1] - 35, WIDTH, 100)
    return (upper, lower)


def create_traffic_car(
    chosen_car: list,
    location: object
    ):
    """
    Create Car object with given model and location
    """
    new_car = Car()
    new_car.width, new_car.height = chosen_car[1]
    new_car.model = chosen_car[0]
    new_car.x, new_car.y = location.spawn_location
    new_car.line = location.line_value
    location.car_occupying = new_car
    return new_car


def create_cloud() -> Cloud:
    scale = random.random()
    image = random.choice([CLOUD_1_IMAGE, CLOUD_2_IMAGE])
    speed = random.randint(10, 15)
    transparency = random.randint(50, 100)
    # scale = random.randint(10, 20) / 10
    model = image
    # model = pg.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
    model.set_alpha(transparency)
    image_width = model.get_width()
    starting_point = (WIDTH, random.randint(0, HEIGHT - model.get_height()))
    return Cloud(model, image_width, speed, starting_point)
    

