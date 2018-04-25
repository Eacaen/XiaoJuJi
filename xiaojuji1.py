# Squirrel Eat Squirrel (a 2D Katamari Damacy clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, sys, time, math, pygame
from pygame.locals import *

FPS = 30 # frames per second to update the screen
WINWIDTH = 1100 # width of the program's window, in pixels
WINHEIGHT = 500 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

GRASSCOLOR = (24, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

CAMERASLACK_X = 500     # how far from the center the squirrel moves before moving the camera
CAMERASLACK_Y = 200    
MOVERATE = 9         # how fast the player moves
BOUNCERATE = 6       # how fast the player bounces (large is slower)
BOUNCEHEIGHT = 30    # how high the player bounces
STARTSIZE = 34       # how big the player starts off
WINSIZE = 300        # how big the player needs to be to win
INVULNTIME = 2       # how long the player is invulnerable after being hit in seconds
GAMEOVERTIME = 4     # how long the "game over" text stays on the screen in seconds
MAXHEALTH = 3        # how much health the player starts with

NUMGRASS = 80        # number of grass objects in the active area
NUMSQUIRRELS = 30    # number of squirrels in the active area
SQUIRRELMINSPEED = 3 # slowest squirrel speed
SQUIRRELMAXSPEED = 7 # fastest squirrel speed
DIRCHANGEFREQ = 2    # % chance of direction change per frame
LEFT = 'left'
RIGHT = 'right'
ANGLE = 90
def main():
    global FPSCLOCK, DISPLAYSURF, BGIMAGE , BASICFONT, L_SQUIR_IMG, GRASSIMAGES

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('gameicon.png'))
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('xiao ju ji')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)

    # load the image files
    L_SQUIR_IMG = pygame.image.load('xufeiji.png')

    BGIMAGE = pygame.image.load('flippybackground.png')
    GRASSIMAGES = []
    GRASSIMAGES.append( pygame.image.load('local3.png'))

    while True:
        runGame()


