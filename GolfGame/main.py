import pygame
import ball
from sys import exit

# create a display surface 
width = 800
height = 400

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Speed Golf")
clock = pygame.time.Clock()

# create a plain surface
# test_surface = pygame.Surface((800, 400))
# test_surface.fill('blue2')

# create a sky_surface background
sky_surface = pygame.image.load('graphics/sky.jpg')
sky_surface = pygame.transform.scale(sky_surface, (width, height))

#create a wood platform
wood_surface = pygame.Surface((600, 5))
wood_surface.fill('brown2')

#create a score board
#create font
test_font = pygame.font.Font('graphics/munro.ttf', 25)

text_surface = test_font.render('Score: ', True, 'White')

while True:
    #check to see if the player has closed the window; close if true
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # draw the surfaces on the display
    screen.blit(sky_surface, (0, 0))
    screen.blit(wood_surface, (100, 300))
    screen.blit(text_surface, (600, 5))

    # update all the elements
    pygame.display.update()
    clock.tick(60)
