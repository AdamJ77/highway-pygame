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



