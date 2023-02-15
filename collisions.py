import random

import numpy as np
import pygame as pg

from class_player import Player
from classes_other import Chopper
from config import (COLLISION_TOLERANCE, HEIGHT, POLICE_CHOPPER_HEIGHT,
                    POLICE_CHOPPER_WIDTH, WIDTH)

# PHYSICS COLLISIONs

def check_collision_with_player(
    player_rect: pg.Rect,
    object: pg.Rect
    ) -> bool:
    """
    Return True if player collided with object else False
    """
    return True if player_rect.colliderect(object) else False

# CHECK TRAFFIC COLLISION
def check_collision_cars(
    player: Player,
    player_rect: pg.Rect,
    traffic_cars: np.array
    ) -> bool:
    """
    Check if player's rect collided with other car's rect
    """
    # rect_player = player.get_rect()

    for car in traffic_cars:
        rect_car = car.get_rect()
        if player_rect.colliderect(rect_car):
            check_side_collision(player, player_rect, rect_car)
    return


def check_side_collision(
    player: Player,
    rect_player: pg.Rect,
    rect_car: pg.Rect,
    ):
    """Check from on which side was collision"""
    if abs(rect_player.bottom - rect_car.top) < COLLISION_TOLERANCE:
        print("bottom collision", player.speed)
        if player.rotation < 0:
            player.rotation += 10
        # player.rotate_back("bottom")

    if abs(rect_player.top - rect_car.bottom) < COLLISION_TOLERANCE + player.speed * player.get_tan_abs(player.rotation):
        print("top collision", player.speed)
        if player.rotation > 0:
            player.rotation -= 10
        # player.rotate_back("top")

    if abs(rect_player.right - rect_car.left) < COLLISION_TOLERANCE + player.speed:
        print("right collision", player.speed, rect_player.right, rect_car.left)
        player.x = rect_car.x - player.width
        player.speed = 0
    
    if abs(rect_player.left - rect_car.right) < COLLISION_TOLERANCE + player.speed:
        player.x = rect_car.right + 10
        player.speed = 0
        print("left collision", player.speed)

    return


def check_boundaries_collision(
    player_rect: pg.Rect,
    upper: pg.Rect,
    lower: pg.Rect
    ):
    """Return True if player collided with upper or lower boundary"""

    if check_collision_with_player(player_rect, upper):
        # print("upper")
        return upper
    elif check_collision_with_player(player_rect, lower):
        # print("lower")
        return lower
    else:
        # print("False")
        return False


def collisions(
    player: Player,
    traffic_cars: np.array,
    upper: pg.Rect,
    lower: pg.Rect,
    chopper: Chopper
    )-> None:
    player_rect = player.get_rect()

    # BOUNDARIES
    if is_collision:= check_boundaries_collision(player_rect, upper, lower):
        boundary = "upper" if is_collision is upper else "lower"
        player.rotate_back(boundary)

    # TRAFFIC
    check_collision_cars(player, player_rect, traffic_cars)

    # CHOPPER
    if check_collision_with_player(player_rect, chopper.get_rect()) and not chopper.isMoving:
        chopper.isMoving = True
        rand_x, rand_y = create_chopper_direction()
        chopper.destination = (rand_x, rand_y)


def create_chopper_direction() -> tuple[int]:
    x = random.randint(1, WIDTH - POLICE_CHOPPER_WIDTH)
    y = random.randint(1, HEIGHT - POLICE_CHOPPER_HEIGHT)
    return x,y