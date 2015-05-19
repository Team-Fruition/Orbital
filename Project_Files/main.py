import pygame;

from supplementary import *;
from background import loadBackground;

pygame.init();

#Define and initialize surface to show to the user:
window_width = 1024;
window_height = 1024;
gameDisplay = pygame.display.set_mode((window_width, window_height));

#Define colors:
white = (255, 255, 255);
black = (0, 0, 0);
red = (255, 0, 0);
blue = (0, 0, 255);
green = (0, 255, 0);

#Define font:
fontSize = 25;
fontDisplayPos = (window_width/2, window_height/2);
font = pygame.font.SysFont(None, fontSize);

#Title:
pygame.display.set_caption("Space Arena");

#External Functions:
def message_to_screen(msg, color=black, displayPos = fontDisplayPos):

    def textObjects():
        textSurface = font.render(msg, True, color);
        return textSurface, textSurface.get_rect();
    
    textSurface, textRect = textObjects();
    textRect.center = (displayPos[0]), (displayPos[1]);
    gameDisplay.blit(textSurface, textRect);
    pygame.display.update();

class backgroundDisplayLogic:

    background = [];
    backgroundLoopBackwards = False;
    backgroundSpriteCount = 0;
    backgroundDelay = 5;
    
    def __init__(self, backgroundList):
        self.background = backgroundList;

    def update(self):
        if self.backgroundDelay >= 5:
            if self.backgroundLoopBackwards == False:
                self.backgroundSpriteCount += 1;
                if self.backgroundSpriteCount >= len(self.background):
                    self.backgroundLoopBackwards = True;
                    self.backgroundSpriteCount -= 1;
            else:
                self.backgroundSpriteCount -= 1;
                if self.backgroundSpriteCount <= 0:
                    self.backgroundLoopBackwards = False;
                    self.backgroundSpriteCount +=1;
                
            self.backgroundDelay = 0;
        else:
            self.backgroundDelay += 1;

    def obtainBackgroundSprite(self):
        return self.background[self.backgroundSpriteCount];

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
    acceleration = 0.35;
    friction = 0.25;

    #Background:
    background = backgroundDisplayLogic(loadBackground());
    
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

            if event.type == pygame.KEYUP:      #Detect for Key release
                if event.key == pygame.K_a or event.key == pygame.K_d:             
                    A_pressed = False;
                    D_pressed = False;
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    W_pressed = False;
                    S_pressed = False;


        #Logic

        #Render

        #Background:
        gameDisplay.blit(background.obtainBackgroundSprite(), (-1024, -1024));
        background.update();
        
        pygame.display.update();

        #Control FPS:
        clock.tick(framesPerSecond);

    pygame.quit();
    quit();

gameLoop();
        



        
