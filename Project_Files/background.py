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
    autoRoamSpeed = 0.5;

    #Controls camera movement (Up, Down, Left, Right)
    currentMovement = [0, autoRoamSpeed, 0, 0];    
    
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

        #Check for Bottom Boundary
        if reachedBottomBound:
            self.currentMovement = [0, 0, self.autoRoamSpeed, 0]; #Start going Left
        elif reachedLeftBound:
            self.currentMovement = [self.autoRoamSpeed, 0, 0, 0]; #Start going Up
        elif reachedTopBound:
            self.currentMovement = [0, 0, 0, self.autoRoamSpeed]; #Start going Right
        elif reachedRightBound:
            self.currentMovement = [0, self.autoRoamSpeed, 0, 0]; #Start going Down
        
        #Check for Bottom Left Corner
        if reachedBottomLeft:
            self.currentMovement = [self.autoRoamSpeed, 0, 0, 0]; #Go Up
            
        #Check for Bottom Right Corner
        elif reachedBottomRight:
            self.currentMovement = [0, 0, self.autoRoamSpeed, 0]; #Go Left

        #Check for Top Left Corner
        elif reachedTopLeft:
            self.currentMovement = [0, 0, 0, self.autoRoamSpeed]; #Go Right

        #Check for Top Right Corner
        elif reachedTopRight:
            self.currentMovement = [0, self.autoRoamSpeed, 0, 0]; #Go Down

    def _calculatePositionChange(self, moveConfig = "Free"):
        #Assumes that self.currentMovement represents the camera/window and not the background itself
        if moveConfig == "Free":
            self._determineFreeMovement();

        self.currentMovement[0] *= -1;
        self.currentMovement[2] *= -1;
        
        self.backgroundPos[0] += -(self.currentMovement[2] + self.currentMovement[3]);
        self.backgroundPos[1] += -(self.currentMovement[0] + self.currentMovement[1]);

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
