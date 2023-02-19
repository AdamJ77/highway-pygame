import math

import numpy as np
import pygame as pg

from environment import VelocityGUI

WIDTH, HEIGHT = 1900, 1080
WIN = pg.display.set_mode((WIDTH, HEIGHT))  # maybe add pg.FULLSCREEN ?
AREA_SURFACE = pg.Surface((WIDTH, HEIGHT))
empty = pg.Color(0,0,0,0)
# background = pg.Rect(0,0, WIDTH, HEIGHT)
# rect_object = pg.Rect(50, 50, 10, 10)
# pg.draw.rect(AREA_SURFACE, (255, 255, 255), background)
# pg.draw.rect(AREA_SURFACE, (127, 255, 240), rect_object, 1)
OBSTACLE_1_INIT_X = 500
OBSTACLE_1_INIT_Y = 250

OBSTACLE_1_WIDTH = 200
OBSTACLE_1_HEIGHT = 100


X, Y = 50, 50
SPEED = 2

class Obstacle:
    def __init__(self) -> None:
        self.rect = pg.Rect(OBSTACLE_1_INIT_X, OBSTACLE_1_INIT_Y, OBSTACLE_1_WIDTH, OBSTACLE_1_HEIGHT)
        self.left_top = (OBSTACLE_1_INIT_X, OBSTACLE_1_INIT_Y)
        self.right_top = (OBSTACLE_1_INIT_X + OBSTACLE_1_WIDTH, OBSTACLE_1_INIT_Y)
        self.left_down = (OBSTACLE_1_INIT_X, OBSTACLE_1_INIT_Y + OBSTACLE_1_HEIGHT)
        self.right_down = (OBSTACLE_1_INIT_X + OBSTACLE_1_WIDTH, OBSTACLE_1_INIT_Y + OBSTACLE_1_HEIGHT)
    
    def get_points(self):
        return [self.left_top, self.right_top, self.left_down, self.right_down]

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

    def follow(self, player: Followed):
        self.x += SPEED_ENEMY * cos_x((player.x, player.y), (self.x, self.y))
        self.y += SPEED_ENEMY * cos_y((player.x, player.y), (self.x, self.y))

    def follow_obstacle_point(self, point: tuple[int]):
        self.x += SPEED_ENEMY * cos_x(point, (self.x, self.y))
        self.y += SPEED_ENEMY * cos_y(point, (self.x, self.y))
    
    def direction(self, player) -> tuple[float, float]:
        return (x_dist(player.x, self.x), y_dist(player.y, self.y))
        
    def draw(self):
        return pg.Rect(self.x, self.y, 5, 5)



def distance(point1, point2) -> float:
    return math.sqrt(((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2))

def x_dist(point1_x: int, point2_x: int) -> int:
    return point1_x - point2_x

def y_dist(point1_y: int, point2_y: int) -> int:
    return point1_y - point2_y

def cos_x(point1: tuple[int], point2: tuple[int]) -> float:
    return x_dist(point1[0], point2[0]) / distance(point1, point2)

def cos_y(point1: tuple[int], point2: tuple[int]) -> float:
    return y_dist(point1[1], point2[1]) / distance(point1, point2)  



def main(*args, **kwargs):

    pg.init()
    clock = pg.time.Clock()
    run = True
    player = Followed()
    enemy = Follower()
    obstacle_1 = Obstacle()
    velocity_gui = VelocityGUI(WIN, 10)
    pg.draw.rect(AREA_SURFACE, (40, 255, 0), obstacle_1.rect, 4)

    while run:
        pg.display.flip()
        pg.draw.rect(AREA_SURFACE, (127, 255, 240), player.draw(), 5)
        pg.draw.rect(AREA_SURFACE, (255, 125, 124), enemy.draw(), 5)
        # print(enemy.direction(player))
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
            if obstacle_1.rect.clipline(enemy.x, enemy.y, player.x, player.y):
                distances = [(distance((enemy.x, enemy.y), point) + distance((player.x, player.y), point), point, i) for i, point in enumerate(obstacle_1.get_points())]
               
                distances = sorted(distances, key= lambda x: x[0])
                best_d = distances[0]
                # best_d = np.argmin(distances)
                
                # if obstacle_1.rect.clipline(enemy.x, enemy.y, best_d[1][0], best_d[1][1]):
                    # best_d = distances[1]
            
                if best_d[2] == 0:
                    enemy.follow_obstacle_point(obstacle_1.left_top)    
                elif best_d[2] == 1:
                    enemy.follow_obstacle_point(obstacle_1.right_top) 
                elif best_d[2] == 2:
                    enemy.follow_obstacle_point(obstacle_1.left_down)
                else:
                    enemy.follow_obstacle_point(obstacle_1.right_down)
            else:
                enemy.follow(player)


        WIN.blit(AREA_SURFACE, (0,0))
        velocity_gui.display_velocity(10.0)


  
        # pg.display.update()
        
    pg.quit()


if __name__ == "__main__":
    main()