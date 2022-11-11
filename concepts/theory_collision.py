"""
have to draw rectangles around images
Rect1.colliderect(Rect2)    -> true if collision

Rect1.collidepoint(x,y) -> checking if x,y of one point on a rect is colliding with another rect

 best collision detection
 1. check for any collision with colliderect
 2. if so do calculation for each side of the rectangle we collide with
    CHECK WHICH SIDE WAS COLLIDED
    e.g. bottom_first_rect - top_second_rect = about 0 -> bottom collision of the first rect
         right_             - left           = aboout 0 -> right collsion


"""
import random

class Location:
   #  spawn_location = None

    def __init__(self, spawn_loc, isOccupied=False) -> None:
        self.spawn_location = spawn_loc
        self.isOccupied = isOccupied

    @classmethod
    def location(cls, location):
        return cls(location)


if __name__ == "__main__":


   testing = (0, 2, 3)
   my_choice = random.choice(testing)
   print(my_choice)