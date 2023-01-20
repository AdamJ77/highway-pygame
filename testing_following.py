import numpy as np
import pygame as pg

WIDTH, HEIGHT = 1900, 1000
WIN = pg.display.set_mode((WIDTH, HEIGHT))  # maybe add pg.FULLSCREEN ?
AREA_SURFACE = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
rect_object = pg.Rect(50, 50, 10, 10)
pg.draw.rect(AREA_SURFACE, (255,255,255), rect_player, 1)

def main(*args, **kwargs):
    pg.init()
    clock = pg.time.Clock()
    run = True


    while run:
        pg.display.flip()
        clock.tick(40)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        
    pg.quit()


if __name__ == "__main__":
    main()