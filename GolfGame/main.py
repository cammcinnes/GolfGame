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
sky_surface = pygame.transform.scale(sky_surface, (width, height)).convert()

#create a wood platform
wood_h = 5
wood_w = 600
wood = pygame.Surface((wood_w, wood_h)).convert()
wood.fill('brown2')
wood_rect = wood.get_rect(topleft = (100, 300))


#create a score board
test_font = pygame.font.Font('graphics/munro.ttf', 25)
text_surface = test_font.render('Score: ', True, 'White')

#create a golf ball object
golfBall = ball (100, 300 - 6, 5, (255,255,255))
x = 0
y = 0
time = 0
power = 0
angle = 0
shoot = False
collide = False

# function for drawing background, golf ball and intensity line
def redrawWindow():
    screen.blit(sky_surface, (0, 0))
    screen.blit(wood, wood_rect)
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

# Check for collision of ball with surface
def collision(rect, center_x, center_y, radius):
    rleft = rect.x
    rtop = rect.y
    rright = rect.right
    rbottom =  rect.bottom

    # bounding box of the circle
    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius

    # trivial reject if bounding boxes do not intersect
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rleft, rleft+width):
        for y in (rtop, rtop+height):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True  # overlaid

    return False  # no collision detected

while True:

    #actions if ball is shooting or not
    # TODO: Make golf ball stay on wood when it collides; fix that at high speed golf ball goes through platform; make golf ball switch directions when hits wood
    # TODO: Make golf ball bounce
    if shoot:
        if  golfBall.y < height - golfBall.radius:
            hit = collision(wood_rect, golfBall.x, golfBall.y, golfBall.radius)
            # TODO: create the bounce of ball
            if hit:
                if golfBall.y > wood_rect.top:
                    golfBall.y = golfBall.y - golfBall.radius
                    shoot = False
                else:
                    golfBall.y = golfBall.y + golfBall.radius
                    shoot = False

            else:
                time += 0.2
                po = ball.ballPath(x, y, power, angle, time, collide)
                golfBall.x = po[0]
                golfBall.y = po[1]
            
        else:
            golfBall.y = height - (golfBall.radius + 1)
            shoot = False


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
                collide = False


    # update all the elements
    redrawWindow()
    clock.tick(60)
