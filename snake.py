# Importing the library
import pygame
from pygame.locals import *
import random

#function that generates a randomly placed food
def createFood():
    randX = random.randint(0,39) * 10
    randY = random.randint(0,39) * 10
    food = pygame.Rect(randX,randY, 10,10)

    if ([randX, randY] in snakeBody) or food.colliderect(food1) or food.colliderect(food2):
        while ([randX, randY] in snakeBody) or food.colliderect(food1) or food.colliderect(food2):
            randX = random.randint(0,39) * 10
            randY = random.randint(0,39) * 10
            food = pygame.Rect(randX,randY, 10,10)
    return food

# Initializing Pygame
pygame.init()

# Initializing Colors
red = (255,0,0)
black = (0,0,0)
white = (255,255,255)
green = (57,255,20)
 
# Initializing surface
size = 400, 400
width, height = size
surface = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")
surface.fill(black)

#creates the starting snakeHead and speed
snakeBody = []
snakeBody.append([190,190])
snakeHead = pygame.Rect(snakeBody[0][0], snakeBody[0][1], 10, 10)
pygame.draw.rect(surface, green, snakeHead)

#creates variables associated with the snake's speed
speed = [0,0]
ittSpeed = [10,9,8,7]
lastMoveSpeed = [0,0]
speedCounter = 0
ittCount = -1

#sets up the starting food
foodCount = 0
food1 = pygame.Rect(-10,-10,0,0)
food2 = pygame.Rect(-10,-10,0,0)
food1 = createFood()
food2 = createFood()
pygame.draw.rect(surface, red, food1)
pygame.draw.rect(surface, red, food2)

running = True
while running:
    ittCount += 1
    #sets delay so the object does not move so fast
    pygame.time.wait(ittSpeed[speedCounter])

    #only moves the snake every 10 itterations
    if ittCount % 10 == 0:
        if speed != [0,0]:
            snakeBody.append([snakeBody[len(snakeBody)-1][0] + speed[0],snakeBody[len(snakeBody)-1][1] + speed[1]])
            snakeHead = pygame.Rect(snakeBody[len(snakeBody)-1][0],snakeBody[len(snakeBody)-1][1], 10,10)
            pygame.draw.rect(surface, green, snakeHead)

        #removes the last segment of its body
        if len(snakeBody) > foodCount + 1:
            if snakeBody[len(snakeBody)-1] != snakeBody[0]:
                pygame.draw.rect(surface, black, pygame.Rect(snakeBody[0][0], snakeBody[0][1], 10, 10))
            del snakeBody[0]

        pygame.display.flip()

        #checks if the snake runs into its body
        if snakeBody[len(snakeBody)-1] in snakeBody[:len(snakeBody)-1]:
            running = False

        #updates the direction of the last movea
        lastMoveSpeed = speed


    #sets speed according to food count
    if foodCount >= 40: speedCounter = 3
    elif foodCount >= 30: speedCounter = 2
    elif foodCount >= 20: speedCounter = 1

    #checks to see if the user clicks the 'x' button
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        #if the user presses a button and it is an arrow key it changes the direction of the object
        #also checks to see if it is allowed to change to that direction
        if event.type == KEYDOWN:
            if event.key == K_UP:
                if lastMoveSpeed != [0,10] or foodCount < 1:
                    speed = [0,-10]
            if event.key == K_DOWN:
                if lastMoveSpeed != [0,-10] or foodCount < 1:
                    speed = [0,10]
            if event.key == K_LEFT:
                if lastMoveSpeed != [10,0] or foodCount < 1:
                    speed = [-10,0]
            if event.key == K_RIGHT:
                if lastMoveSpeed != [-10,0] or foodCount < 1:
                    speed = [10,0]

    #checks to make sure the snake does not go off screen
    if snakeHead.top < 0:
        running = False
    if snakeHead.bottom > 400:
        running = False
    if snakeHead.left < 0:
        running = False
    if snakeHead.right > 400:
        running = False

    #checks if the snake head collides with food
    if food1.colliderect(snakeHead):
        foodCount += 1
        pygame.draw.rect(surface, green, food1)
        food1 = createFood()
        pygame.draw.rect(surface, red, food1)
        pygame.display.flip()

    if food2.colliderect(snakeHead):
        foodCount += 1
        pygame.draw.rect(surface, green, food2)
        food2 = createFood()
        pygame.draw.rect(surface, red, food2)
        pygame.display.flip()

#window opens to show score
size = 300, 300
pygame.init()
pygame.display.set_caption("Score")
surface = pygame.display.set_mode(size)
running = True
font = pygame.font.SysFont("Times new Roman", 40)
text = font.render("Score: " + str(foodCount),True,black)

surface.fill(white)
surface.blit(text,((150-text.get_width()/2),(150-text.get_height()/2)))
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False