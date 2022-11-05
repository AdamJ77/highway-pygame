import pygame
import pygame.font

pygame.init()
size = (400,400)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# def blitRotate(surf, image, pos, originPos, angle):

#     # calcaulate the axis aligned bounding box of the rotated image
#     w, h       = image.get_size()
#     box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
#     box_rotate = [p.rotate(angle) for p in box]
#     min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
#     max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

#     # calculate the translation of the pivot
#     pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
#     pivot_rotate = pivot.rotate(angle)
#     pivot_move   = pivot_rotate - pivot

#     # calculate the upper left origin of the rotated image
#     origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

#     # get a rotated image
#     rotated_image = pygame.transform.rotate(image, angle)

#     # rotate and blit the image
#     surf.blit(rotated_image, origin)

#     # draw rectangle around the image
#     pygame.draw.rect (surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)

# font = pygame.font.SysFont('Times New Roman', 50)
# text = font.render('image', False, (255, 255, 0))
# image = pygame.Surface((text.get_width()+1, text.get_height()+1))
# pygame.draw.rect(image, (0, 0, 255), (1, 1, *text.get_size()))
# image.blit(text, (1, 1))
# w, h = image.get_size()

sword_surface = pygame.image.load("images/player_car_new.png")

angle = 1  # In Degrees
pivot = pygame.Vector2(100, 100)  # You can use any X and Y here.
# Create the surface

sword_rect = sword_surface.get_rect()
# Create the rotation vector
rotation_vector = sword_surface.get_rect().center - pivot
angle = 0
done = False
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                done = True

    # Rotate the rotation vector, and store as a new variable
    rotated_vector = rotation_vector.rotate(angle)
    # Rotate the surface
    rotated_sword_surface = pygame.transform.rotate(sword_surface, angle)
    # Relocate the surface
    relocation_vector = rotated_vector - rotation_vector
    sword_rect.center += relocation_vector
    self.image = sword_surface
    self.rect = sword_rect
    angle += 1

pygame.quit()
