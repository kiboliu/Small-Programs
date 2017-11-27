#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 17:50:40 2017

@author: liuzhangqian
"""

import random, sys, time, pygame
from pygame.locals import *

#screen refresh rate, equal to the move speed of snake
FPS = 5

WINDOWWIDTH = 640
WINDOWHEIGHT = 480

#size of grid
CELLSIZE = 20

assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."

#number of grids
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
DARKGREEN = (0,155,0)
DARKGRAY = (40,40,40)
BGCOLOR = BLACK

#move of snake
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#head of snake
HEAD = 0

def main():
    
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    
    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()
    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    BASICFONT = pygame.font.Font('ARBERKLEY.ttf', 18)
    
    pygame.display.set_caption('Snake')
    
    showStartScreen()
    
    while True:
        
        runGame()
        
        showGameOverScreen()

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

#randomly generate a coordinate for food
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

#draw the food according the generated coordinate
def drawFood(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    foodRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, foodRect)

#draw the snake according to the snakeCoords
def drawSnake(snakeCoords):
    for coord in snakeCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        snakeSegmentRect = pygame.Rect(x, y ,CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, snakeSegmentRect)
        snakeInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, snakeInnerSegmentRect)

#show score
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

#exit game
def terminate():
    pygame.quit()
    sys.exit()
    
#message of key to press
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

#catch the event of key pressed
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
        
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
        
    return keyUpEvents[0].key

#show the beginning screen
def showStartScreen():
    DISPLAYSURF.fill(BGCOLOR)
    titleFont = pygame.font.Font('ARBERKLEY.ttf', 100)
    titleSurf = titleFont.render('Snake!', True, GREEN)
    titleRect = titleSurf.get_rect()
    titleRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(titleSurf, titleRect)
    
    drawPressKeyMsg()
    pygame.display.update()
    
    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

#show the operating screen
def runGame():
    #initialize a coordinate for the snake
    #avoid putting snake much near the the wall
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLWIDTH - 6)
    
    #build a snake with length of 3 grids
    snakeCoords = [{'x': startx, 'y': starty}, {'x': startx - 1, 'y': starty}, {'x': startx - 2, 'y': starty}]
    #initialize a movement direction
    direction = RIGHT
    #initialize a food coordinate
    food = getRandomLocation()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        #check if the snake hit the wall
        if snakeCoords[HEAD]['x'] == -1 or snakeCoords[HEAD]['x'] == CELLWIDTH or snakeCoords[HEAD]['y'] == -1 or snakeCoords[HEAD]['y'] == CELLHEIGHT:
            return
        #check if the snake hit itself
        for snakeBody in snakeCoords[1:]:
            if snakeBody['x'] == snakeCoords[HEAD]['x'] and snakeBody['y'] == snakeCoords[HEAD]['y']:
                return
        #check if the snake eat the food
        if snakeCoords[HEAD]['x'] == food['x'] and snakeCoords[HEAD]['y'] == food['y']:
            food = getRandomLocation()
        else:
            #to realize moving the snake, delete its tail and then add a head
            del snakeCoords[-1]
        
        #add a head according to the direction
        if direction == UP:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] - 1}
        if direction == DOWN:
            newHead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] + 1}
        if direction == LEFT:
            newHead = {'x': snakeCoords[HEAD]['x'] - 1, 'y': snakeCoords[HEAD]['y']}
        if direction == RIGHT:
            newHead = {'x': snakeCoords[HEAD]['x'] + 1, 'y': snakeCoords[HEAD]['y']}
        
        snakeCoords.insert(0, newHead)
        
        #draw the background
        DISPLAYSURF.fill(BGCOLOR)
        
        #draw grids
        drawGrid()
        
        #draw the snake
        drawSnake(snakeCoords)
        
        #draw the food
        drawFood(food)
        
        #draw the score
        drawScore(len(snakeCoords) - 3)
        
        #update the screen
        pygame.display.update()
        
        #set the fps
        FPSCLOCK.tick(FPS)
#show the end screen
def showGameOverScreen():
    
    gameOverFont = pygame.font.Font('ARBERKLEY.ttf', 50)
    
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    
    gameRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2 - gameRect.height - 10)
    overRect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()
    
    while True:
        if checkForKeyPress():
            pygame.event.get()
            return
        
if __name__ == '__main__':
    main()

