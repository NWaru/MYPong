
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
new_speed = rect_change_x



field = pygame.Rect((0,0,WINDOWWIDTH,WINDOWLENGTH))

class Paddle():
    """paddles on screen"""
    def __init__(self):
        self.colour = WHITE
        self.up_change = -10
        self.down_change = 10
        self.length = 670 / 3 - 80
        self.width = 15
        self.x_pos = 0
        self.y_pos = 0
        self.rectangle = pygame.Rect([self.x_pos, self.y_pos,
                                               self.width, self.length])

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rectangle)

computer = Paddle()
computer.rectangle[0] = 30
computer.rectangle[1] = 200
computer.up_change = -7
computer.down_change = 7

player = Paddle()
player.rectangle[0] = 1155
player.rectangle[1] = 200

pressed_up = False
pressed_down = False

at_top = False
at_bottom = False

move_up = False
move_down = False

ball = pygame.Rect([rect_x,rect_y,15,15])

thinking = False

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

    # elif rect_change_x == 7:
        # if computer.rectangle[1] != 200:
        # computer.rectanle[1] += 25

    #if move_up:
        #computer.rectangle[1] -= computer.change
    #if move_down:
        #computer.rectangle[1] += computer.change

    
    # -------- Main Program Loop --------
while not done:
     # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicke close
            done = True #Flags completeness and exits loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not topborder:
                pressed_up = True
                player.up_change = -10
            if event.key == pygame.K_DOWN and not bottomborder: 
                pressed_down = True
                player.down_change = 10
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP: 
                pressed_up = False
            if event.key == pygame.K_DOWN:
                pressed_down = False
                
    if pressed_up:
        player.rectangle[1] += player.up_change
    if pressed_down:
        player.rectangle[1] += player.down_change
        
    if thinking:
        computer.rectangle.centery += AI()  
    

           
    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
  
    # --- Drawing code should go here 
    # Draw on the screen a green line from (0,) to (100, 100)
    # that is 5 pixels wide.

    # Draws rectangle
    pygame.draw.rect(screen, WHITE,ball)
    # Red rectangle inside white
    # pygame.draw.rect(screen, RED, [rect_x + 10, rect_y + 10, 30, 30])

    player.draw(screen)
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

    if player.rectangle[1] < 21:
        player.up_change = 0
        bottomborder = False
        topborder = True
    elif player.rectangle[1] > 700 - 20 - player.length:
        player.down_change = 0
        topborder = False
        bottomborder = True
    else:
        player.up_change = -10
        player.down_change = 10
        topborder = False
        bottomborder = False

    if ball.colliderect(player.rectangle) and ball.left <= player.rectangle.right:
        rect_change_x = rect_change_x * -1
        speed_count += 1
        thinking = True
        rect_change_x += -0.5



    if computer.rectangle[1] < 21:
        computer.up_change = 0
        at_bottom = False
        at_top = True
    elif computer.rectangle[1] > 700 - 20 - computer.length:
        computer.down_change = 0
        at_top = False
        at_bottom = True
    else:
        computer.up_change = -7
        computer.down_change = 7
        at_top = False
        at_bottom = False

    if ball.colliderect(computer.rectangle) and ball.right  >= computer.rectangle.right:
        rect_change_x = rect_change_x * -1
        speed_count += 1
        thinking = False
        rect_change_x += 0.5
    
    if ball[0] > 1300:
        ball[0] = 600
        ball[1] = random.randrange(21,664)
        comp1_score += 1
        rect_change_x = -7
        thinking = True

    if ball[0] < -99:
        ball[0] = 600
        ball[1] = random.randrange(21,664)
        comp2_score += 1
        rect_change_x = 7
        thinking = True

    print_score()
        
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second 
    clock.tick(60)

# Close the window and quit.
pygame.quit()
