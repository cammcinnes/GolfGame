import pygame
import math

class ball(object):

    # Initializes the ball object
    def __init__(self, x, y, radius, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = colour
    
    # Draws 2 circles as the ball one white and one black for the outline
    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius - 1)

    # sets velocity and positon of ball after being hit
    @staticmethod
    def ballPath (startX, startY, power, angle, time):
        vX = math.cos(angle) * power
        vY = math.sin(angle) * power

        distX = vX * time
        distY = vY * time + ((-4.9 * time**2) / 2)

        newX = round(distX + startX)
        newY = round(startY - distY)

        return (newX, newY)

    
