import random
from config import (
    WIN,
    HIGHWAY_IMAGE,
    HIGHWAY_IMAGE_WIDTH,
    SCROLL_SPEED,
    LAMPS_IMAGE,
    LAMPS_WIDTH,
    bg_tiles,
    lamp_tiles
)

def get_random_colors() -> list:
    """Return RGB list color"""
    return [random.randint(0, 255) for _ in range(3)]



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
