import pygame;

from supplementary import *;

#Constants:

ART_ASSETS = "Art_Assets";
MAIN_MENU = "MainMenu";
JPG_EX = ".jpg";

def loadBackground():

    background = [];
    
    for index in range(0, 18):
        background.append(loadImg(urlConstructor(ART_ASSETS, MAIN_MENU), MAIN_MENU + str(1000 + index)[1:] + JPG_EX));

    return background;

class BackgroundDisplayLogic:

    #Default Color
    BLACK = (0, 0, 0);

    #Constants initialization
    MOVE_DOWN = 1;
    MOVE_RIGHT = 2;
    MOVE_UP = 3;
    MOVE_LEFT = 4;

    BACKGROUND_BORDER_THICKNESS = 5;

    #Background movement boundaries (variable names according to view from camera)
    #Tuple Values: (exceedBottom, exceedRight, exceedTop, exceedLeft)
    BTM_RIGHT = (True, True, False, False);
    BTM_LEFT = (True, False, False, True);
    TOP_RIGHT = (False, True, True, False);
    TOP_LEFT = (False, False, True, True);

    #Variables initialization
    background = [];
    backgroundWidth = 0;
    backgroundHeight = 0;
    
    #Controls if backgroundSpriteCount increases or decreases
    backgroundLoopBackwards = False;

    #Counter for current frame of animation
    backgroundSpriteCount = 0;

    #Prevents background from updating too quickly
    backgroundDelay = 5; 

    #Controls rendering position in the game (x, y)
    backgroundPos = [];

    #Controls camera movement
    currentMovement = MOVE_DOWN;

    #Controls camera speed:
    movementSpeed = 0.5;
    
    def __init__(self, backgroundList):
        self.background = backgroundList;

        if len(self.background) == 0:
            tempBackground = pygame.Surface((2048, 2048));
            tempBackground.fill(BLACK);
            self.background = [tempBackground];
        
        self.backgroundWidth = self.background[0].get_width();
        self.backgroundHeight = self.background[0].get_height();
        self.backgroundPos = [-self.backgroundWidth/4, -self.backgroundHeight/4];

    def _checkBounds(self):
        exceedBottom = False;
        exceedRight = False;
        exceedTop = False;
        exceedLeft = False;
        
        #Check if camera is about to exceed bottom boundary
        if self.backgroundPos[1] <= -self.backgroundHeight/2 + self.BACKGROUND_BORDER_THICKNESS:
            exceedBottom = True;
        #Check if camera is about to exceed right boundary
        if self.backgroundPos[0] <= -self.backgroundWidth/2 + self.BACKGROUND_BORDER_THICKNESS:
            exceedRight = True;
        #Check if camera is about to exceed top boundary
        if self.backgroundPos[1] >= 0 - self.BACKGROUND_BORDER_THICKNESS:
            exceedTop = True;      
        #Check if camera is about to exceed left boundary
        if self.backgroundPos[0] >= 0 - self.BACKGROUND_BORDER_THICKNESS:
            exceedLeft = True;

        return (exceedBottom, exceedRight, exceedTop, exceedLeft);
            
    def _determineFreeMovement(self):
        boundaryCheck = self._checkBounds();

        numEntryTrue = 0;
        
        for entry in boundaryCheck:
            if entry == True:
                numEntryTrue += 1;

        if numEntryTrue == 1:
            #Exceed one of the boundaries
            if boundaryCheck[0] == True:
                self.currentMovement = self.MOVE_LEFT;
            elif boundaryCheck[1] == True:
                self.currentMovement = self.MOVE_DOWN;
            elif boundaryCheck[2] == True:
                self.currentMovement = self.MOVE_RIGHT;
            else:
                self.currentMovement = self.MOVE_UP;

        elif numEntryTrue == 2:
            #Camera is at one of the corners
            if boundaryCheck == self.BTM_RIGHT:
                self.currentMovement = self.MOVE_LEFT;
            elif boundaryCheck == self.BTM_LEFT:
                self.currentMovement = self.MOVE_UP;
            elif boundaryCheck == self.TOP_RIGHT:
                self.currentMovement = self.MOVE_DOWN;
            else:
                self.currentMovement = self.MOVE_RIGHT;

    def moveBackground(self):
        self._determineFreeMovement();

        if self.currentMovement == self.MOVE_DOWN:
            self.backgroundPos[1] -= self.movementSpeed;
        elif self.currentMovement == self.MOVE_RIGHT:
            self.backgroundPos[0] -= self.movementSpeed;
        elif self.currentMovement == self.MOVE_UP:
            self.backgroundPos[1] += self.movementSpeed;
        else:
            self.backgroundPos[0] += self.movementSpeed;

    #Called at every iteration of the loop    
    def update(self):
        #Controls background positioning
        self.moveBackground();
        
        #Controls background sprite refresh rate
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

    def getBackgroundSprite(self):
        return self.background[self.backgroundSpriteCount];

    def resetRenderCoordinates(self):
        self.background_pos = (-self.backgroundWidth/2, -self.backgroundHeight/2);
    
    def getRenderCoordinates(self):
        return (self.backgroundPos[0], self.backgroundPos[1]);
