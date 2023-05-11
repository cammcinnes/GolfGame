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

#create hole
hole_surface = pygame.image.load('graphics/flag.png')
hole_surface = pygame.transform.scale(hole_surface,(90, 100)).convert_alpha()

#create an invisible rectangle for scoring 
s = pygame.Surface((1,5)) 
s_rect = s.get_rect(topleft = (637, 300))
s.set_alpha(128)               
s.fill((255,255,255))           
    
#create font
score_font = pygame.font.Font('graphics/munro.ttf', 25)
end_font = pygame.font.Font('graphics/munro.ttf', 50)


#create a golf ball object
golfBall = ball (100, 300 - 7, 5, (255,255,255))
x = 0
y = 0
velx = 0
vely = 0
time = 0
power = 0
angle = 0
shoot = False
score = 0

# function for drawing background, golf ball and intensity line
def redrawWindow():
    text_surface = score_font.render('Strokes:' + str(score), True, 'White')
    screen.blit(sky_surface, (0, 0))
    screen.blit(s, (637,300))
    screen.blit(wood, wood_rect)
    screen.blit(text_surface, (675, 5))
    
    golfBall.draw(screen)
    screen.blit(hole_surface, (560, 203))
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
    if shoot:
        if  golfBall.y < height - golfBall.radius:
            hit = collision(wood_rect, golfBall.x, golfBall.y, golfBall.radius)
            #TODO: fix bug when hits bottom of wood
            if hit:
                time = 0
                x = golfBall.x
                y = golfBall.y - 6
                velx = velx * 0.75
                vely = vely * 0.5 
                po = ball.ballPath(x, y, velx, vely, time)
                golfBall.x = po[0]
                golfBall.y = po[1]
                # Under a speed of 1 the stroke will stop
                if velx < 1 and velx > -1:
                    shoot = False
            
            else:
                time += 0.2
                po = ball.ballPath(x, y, velx, vely, time)
                golfBall.x = po[0]
                golfBall.y = po[1]
            
        else:
            golfBall.x = 100
            golfBall.y = 300 - 7
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
                score += 1
                x = golfBall.x
                y = golfBall.y
                angle = findAngle(pos)
                power =  math.sqrt((line[1][1] - line [0][1])**2 + (line[1][0] - line[0][0])**2) / 8
                velx = math.cos(angle) * power
                vely = math.sin(angle) * power
                time = 0

    # ends game if ball goes in hole
    sunk = collision(s_rect,  golfBall.x, golfBall.y, golfBall.radius)
    if sunk:
        break
        
    # update all the elements
    redrawWindow()
    clock.tick(60)


# End game title
while True: 
    text_surface = end_font.render('Strokes:' + str(score), True, 'White')
    text_rect = text_surface.get_rect(center = (width / 2, height / 2))
    screen.blit(sky_surface, (0, 0))
    screen.blit(s, (630,300))
    screen.blit(wood, wood_rect)
    screen.blit(text_surface, text_rect)
    
    golfBall.draw(screen)
    screen.blit(hole_surface, (560, 203))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    clock.tick(60)