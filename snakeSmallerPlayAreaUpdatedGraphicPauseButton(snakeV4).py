# Importing the libraries
import pygame
from pygame.locals import *
import random 

def pause():
    #loops until 'p' is pressed again, the esc key is pressed to exit, or the 'x' button is pressed to exit
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                global running; running = False
                return
            if event.type == KEYDOWN and event.key == K_p:
                return

#function that generates a randomly placed food
def createFood(snakeBody):
    #creates random cords for a possible food location
    randX = random.randint(0,24) * 25
    randY = random.randint(0,24) * 25
    food = pygame.Rect(randX,randY, 25,25)

    #if the possible food is located where the snake or an existing food is it creates a new location until finds a free space
    if ([randX, randY] in snakeBody) or food.colliderect(food1) or food.colliderect(food2):
        while ([randX, randY] in snakeBody) or food.colliderect(food1) or food.colliderect(food2):
            randX = random.randint(0,24) * 25
            randY = random.randint(0,24) * 25
            food = pygame.Rect(randX,randY, 25,25)
    #if the location is valid it returns the new food with its new random location
    return food

def game():
    surface.fill(black)

    #creates the starting snakeHead and speed
    snakeBody = []
    snakeBody.append([300,300])
    snakeHead = pygame.Rect(snakeBody[0][0], snakeBody[0][1], 25, 25)
    pygame.draw.rect(surface, green, snakeHead)

    #creates variables associated with the snake's speed
    speed = [0,0]
    ittSpeed = [10,9,8,7]
    lastMoveSpeed = [0,0]
    speedCounter = 0
    ittCount = -1

    #draws starting food onto surface
    foodCount = 0
    global score
    food1 = createFood(snakeBody)
    food2 = createFood(snakeBody)
    pygame.draw.rect(surface, red, food1)
    pygame.draw.rect(surface, red, food2)

    global running
    running = True
    while running:
        ittCount += 1
        #sets delay so the object does not move so fast
        pygame.time.wait(ittSpeed[speedCounter])

        #only moves the snake every 10 itterations
        if ittCount % 15 == 0:
            if speed != [0,0]:
                snakeBody.append([snakeBody[len(snakeBody)-1][0] + speed[0],snakeBody[len(snakeBody)-1][1] + speed[1]])
                snakeHead = pygame.Rect(snakeBody[len(snakeBody)-1][0],snakeBody[len(snakeBody)-1][1], 25,25)
                pygame.draw.rect(surface, green, snakeHead)

            #removes the last segment of its body
            if len(snakeBody) > foodCount + 1:
                if snakeBody[len(snakeBody)-1] != snakeBody[0]:
                    pygame.draw.rect(surface, black, pygame.Rect(snakeBody[0][0], snakeBody[0][1], 25, 25))
                del snakeBody[0]

            #updates display after the snake moved 
            pygame.display.flip()

            #checks if the snake runs into its body
            if snakeBody[len(snakeBody)-1] in snakeBody[:len(snakeBody)-1]:
                running = False

            #updates the direction of the last move
            lastMoveSpeed = speed


        #sets speed according to food count
        if foodCount >= 40: speedCounter = 3
        elif foodCount >= 30: speedCounter = 2
        elif foodCount >= 20: speedCounter = 1

        #checks to see if the user clicks the 'x'
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                #checks if the keydown is the esc key to quit the game
                if event.key == K_ESCAPE:
                    running = False
                #ckecks if the keydown is the 'p' key to pause the game
                if event.key == K_p:
                    pause()

                #checks if the user press an arrow key or wasd to change directions of the snake
                #also checks to see if it is allowed to change to that direction (you can't move left and then directly right if food has been collected)
                if event.key == K_UP or event.key == K_w:
                    if lastMoveSpeed != [0,25] or foodCount < 1:
                        speed = [0,-25]
                if event.key == K_DOWN or event.key == K_s:
                    if lastMoveSpeed != [0,-25] or foodCount < 1:
                        speed = [0,25]
                if event.key == K_LEFT or event.key == K_a:
                    if lastMoveSpeed != [25,0] or foodCount < 1:
                        speed = [-25,0]
                if event.key == K_RIGHT or event.key == K_d:
                    if lastMoveSpeed != [-25,0] or foodCount < 1:
                        speed = [25,0]

        #checks to make sure the snake does not go off screen
        if snakeHead.top < 0:
            running = False
        if snakeHead.bottom > 625:
            running = False
        if snakeHead.left < 0:
            running = False
        if snakeHead.right > 625:
            running = False

        #checks if the snake head collides with food
        if food1.colliderect(snakeHead):
            foodCount += 3
            pygame.draw.rect(surface, green, food1)
            food1 = createFood(snakeBody)
            pygame.draw.rect(surface, red, food1)
            pygame.display.flip()

        if food2.colliderect(snakeHead):
            foodCount += 3
            pygame.draw.rect(surface, green, food2)
            food2 = createFood(snakeBody)
            pygame.draw.rect(surface, red, food2)
            pygame.display.flip()

    #updates the score with the amount of food collected in that game
    score = foodCount

def main():
    game()

    running = True
    while running:
        #creates the fonts and texts for the score to be displayed 
        surface.fill(black)
        font1 = pygame.font.SysFont("agencyfb", 50)
        font2 = pygame.font.SysFont("agencyfb",20)
        textScoreWords = font1.render("Score: ",True,green)
        textScoreNum = font1.render(str(score),True,red)
        textRestart = font2.render("press 'r' to restart",True,grey)

        #displays the score and updates the display
        surface.blit(textScoreWords, (312 - (textScoreWords.get_width() + textScoreNum.get_width())/2, 312 - (textScoreWords.get_height() + textScoreNum.get_height())/2))
        surface.blit(textScoreNum, (312 - (textScoreWords.get_width() + textScoreNum.get_width())/2 + textScoreWords.get_width() , 312 - (textScoreWords.get_height() + textScoreNum.get_height())/2))
        surface.blit(textRestart,(312 - textRestart.get_width()/2, 312 + (textScoreWords.get_height() + textScoreNum.get_height())))
        pygame.display.flip()

        for event in pygame.event.get():
            #checks to see if the user clicks the 'x' button or esc key
            if event.type == QUIT:
                running = False
            #checks to see if the user clicks the restart button or the esc key
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                if event.key == K_r:
                    game()

# Initializing Pygame
pygame.init()
running = True

# Initializing Colors
red = (255,0,0)
black = (0,0,0)
white = (255,255,255)
green = (57,255,20)
grey = (85,85,85)

# Initializing surface
size = 625, 625
width, height = size
surface = pygame.display.set_mode(size)
pygame.display.set_caption("Snake Game")
surface.fill(black)

#initializing score
score = 0

#initializing temp food
food1 = pygame.Rect(-25,-25,0,0)
food2 = pygame.Rect(-25,-25,0,0)

#calls the main function to start 
main()