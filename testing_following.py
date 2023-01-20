import math

import numpy as np
import pygame as pg

WIDTH, HEIGHT = 1900, 1000
WIN = pg.display.set_mode((WIDTH, HEIGHT))  # maybe add pg.FULLSCREEN ?
AREA_SURFACE = pg.Surface((WIDTH, HEIGHT))
empty = pg.Color(0,0,0,0)
# background = pg.Rect(0,0, WIDTH, HEIGHT)
# rect_object = pg.Rect(50, 50, 10, 10)
# pg.draw.rect(AREA_SURFACE, (255, 255, 255), background)
# pg.draw.rect(AREA_SURFACE, (127, 255, 240), rect_object, 1)
obstacle_1 = pg.Rect(500, 250, 200, 100)

X, Y = 50, 50
SPEED = 4

class Followed:
    def __init__(self) -> None:
        self.x = X
        self.y = Y

    def move_right(self):
        self.x += SPEED
    
    def move_left(self):
        self.x -= SPEED

    def move_up(self):
        self.y -= SPEED

    def move_down(self):
        self.y += SPEED

    def draw(self):
        return pg.Rect(self.x, self.y, 5, 5)


SPEED_ENEMY = 3

class Follower:
    def __init__(self) -> None:
        self.x = 500
        self.y = 500
        
    def y_dist(self, player: Followed) -> int:
        return player.y - self.y 
    
    def x_dist(self, player: Followed) -> int:
        return player.x - self.x

    def distance(self, player: Followed):
        return math.sqrt((self.x_dist(player) ** 2) + (self.y_dist(player) ** 2))

    def cos_x(self, player):
        return self.x_dist(player) / self.distance(player)

    def cos_y(self, player):
        return self.y_dist(player) / self.distance(player)

    def follow(self, player: Followed):
        self.x += SPEED_ENEMY * self.cos_x(player)
        self.y += SPEED_ENEMY * self.cos_y(player)
    
    def direction(self, player) -> tuple[float, float]:
        return (self.x_dist(player), self.y_dist(player))
        
    
    
    def draw(self):
        return pg.Rect(self.x, self.y, 5, 5)

def main(*args, **kwargs):
    pg.init()
    clock = pg.time.Clock()
    run = True
    player = Followed()
    enemy = Follower()
    pg.draw.rect(AREA_SURFACE, (40, 255, 0), obstacle_1, 4)

    while run:
        pg.display.flip()
        pg.draw.rect(AREA_SURFACE, (127, 255, 240), player.draw(), 5)
        pg.draw.rect(AREA_SURFACE, (255, 125, 124), enemy.draw(), 5)
        print(enemy.direction(player))
        # print(enemy.distance(player))
        # WIN.fill((0, 0, 0))
        clock.tick(40)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_w]:
            player.move_up()
        if keys_pressed[pg.K_s]:
            player.move_down()
        if keys_pressed[pg.K_a]:
            player.move_left()
        if keys_pressed[pg.K_d]:
            player.move_right()
        if keys_pressed[pg.K_c]:
            AREA_SURFACE.fill(empty)
            pg.draw.rect(AREA_SURFACE, (40, 255, 0), obstacle_1, 4)

        if keys_pressed[pg.K_SPACE]:
            enemy.follow(player)
        
        if enemy.draw().colliderect(obstacle_1):
            print("Yes")
        # else:
        #     enemy.follow(player)
        # AREA_SURFACE = pg.Surface((WIDTH, HEIGHT))

        WIN.blit(AREA_SURFACE, (0,0))
        

  
        # pg.display.update()
        
    pg.quit()


if __name__ == "__main__":
    main()