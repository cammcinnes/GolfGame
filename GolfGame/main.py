import pygame
from sys import exit

# create a display surface 
width = 800
height = 400

pygame.init
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Speed Golf")
clock = pygame.time.Clock()

# create a plain surface
# test_surface = pygame.Surface((800, 400))
# test_surface.fill('blue2')

# create a sky_surface background
sky_surface = pygame.image.load('graphics/sky.jpg')
sky_surface = pygame.transform.scale(sky_surface, (width, height))


while True:
    #check to see if the player has closed the window; close if true
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    screen.blit(sky_surface, (0, 0))
    # draw on the different elements
    # update all the elements
    pygame.display.update()
    clock.tick(60)
