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

    BACKGROUND_BORDER_THICKNESS = 5;

    #Background boundary check variables
    canContinueMovingLeft = True;
    canContinueMovingRight = True;
    canContinueMovingUp = True;
    canContinueMovingDown = True;

    #Variables initialization
    background = [];
    backgroundWidth = 0;
    backgroundHeight = 0;
    
    #Controls if backgroundSpriteCount increases or decreases
    backgroundLoopBackwards = False;

    #Counter for current frame of animation
    backgroundSpriteCount = 0;

    #Prevents background from updating too quickly
    backgroundDelay = 3; 

    #Controls rendering position in the game (x, y)
    backgroundPos = [];

    #Controls free-roam camera speed:
    autoRoamSpeed = 2;

    currentMovement = speedList();
    currentMovement.adjustSpeed(0, autoRoamSpeed);
    
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
        #Check if camera is about to exceed bottom boundary
        if self.backgroundPos[1] <= -self.backgroundHeight/2 + self.BACKGROUND_BORDER_THICKNESS:
            self.canContinueMovingDown = False;
        else:
            self.canContinueMovingDown = True;
        #Check if camera is about to exceed right boundary
        if self.backgroundPos[0] <= -self.backgroundWidth/2 + self.BACKGROUND_BORDER_THICKNESS:
            self.canContinueMovingRight = False;
        else:
            self.canContinueMovingRight = True;
        #Check if camera is about to exceed top boundary
        if self.backgroundPos[1] >= 0 - self.BACKGROUND_BORDER_THICKNESS:
            self.canContinueMovingUp = False;
        else:
            self.canContinueMovingUp = True;
        #Check if camera is about to exceed left boundary
        if self.backgroundPos[0] >= 0 - self.BACKGROUND_BORDER_THICKNESS:
            self.canContinueMovingLeft = False;
        else:
            self.canContinueMovingLeft = True;
            
    def _determineFreeMovement(self):
        self._checkBounds();

        reachedBottomBound = not self.canContinueMovingDown;
        reachedLeftBound = not self.canContinueMovingLeft;
        reachedTopBound = not self.canContinueMovingUp;
        reachedRightBound = not self.canContinueMovingRight;
        
        reachedBottomLeft = reachedBottomBound and reachedLeftBound;
        reachedBottomRight = reachedBottomBound and reachedRightBound;
        reachedTopLeft = reachedTopBound and reachedLeftBound;
        reachedTopRight = reachedTopBound and reachedRightBound;
    
        #Check for Bottom Left Corner
        if reachedBottomLeft:
            self.currentMovement.adjustSpeed(0, -self.autoRoamSpeed); #Go Up
            
        #Check for Bottom Right Corner
        elif reachedBottomRight:
            self.currentMovement.adjustSpeed(self.autoRoamSpeed, 0); #Go Left

        #Check for Top Left Corner
        elif reachedTopLeft:
            self.currentMovement.adjustSpeed(-self.autoRoamSpeed, 0); #Go Right

        #Check for Top Right Corner
        elif reachedTopRight:
            self.currentMovement.adjustSpeed(0, self.autoRoamSpeed); #Go Down

        if reachedBottomBound and not reachedBottomLeft:
            self.currentMovement.adjustSpeed(self.autoRoamSpeed, 0); #Start going Left
            
        elif reachedLeftBound and not reachedTopLeft:
            self.currentMovement.adjustSpeed(0, -self.autoRoamSpeed); #Start going Up
            
        elif reachedTopBound and not reachedTopRight:
            self.currentMovement.adjustSpeed(-self.autoRoamSpeed, 0); #Start going Right
            
        elif reachedRightBound and not reachedBottomRight:
            self.currentMovement.adjustSpeed(0, self.autoRoamSpeed); #Start going Down

    def _calculatePositionChange(self, moveConfig = "Free", currentMovement = None):
        #Assumes that self.currentMovement represents the camera/window and not the background itself
        if moveConfig == "Free":
            self._determineFreeMovement();

        if currentMovement == None:
            currentMovement = self.currentMovement;
        
        if not currentMovement.noNetSpeed():
            self.backgroundPos[0] += currentMovement.getNetHorizontalSpeed();
            self.backgroundPos[1] += currentMovement.getNetVerticalSpeed();

    #Called at every iteration of the loop    
    def update(self):
        #Controls background positioning
        self._calculatePositionChange();
        
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

    def setRenderCoordinates(self, coordinates):
        self.backgroundPos[0] = coordinates[0];
        self.backgroundPos[1] = coordinates[1];
