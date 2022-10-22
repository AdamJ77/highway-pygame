
from cProfile import run
import pygame as pg

pg.init()
WIN = pg.display.set_mode((1920, 1080))
HIGHWAY_IMAGE = pg.transform.scale(pg.image.load("images/highway.png"), (1920, 1080))
clock = pg.time.Clock()

PLAYER_IMAGE = pg.transform.rotate(pg.image.load("images/player_car_new.png"), -90)
running = True
angle = 0
pos = (100, 100)
value = 6
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    clock.tick(60)
    ROTATED_PLAYER = pg.transform.rotate(PLAYER_IMAGE, angle)
    angle += 1
    WIN.blit(HIGHWAY_IMAGE, (0, 0))
    WIN.blit(ROTATED_PLAYER, pos)
    pg.display.update()
pg.quit()