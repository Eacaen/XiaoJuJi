import random, copy, sys, pygame
from pygame.locals import *

FPS = 30 # frames per second to update the screen
WINDOWWIDTH = 640 # width of the program's window, in pixels
WINDOWHEIGHT = 480 # height in pixels
SPACESIZE = 50 # size of the tokens and individual board spaces in pixels
BRIGHTBLUE = (  0, 170, 255)
WHITE	  = (255, 255, 255)
WHITE		= (255, 255, 255)
BLACK		= (  0,   0,   0)
BRIGHTRED	= (255,   0,   0)
RED		  = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN		= (  0, 155,   0)
BLUE		 = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW	   = (155, 155,   0)
DARKGRAY	 = ( 40,  40,  40)
DARKGREEN = (  0, 255,   0)


def main():
	global FPSCLOCK, DISPLAYSURF, REDPILERECT, REDTOKENIMG,BLACKTOKENIMG,BLACKPILERECT


	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Four in a Row')

	REDTOKENIMG = pygame.image.load('4row_red.png')
	REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))
	BLACKTOKENIMG = pygame.image.load('4row_black.png')
	BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))

	REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
	BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)
 

	DISPLAYSURF.fill(WHITE)
	# draw the red and black tokens off to the side
	DISPLAYSURF.blit(REDTOKENIMG, REDPILERECT) # red on the left
	DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT) # black on the right

	while True:

		runGame()


def runGame():
	draggingToken = False
	tokenx, tokeny = None, None

	while True:
		DISPLAYSURF.fill(WHITE)
		DISPLAYSURF.blit(REDTOKENIMG, REDPILERECT) # red on the left
		DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT) # black on the right

		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN and not draggingToken and REDPILERECT.collidepoint(event.pos):
				# start of dragging on red token pile.
				draggingToken = True
				tokenx, tokeny = event.pos
			elif event.type == MOUSEMOTION and draggingToken:
				# update the position of the red token being dragged
				tokenx, tokeny = event.pos
			elif event.type == MOUSEBUTTONUP and draggingToken:
				animateDroppingToken(tokenx, tokeny)

				tokenx, tokeny = None, None
				draggingToken = False

		if tokenx != None and tokeny != None:
			print( tokenx, tokeny)
			REDTOKENIMG_r = REDTOKENIMG.get_rect()
			REDTOKENIMG_r.center = (tokenx, tokeny)
			DISPLAYSURF.blit(REDTOKENIMG, REDTOKENIMG_r)



		
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def terminate():
	pygame.quit()
	sys.exit()

def animateDroppingToken(x, y):
	dropSpeed = 1.0

	lowestEmptySpace = WINDOWHEIGHT

	while True:
		y += int(dropSpeed)
		# dropSpeed += 0.5
		if  y >= lowestEmptySpace:ｙ
			return

		REDTOKENIMG_r = REDTOKENIMG.get_rect()
		REDTOKENIMG_r.center = (x, y)
		DISPLAYSURF.blit(REDTOKENIMG, REDTOKENIMG_r)

		pygame.display.update()
		FPSCLOCK.tick()

if __name__ == '__main__':
	main()