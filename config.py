import pygame as pg
import math


# GAME
WIDTH, HEIGHT = 1900, 1000
WIN = pg.display.set_mode((WIDTH, HEIGHT))  # maybe add pg.FULLSCREEN ?
DRIVING_AREA_SIZE = (HEIGHT//5 - 50, HEIGHT - 160)

# BLANK HIGHWAY AREA (TO TEST RECT)
AREA_SURFACE = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)

# PLAYER
PLAYER_IMAGE = pg.transform.rotate(pg.image.load("images/player_car_new.png"), -90)
PLAYER_WIDTH, PLAYER_HEIGHT = PLAYER_IMAGE.get_width(), PLAYER_IMAGE.get_height()

SPEED_PLAYER = 0
MAX_SPEED_PLAYER = 20
ACELERATION = 0.5
SPEED_CAR_SIDEWAYS = 5
FRICTION_DECEL = 0.5     # decelaration caused by friction and no acceleration
BRAKE_DECEL = 10

ANGLE_ROTATE = 3
ROTATION_BACK_SPEED_ANGLE = 2
MAX_ANGLE = 45

#BRAKE LIGHTS
BRAKE_LIGHTS = pg.transform.rotate(pg.image.load("images/lights_on.png"), -90)


# BACKGROUND
HIGHWAY_IMAGE = pg.transform.scale(pg.image.load("images/highway2.png"), (WIDTH, HEIGHT))
HIGHWAY_IMAGE_WIDTH = HIGHWAY_IMAGE.get_width()
# BACKGROUND SCROLL CONFIG
bg_tiles = math.ceil((WIDTH / HIGHWAY_IMAGE_WIDTH)) + 2    # maybe 1
SCROLL_SPEED = 5


# LAMP SCROLL
# LAMP_WIDTH = 35
# LAMP_HEIGHT = 173
# DISTANCE_BETWEEN_LAMPS = 500

LAMPS_IMAGE = pg.image.load("images/row_lamps.png")
LAMPS_WIDTH = LAMPS_IMAGE.get_width()
lamp_tiles = math.ceil((WIDTH / LAMPS_WIDTH)) + 2
print(lamp_tiles)


# CARS
CAR_IMAGE_RED = pg.transform.rotate(pg.image.load("images/car1.png"), 90)
CAR_IMAGE_GREEN = pg.transform.rotate(pg.image.load("images/car2.png"), 90)
CAR_IMAGE_PURPLE = pg.transform.rotate(pg.image.load("images/car3.png"), 90)
CAR_WIDTH = CAR_IMAGE_RED.get_width()
CAR_HEIGHT = CAR_IMAGE_RED.get_height()

# TRUCK
TRUCK_WIDTH, TRUCK_HEIGHT = 161, 534
TRUCK_IMAGE = pg.transform.rotate(pg.transform.scale(pg.image.load("images/truck.png"), (TRUCK_WIDTH, TRUCK_HEIGHT)), -90)
TRUCK_WIDTH = TRUCK_IMAGE.get_width()
TRUCK_HEIGHT = TRUCK_IMAGE.get_height()



# OTHER OBJECTS

#SPAWN LOCATIONS
SPAWN_LOC_1 = (HIGHWAY_IMAGE_WIDTH - CAR_WIDTH, DRIVING_AREA_SIZE[0] + 80)
SPAWN_LOC_2 = (HIGHWAY_IMAGE_WIDTH - CAR_WIDTH, DRIVING_AREA_SIZE[0] + 300)
SPAWN_LOC_3 = (HIGHWAY_IMAGE_WIDTH - CAR_WIDTH, DRIVING_AREA_SIZE[0] + 520)
SPAWN_LOCATIONS = [SPAWN_LOC_1, SPAWN_LOC_2, SPAWN_LOC_3]














