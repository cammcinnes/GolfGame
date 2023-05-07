import pygame
import math
from ball import ball
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

# Global Variables:

# create a sky_surface background
sky_surface = pygame.image.load('graphics/sky.jpg')
sky_surface = pygame.transform.scale(sky_surface, (width, height))

#create a wood platform
wood_surface = pygame.Surface((600, 5))
wood_surface.fill('brown2')

#create a score board
test_font = pygame.font.Font('graphics/munro.ttf', 25)
text_surface = test_font.render('Score: ', True, 'White')

#create a golf ball object
golfBall = ball (400, height - 6, 5, (255,255,255))
x = 0
y = 0
time = 0
power = 0
angle = 0
shoot = False

# function for drawing background, golf ball and intensity line
def redrawWindow():
    screen.blit(sky_surface, (0, 0))
    screen.blit(wood_surface, (100, 300))
    screen.blit(text_surface, (600, 5))

    golfBall.draw(screen)
    pygame.draw.line(screen, (255, 255, 255), line[0], line[1])

    pygame.display.update()

# function for finding the angle of projectile based on position of ball and mouse
def findAngle(pos):
    sX = golfBall.x
    sY = golfBall.y

    try:
        angle = math.atan(((sY - pos[1]) / (sX - pos[0])))
    except:
        angle = math.pi / 2
    
    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (2 * math.pi) - angle
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    
    return angle
    

while True:

    #actions if ball is shooting or not
    if shoot:
        if golfBall.y < 400 - golfBall.radius:
            time += 0.2
            po = ball.ballPath(x, y, power, angle, time)
            golfBall.x = po[0]
            golfBall.y = po[1]
        else:
             shoot = False
             golfBall.y = height - (golfBall.radius + 1)


    # find position for line from ball to cursor
    pos = pygame.mouse.get_pos()
    line = [(golfBall.x, golfBall.y), pos]

    # check to see if the player has closed the window; close if true
    # check to see if player is shooting the ball, set intials
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if shoot == False:
                shoot = True
                x = golfBall.x
                y = golfBall.y
                time = 0
                power =  math.sqrt((line[1][1] - line [0][1])**2 + (line[1][0] - line[0][0])**2) / 8
                angle = findAngle(pos)


    # update all the elements
    redrawWindow()
    clock.tick(60)