def runGame():
    # set up variables for the start of a new game
    invulnerableMode = False  # if the player is invulnerable
    invulnerableStartTime = 0 # time the player became invulnerable
    gameOverMode = False      # if the player has lost
    gameOverStartTime = 0     # time the player lost
    winMode = False           # if the player has won


    # camerax and cameray are the top left of where the camera view is
    camerax = 0
    cameray = 0

    AccidentObj = []    # stores all the grass objects in the game
    squirrelObjs = [] # stores all the non-player squirrel objects
    # stores the player object:
    playerObj = {'surface': pygame.transform.rotate(\
        pygame.transform.scale(L_SQUIR_IMG, (STARTSIZE, STARTSIZE)), ANGLE),
                 'facing': LEFT,
                 'size': STARTSIZE,
                 'x': HALF_WINWIDTH,
                 'y': HALF_WINHEIGHT,
                 'health': MAXHEALTH,
                 'ANGLE': ANGLE}

    moveLeft  = False
    moveRight = False
    moveUp    = False
    moveDown  = False

    tokenx, tokeny = None, None
    AREA = 50
    # start off with some random grass images on the screen

    while True: # main game loop
        i = 0
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:

                if event.key in (K_UP, K_w):
                    moveDown = False
                    moveUp = True
                elif event.key in (K_DOWN, K_s):
                    moveUp = False
                    moveDown = True
                elif event.key in (K_LEFT, K_a):
                    moveRight = False
                    moveLeft = True
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = True


            elif event.type == KEYUP:
                # stop moving the player's squirrel
                if event.key in (K_LEFT, K_a):
                    moveLeft = False
                    moveRight = False
                elif event.key in (K_RIGHT, K_d):
                    moveLeft = False
                    moveRight = False
                elif event.key in (K_UP, K_w):
                    moveUp = False
                    moveDown = False
                elif event.key in (K_DOWN, K_s):
                    moveDown = False
                    moveUp = False

                elif event.key == K_ESCAPE:
                    terminate()


            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # start of dragging on red token pile.
                tokenx, tokeny = event.pos

            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                # start of dragging on red token pile.
                tokenx, tokeny = event.pos

        i = 0
        if tokenx != None and tokeny != None:
            print( tokenx, tokeny)

            if len(AccidentObj) == 0:
                AccidentObj.append(makeNewLocation( tokenx, tokeny ))
                tokenx, tokeny = None, None
            else:
                
                for gObj in AccidentObj:
                    i = i +1
                    gRect = pygame.Rect( (gObj['x'] ,gObj['y'] , gObj['width'], gObj['height']) )

                    if  gRect.collidepoint( (tokenx, tokeny) ):
                        print('del location')
                        AccidentObj.remove( gObj)
                        break

                if i == len(AccidentObj):
                    print('i == len(AccidentObj)' , i , len(AccidentObj))
                    print('add location')
                    AccidentObj.append(makeNewLocation( tokenx, tokeny ))      
                    i = 0


        tokenx, tokeny = None, None
        # move all the squirrels
        for sObj in squirrelObjs:
            # move the squirrel, and adjust for their bounce
            sObj['x'] += sObj['movex']
            sObj['y'] += sObj['movey']



        # adjust camerax and cameray if beyond the "camera slack"
        playerCenterx = playerObj['x'] + int(playerObj['size'] / 2)
        playerCentery = playerObj['y'] + int(playerObj['size'] / 2)
        if (camerax + HALF_WINWIDTH) - playerCenterx > CAMERASLACK_X:
            camerax = playerCenterx + CAMERASLACK_X - HALF_WINWIDTH
        elif playerCenterx - (camerax + HALF_WINWIDTH) > CAMERASLACK_X:
            camerax = playerCenterx - CAMERASLACK_X - HALF_WINWIDTH

        if (cameray + HALF_WINHEIGHT) - playerCentery > CAMERASLACK_Y:
            cameray = playerCentery + CAMERASLACK_Y - HALF_WINHEIGHT
        elif playerCentery - (cameray + HALF_WINHEIGHT) > CAMERASLACK_Y:
            cameray = playerCentery - CAMERASLACK_Y - HALF_WINHEIGHT

        # draw the green background
        DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())


        for gObj in AccidentObj:
            gRect = pygame.Rect( (gObj['x'] , # - camerax,
                                  gObj['y'] ,#- cameray,
                                  gObj['width'],
                                  gObj['height']) )
            # pygame.draw.rect(DISPLAYSURF, RED, (gObj['x'] ,gObj['y'] , gObj['width'], gObj['height']), 1)

            DISPLAYSURF.blit(GRASSIMAGES[gObj['grassImage']], gRect)

        # draw the player squirrel

        playerObj['rect'] = pygame.Rect( (playerObj['x'] - camerax,
                                              playerObj['y'] - cameray ,
                                              playerObj['size'],
                                              playerObj['size']) )
        DISPLAYSURF.blit(playerObj['surface'], playerObj['rect'])


        # draw the health meter
        drawHealthMeter(playerObj['health'])

        if not gameOverMode:
            # actually move the player

            if moveLeft:
                playerObj['x'] -= MOVERATE
            if moveRight:
                playerObj['x'] += MOVERATE
            if moveUp:
                playerObj['y'] -= MOVERATE
            if moveDown:
                playerObj['y'] += MOVERATE


        pygame.display.update()
        FPSCLOCK.tick(FPS)



def makeNewLocation(tokenx, tokeny):
    gr = {}
    gr['grassImage'] = random.randint(0, len(GRASSIMAGES) - 1)
    gr['width']  = GRASSIMAGES[0].get_width()
    gr['height'] = GRASSIMAGES[0].get_height()
    gr['x'], gr['y'] = (tokenx - gr['width']/2 , tokeny -  gr['height'])
    gr['rect'] = pygame.Rect( (gr['x'], gr['y'], gr['width'], gr['height']) )
    return gr

def drawHealthMeter(currentHealth):
    for i in range(currentHealth): # draw red health bars
        pygame.draw.rect(DISPLAYSURF, RED,   (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10))
    for i in range(MAXHEALTH): # draw the white outlines
        pygame.draw.rect(DISPLAYSURF, WHITE, (15, 5 + (10 * MAXHEALTH) - i * 10, 20, 10), 1)


def terminate():
    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    main()