import pygame as pg
import random
from classes_other import ColorCar, Location, Car
from config import (
    WIN,
    WIDTH,
    HEIGHT,
    HIGHWAY_IMAGE,
    HIGHWAY_IMAGE_WIDTH,
    SCROLL_SPEED,
    LAMPS_IMAGE,
    LAMPS_WIDTH,
    bg_tiles,
    lamp_tiles,
    CAR_IMAGE_GREEN,
    CAR_IMAGE_RED,
    CAR_IMAGE_PURPLE,
    CAR_HEIGHT,
    CAR_WIDTH,
    MUSCLE_CAR_IMAGE_YELLOW,
    MUSCLE_CAR_HEIGHT,
    MUSCLE_CAR_WIDTH,
    SEDAN_CAR_IMAGE_BROWN,
    SEDAN_CAR_HEIGHT,
    SEDAN_CAR_WIDTH,
    SPAWN_LOCATIONS,
    DRIVING_AREA_SIZE
)


def get_random_colors() -> list:
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


def create_color_cars_dict():
    Car_Colors = {}
    Car_Colors[ColorCar.CAR_GREEN] = [CAR_IMAGE_GREEN, (CAR_WIDTH, CAR_HEIGHT)]
    Car_Colors[ColorCar.CAR_RED] = [CAR_IMAGE_RED, ((CAR_WIDTH, CAR_HEIGHT))]
    Car_Colors[ColorCar.CAR_PURPLE] = [CAR_IMAGE_PURPLE, (CAR_WIDTH, CAR_HEIGHT)]
    Car_Colors[ColorCar.MUSCLE_CAR_YELLOW] = [MUSCLE_CAR_IMAGE_YELLOW, (MUSCLE_CAR_WIDTH, MUSCLE_CAR_HEIGHT)]
    Car_Colors[ColorCar.SEDAN_BROWN] = [SEDAN_CAR_IMAGE_BROWN, (SEDAN_CAR_WIDTH, SEDAN_CAR_HEIGHT)]
    return Car_Colors


def create_spawning_locations():
    loc1 = Location.location(SPAWN_LOCATIONS[0], 1)
    loc2 = Location.location(SPAWN_LOCATIONS[1], 2)
    loc3 = Location.location(SPAWN_LOCATIONS[2], 3)
    return loc1, loc2, loc3


def create_boundaries() -> tuple:
    upper = pg.Rect(0, 0, WIDTH, DRIVING_AREA_SIZE[0] + 25)
    lower = pg.Rect(0, HEIGHT - 170, WIDTH, 100)
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

