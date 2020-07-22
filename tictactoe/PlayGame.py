import pygame, sys
from pygame.locals import *
import time
import numpy as np

# import custom game class
from BaseGame import TicTacToe

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 1
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 360

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

background = pygame.image.load("./assets/tictactoe_background.jpg")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)

pygame.display.set_caption("Game")


class block(pygame.sprite.Sprite):
    def __init__(self, i):
        super().__init__() 
        self.surf = pygame.Surface((100, 100))
        self.rect = self.surf.get_rect(topleft=((i//3)*SCREEN_WIDTH/3+50, 10+(i%3)*SCREEN_HEIGHT/3))
        self.i = i
        
    def display(self, user):
        if user==1:
            self.image = pygame.image.load("./assets/x.jpg")
        else:
            self.image = pygame.image.load("./assets/o.jpg")
        
sprites = []
for i in range(9):
    new_sprite = block(i)
    sprites.append(new_sprite)
          
def keep_playing():
    # runs after game finishes to get user input
    while True:
        button = Rect(SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2-50, 300, 100)
        
        # draw button and background
        DISPLAYSURF.fill(WHITE)
        pygame.draw.rect(DISPLAYSURF, GREEN, button)
        
        text = font_small.render('Click here to play again!', True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        DISPLAYSURF.blit(text, text_rect)
        
        
        DISPLAYSURF.blit(font_small.render('User wins: {}'.format(records[0]), True, BLACK), 
                         (0, 0))
        DISPLAYSURF.blit(font_small.render('Ties: {}'.format(records[1]), True, BLACK), 
                         (0, text_rect.height))
        DISPLAYSURF.blit(font_small.render('Computer wins: {}'.format(records[2]), True, BLACK), 
                         (0, text_rect.height*2))
        
        # update layout
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # location of the click
                x,y = event.pos

                if button.collidepoint(x,y):
                    return True
                else:
                    return False
					
play = True
records = [0,0,0]
while play:
    game = TicTacToe()
    #Game Loop
    while not game.game_finished:
        if game.user==1:
            # get user input to update game layout
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # location of the click
                    x,y = event.pos

                    for sprite in sprites:
                        if sprite.rect.collidepoint(x,y):

                            if game.board[sprite.i//3, sprite.i%3]==0:
                                # update the game board                        
                                game.board[sprite.i//3, sprite.i%3] = 1

                                # change the user so the computer goes next
                                game.game_finished = game.is_game_finished()
                                game.user *= -1
                                break # out of inner loop
        else:   
            # make computer move
            game.make_computer_move()
            time.sleep(.25)
            game.game_finished = game.is_game_finished()
            game.user *= -1

        # update the board
        DISPLAYSURF.blit(background, (0,0))
        for i,element in enumerate(game.board.flatten()):
            if element!=0:
                sprite = sprites[i]

                # set whether the sprite is an X or O
                sprite.display(element)

                DISPLAYSURF.blit(sprite.image, sprite.rect)

        pygame.display.update()
    records[game.winner*-1+1] += 1
    time.sleep(.5)
    play = keep_playing()
	
pygame.display.quit()
pygame.quit()