import math
import sys

import pygame as pg

pg.init()
screen = pg.display.set_mode((1900, 1080))

# Load car image
car_image = pg.transform.rotate(pg.image.load("images/player_car_new.png"), -90)

# Set car position
car_position = (1000, 500)

# Initialize rotation angle
angle = 0

# Offset from the center to the rear axis
rear_axis_offset = (car_image.get_width() / 2, car_image.get_height())

# Rotate car image around rear axis and draw it on the screen
def draw_car(angle):
    # Translate car image so that the rear axis is at the origin
    translated_car = pg.Surface((car_image.get_width(), car_image.get_height()), pg.SRCALPHA)
    translated_car.blit(car_image, (rear_axis_offset[0], rear_axis_offset[1]))
    
    # Rotate translated car image
    rotated_car = pg.transform.rotate(translated_car, angle)
    
    # Get rectangle of rotated car image
    rot_rect = rotated_car.get_rect(topleft=(rear_axis_offset[0], rear_axis_offset[1]))
    
    # Translate rotated car image back to its original position
    final_car = pg.Surface((rot_rect.width, rot_rect.height), pg.SRCALPHA)
    final_car.blit(rotated_car, (rear_axis_offset[0], rear_axis_offset[1]))
    
    # Draw final car image on screen
    screen.blit(final_car, (car_position[0]-rear_axis_offset[0], car_position[1]-rear_axis_offset[1]))

# ...
if __name__ == "__main__":
    # Main game loop
    while True:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        # Update angle
        angle += 0
        
        # Clear screen
        # screen.fill((255, 255, 255))
        
        # Draw car
        draw_car(angle)
        
        # Update screen
        pg.display.update()