import pygame;

from supplementary import *;
from backgroundClass import *;
from playerClass import *;
from scene import *;

pygame.init();

#Define and initialize surface to show to the user:
windowWidth = 1024;
windowHeight = 1024;
gameDisplay = pygame.display.set_mode((windowWidth, windowHeight));

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
    
    acceleration = 0.35;
    friction = 0.25;

    #Scene:
    mainScene = Scene(Background(windowWidth, windowHeight), [], [], [], Player(windowWidth, windowHeight),acceleration, friction);
    
    #Object Properties:
    gameState = {"W_pressed":False, "A_pressed":False, "S_pressed":False, "D_pressed":False,
                 "Q_pressed":False, "E_pressed":False, "mouseCoordinates":(0, 0), "leftMouseClicked":False,
                 "rightMouseClicked":False};

    #Main Game Loop:
    while not gameExit:

        #Event Detection and Handling

        for event in pygame.event.get():        #Get events in real time        
            #print(event);
            
            if event.type == pygame.QUIT:       #Detect for Quit Event 
                gameExit = True;

            elif event.type == pygame.KEYDOWN:    #Detect for Key press
                if event.key == pygame.K_a:       #Detect for A Key
                    gameState["A_pressed"] = True;
                elif event.key == pygame.K_d:     #Detect for D Key
                    gameState["D_pressed"] = True;
                elif event.key == pygame.K_w:     #Detect for W Key
                    gameState["W_pressed"] = True;
                elif event.key == pygame.K_s:     #Detect for S Key
                    gameState["S_pressed"] = True;
                elif event.key == pygame.K_q:     #Detect for Q Key
                    gameState["Q_pressed"] = True;
                elif event.key == pygame.K_e:     #Detect for E Key
                    gameState["E_pressed"] = True;

            elif event.type == pygame.KEYUP:      #Detect for Key release
                if event.key == pygame.K_a:       #Detect for A Key
                    gameState["A_pressed"] = False;
                elif event.key == pygame.K_d:     #Detect for D Key
                    gameState["D_pressed"] = False;
                elif event.key == pygame.K_w:     #Detect for W Key
                    gameState["W_pressed"] = False;
                elif event.key == pygame.K_s:     #Detect for S Key
                    gameState["S_pressed"] = False;
                elif event.key == pygame.K_q:     #Detect for Q Key
                    gameState["Q_pressed"] = False;
                elif event.key == pygame.K_e:     #Detect for E Key
                    gameState["E_pressed"] = False;

            elif event.type == pygame.MOUSEMOTION:#Detect for movement of Mouse
                gameState["mouseCoordinates"] = event.pos;

            elif event.type == pygame.MOUSEBUTTONDOWN:  #Detect for Mouse Button Press
                if event.button == MOUSELEFT:
                    gameState["leftMouseClicked"] = True;
                elif event.button == MOUSERIGHT:
                    gameState["rightMouseClicked"] = True;

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSELEFT:
                    gameState["leftMouseClicked"] = False;
                elif event.button == MOUSERIGHT:
                    gameState["rightMouseClicked"] = False;

        #Logic
        mainScene.update(gameState);

        #Render
        for item in mainScene.getObjectsToRender():
            gameDisplay.blit(item.getSprite(), item.getPos());
        
        pygame.display.update();

        #Control FPS:
        clock.tick(framesPerSecond);

    pygame.quit();
    quit();

gameLoop();
        



        
