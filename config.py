import pygame as pg
import math



# GAME
WIDTH, HEIGHT = 1900, 1000
WIN = pg.display.set_mode((WIDTH, HEIGHT))
DRIVING_AREA_SIZE = (HEIGHT//5, 4*HEIGHT//5)



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



# TRUCK
TRUCK_WIDTH, TRUCK_HEIGHT = 161, 534
TRUCK_IMAGE = pg.transform.rotate(pg.transform.scale(pg.image.load("images/truck.png"), (TRUCK_WIDTH, TRUCK_HEIGHT)), -90)




# OTHER OBJECTS

















