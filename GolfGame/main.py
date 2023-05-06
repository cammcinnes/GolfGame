import pygame
from sys import exit

# creating a display surface 
pygame.init
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Speed Golf")

while True:
    #check to see if the player has closed the window; close if true
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        
    # draw on the different elements
    # update all the elements
    pygame.display.update()
