#Branching Comment

import pygame;

from supplementary import *;
from backgroundClass import *;
from scene import *;

pygame.init();

#Define and initialize surface to show to the user:
windowWidth = 1024;
windowHeight = 1024;
gameDisplay = pygame.display.set_mode((windowWidth, windowHeight));

#Define colors:
white = (255, 255, 255);
black = (0, 0, 0);
red = (255, 0, 0);
blue = (0, 0, 255);
green = (0, 255, 0);

#Define font:
fontSize = 25;
fontDisplayPos = (windowWidth/2, windowHeight/2);
font = pygame.font.SysFont(None, fontSize);

#Title:
pygame.display.set_caption("Space Arena");

#Classes


#Functions:
def messageToScreen(msg, color=black, displayPos = fontDisplayPos):

    def textObjects():
        textSurface = font.render(msg, True, color);
        return textSurface, textSurface.get_rect();
    
    textSurface, textRect = textObjects();
    textRect.center = (displayPos[0]), (displayPos[1]);
    gameDisplay.blit(textSurface, textRect);
    pygame.display.update();

def gameLoop():

    #Game Loop Variables:

    gameOver = False;
    gameExit = False;

    #Main Game Properties:
    framesPerSecond = 60;
    clock = pygame.time.Clock();

    W_pressed = False;
    A_pressed = False;
    S_pressed = False;
    D_pressed = False;
    Q_pressed = False;
    E_pressed = False;
    acceleration = 0.3;
    friction = 0.1;

    #Scene:
    mainScene = Scene(Background(windowWidth, windowHeight), [], [], [], acceleration, friction);
    
    #Object Properties:

    #Main Game Loop:
    while not gameExit:

        #Event Detection and Handling

        for event in pygame.event.get():        #Get events in real time        
            #print(event);
            
            if event.type == pygame.QUIT:       #Detect for Quit Event 
                gameExit = True;

            if event.type == pygame.KEYDOWN:    #Detect for Key press
                if event.key == pygame.K_a:     #Detect for A Key
                    A_pressed = True;
                if event.key == pygame.K_d:     #Detect for D Key
                    D_pressed = True;
                if event.key == pygame.K_w:     #Detect for W Key
                    W_pressed = True;
                if event.key == pygame.K_s:     #Detect for S Key
                    S_pressed = True;
                if event.key == pygame.K_q:     #Detect for Q Key
                    Q_pressed = True;
                if event.key == pygame.K_e:     #Detect for E key
                    E_pressed = True;

            if event.type == pygame.KEYUP:      #Detect for Key release
                if event.key == pygame.K_a or event.key == pygame.K_d:             
                    A_pressed = False;
                    D_pressed = False;
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    W_pressed = False;
                    S_pressed = False;
                if event.key == pygame.K_q or event.key == pygame.K_e:
                    Q_pressed = False;
                    E_pressed = False;

        keyBoardState = (W_pressed, A_pressed, S_pressed, D_pressed, Q_pressed, E_pressed);
        currentMousePos = pygame.mouse.get_pos();
        currentMouseState = pygame.mouse.get_pressed();

        #Logic
        mainScene.update(keyBoardState, currentMousePos, currentMouseState);

        #Render
        for item in mainScene.getObjectsToRender():
            gameDisplay.blit(item.getSprite(), item.getPos());
        
        pygame.display.update();

        #Control FPS:
        clock.tick(framesPerSecond);

    pygame.quit();
    quit();

gameLoop();
        



        
