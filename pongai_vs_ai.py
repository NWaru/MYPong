
import pygame
import math
import random

# Define some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

# Set the width and height of the screen [width, height]
WINDOWWIDTH, WINDOWLENGTH = 1200, 700
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWLENGTH))

pygame.display.set_caption("Bouncing Square")
pygame.mouse.set_visible(0)

# Loop until the user clicks the close button. 
done = False
ai_complete = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

topborder = False
bottomborder = False

# Starting position of rectangle
rect_x = 50
rect_y = 50
# Speed and direction of rectangle
rect_change_x = 7
rect_change_y = 7

speed_count = 0

field = pygame.Rect((0,0,WINDOWWIDTH,WINDOWLENGTH))

class Paddle():
    """paddles on screen"""
    def __init__(self):
        self.colour = WHITE
        self.up_change = -9
        self.down_change = 9
        self.length = 670 / 3 - 70
        self.width = 18
        self.x_pos = 0
        self.y_pos = 0
        self.rectangle = pygame.Rect([self.x_pos, self.y_pos,
                                               self.width, self.length])

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rectangle)

computer = Paddle()
computer.rectangle[0] = 30
computer.rectangle[1] = 200
computer.up_change = -9
computer.down_change = 9

computer2 = Paddle()
computer2.rectangle[0] = 1155
computer2.rectangle[1] = 200

pressed_up = False
pressed_down = False

at_top = False
at_bottom = False

move_up = False
move_down = False

ball = pygame.Rect([rect_x,rect_y,15,15])

thinking = False
thinking2 = False

comp1_score = 0
comp2_score = 0

def print_score():
    global comp1_score
    global comp2_score 

    font = pygame.font.SysFont('Courier New', 50, False, False)
    score1 = font.render(str(comp1_score), True, WHITE)
    score2 = font.render(str(comp2_score), True, WHITE)

    screen.blit(score1, [325, 45])
    screen.blit(score2, [875, 45])

def AI():
    if computer.rectangle.centery >= ball.centery:
        return computer.up_change
    elif computer.rectangle.centery < ball.centery:
        return computer.down_change
    
def AI2():
    if computer2.rectangle.centery >= ball.centery:
        return computer2.up_change
    elif computer2.rectangle.centery < ball.centery:
        return computer2.down_change

while not done:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True #Flags completeness and exits loop
        
    if thinking:
        computer.rectangle.centery += AI()

    if thinking2:
        computer2.rectangle.centery += AI2()
    
    screen.fill(BLACK)
  
    # Draws rectangle
    pygame.draw.rect(screen, WHITE,ball)

    computer2.draw(screen)
    computer.draw(screen)
    pygame.draw.rect(screen, WHITE, field, 20)

    pygame.draw.line(screen, WHITE, (WINDOWWIDTH/2, 0), (WINDOWWIDTH/2, 700)) 
    
    # Moves rectangle starting point
    ball[0] += rect_change_x
    ball[1] += rect_change_y

    #Bounce rectangle
    if ball[1] > 665 or ball[1] < 20:
        rect_change_y = rect_change_y * -1
    #if ball[0] > 1165 or ball[0] < 20:
    #    rect_change_x = rect_change_x * -1

    if computer2.rectangle[1] < 21:
        computer2.up_change = 0
        bottomborder = False
        topborder = True
    elif computer2.rectangle[1] > 700 - 20 - computer2.length:
        computer2.down_change = 0
        topborder = False
        bottomborder = True
    else:
        computer2.up_change = -9
        computer2.down_change = 9
        topborder = False
        bottomborder = False

    if computer2.rectangle.colliderect(ball):# and ball.top > computer2.rectangle.top and ball.bottom < computer2.rectangle.bottom: 
        rect_change_x = rect_change_x * -1
        thinking = True
        thinking2 = False

        #if rect_change_x < 16:
        rect_change_x += -2
        



    if computer.rectangle[1] < 21:
        computer.up_change = 0
        at_bottom = False
        at_top = True
    elif computer.rectangle[1] > 700 - 20 - computer.length:
        computer.down_change = 0
        at_top = False
        at_bottom = True
    else:
        computer.up_change = -9
        computer.down_change = 9
        at_top = False
        at_bottom = False

    if computer.rectangle.colliderect(ball): # and ball.top > computer.rectangle.top and ball.bottom < computer.rectangle.bottom:
        rect_change_x = rect_change_x * -1
        thinking = False
        thinking2 = True
        
        #if rect_change_x < -16:
        rect_change_x += 2
    
    if ball[0] > 1300:
        ball[0] = 600
        ball[1] = random.randrange(21,664)
        comp1_score += 1
        rect_change_x = -7
        thinking = True
        thinking2 = False

    if ball[0] < -99:
        ball[0] = 600
        ball[1] = random.randrange(21,664)
        comp2_score += 1
        rect_change_x = 7
        thinking = False
        thinking2 = True

    print_score()    
    pygame.display.flip()

    # --- Limit to 60 frames per second 
    clock.tick(60)

# Close the window and quit.
pygame.quit()
