import numpy as np
import pygame as pg

from class_player import Player

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
        # print("upper")
        return upper
    elif check_collision_with_player(player.act_rect, lower):
        # print("lower")
        return lower
    else:
        # print("False")
        return False


def collisions(
    player: Player,
    traffic_cars: np.array,
    upper: pg.Rect,
    lower: pg.Rect
    )-> None:
    is_collision = check_boundaries_collision(player, upper, lower)
    # print(is_collision)
    if is_collision:
        boundary = "upper" if is_collision is upper else "lower"
        player.rotate_back(boundary)
    # check_collision_cars(player, traffic_cars)
