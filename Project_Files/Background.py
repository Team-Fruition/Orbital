from supplementary import *;
from SpeedController import *;
from DisplacementController import *;

class Background:

    ####Constants
    
    BORDER = 16;
    BOUNCE_VALUE = 5;
    
    ####Properties
    
    ##Main
    
    backgroundWidth = 0;
    backgroundHeight = 0;

    ##Graphical

    #Holds all Sprites used for this object
    backgroundImgList = [];

    #Controls if backgroundSpriteCount increases or decreases
    backgroundLoopBackwards = False;

    #Counter for current frame of animation
    backgroundSpriteCount = 0;

    #Prevents background from updating too quickly
    backgroundDelay = 5;

    ##Positional 
    
    #Controls position to render
    backgroundPos = [];

    #Position at which background is aligned to camera center
    centerBackgroundPos = [];

    #Position at which background's center is at (0, 0)
    trueCenter = [];

    ##Movement 

    #Camera Boundaries (Boolean)
    canContinueMovingLeft = True;
    canContinueMovingRight = True;
    canContinueMovingUp = True;
    canContinueMovingDown = True;

    #Camera Boundaries (Variable)
    leftBound = 0; #Controls when the camera cannot go to the left any further
    rightBound = 0; #Controls when the camera cannot go to the right any further
    upperBound = 0; #Controls when the camera cannot go any higher
    lowerBound = 0; #Controls when the camera cannot go any lower

    #Camera Related Properties
    globalSpeedController = SpeedController();
    globalDisplacementController = DisplacementController();
    
    globalAcceleration = 0;
    globalFriction = 0;
    
    ####Initialization Methods
    
    ##Graphical
    
    def fillImgList(self):
        url = urlConstructor(ART_ASSETS, MAIN_MENU);
        for index in range(0, 18):
            self.backgroundImgList.append(loadImg(url, MAIN_MENU + str(1000 + index)[1:] + JPG_EX));

    ##Main
            
    def determineWidthAndHeight(self):
        self.backgroundWidth = self.backgroundImgList[0].get_width();
        self.backgroundHeight = self.backgroundImgList[0].get_height();

    ##Positional
        
    def determinePositionalData(self, windowWidth, windowHeight):
        self.trueCenter = [-self.backgroundWidth/2, -self.backgroundHeight/2];
        self.centerBackgroundPos = [-self.backgroundWidth/2 + windowWidth/2, -self.backgroundHeight/2 + windowHeight/2];
        self.backgroundPos = [self.centerBackgroundPos[0], self.centerBackgroundPos[1]];

    ##Movement

    def determineCameraBoundaries(self, windowWidth, windowHeight):
        self.leftBound = 0 - self.BORDER;
        self.rightBound = self.getPos()[0]*2 + self.BORDER;
        self.upperBound = 0 - self.BORDER;
        self.lowerBound = self.getPos()[1]*2 + self.BORDER;        

    def setAccelerationAndFriction(self, acceleration, friction):
        self.globalAcceleration = acceleration;
        self.globalFriction = friction;

    ##Init
    
    def __init__(self, windowWidth, windowHeight, acceleration, friction):
        self.fillImgList();
        self.determineWidthAndHeight();
        self.determinePositionalData(windowWidth, windowHeight);
        self.determineCameraBoundaries(windowWidth, windowHeight);
        self.setAccelerationAndFriction(acceleration, friction);

    ####Primary Functions
    
    def update(self, keyBoardState, currentMousePos, currentMouseState, *backgroundData):

        #Update
        self.updatePos(keyBoardState);
        
        #Refresh Sprite
        self.refreshBackgroundSprite();

    def getSprite(self):
        return self.backgroundImgList[self.backgroundSpriteCount];

    def getPos(self):
        return (self.backgroundPos[0], self.backgroundPos[1]);

    ####Secondary Functions

    ##Graphical
    
    def refreshBackgroundSprite(self):
        if self.backgroundDelay >= 5:
            if self.backgroundLoopBackwards == False:
                self.backgroundSpriteCount += 1;
                if self.backgroundSpriteCount >= len(self.backgroundImgList):
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

    ##Positional

    #Directly set position
            
    def setHorizontalCoordinates(self, coordinate):
        self.background[0] = coordinate;

    def setVerticalCoordinates(self, coordinate):
        self.background[1] = coordinate;

    def setPos(self, coordinates):
        self.setHorizontalCoordinates(coordinates[0]);
        self.setVerticalCoordinates(coordinates[1]);

    def centralizeToCamera(self):
        self.backgroundPos = [self.centerBackgroundPos[0], self.centerBackgroundPos[1]];   

    #Get positional data
    def getPos(self):
        return self.backgroundPos;
    
    def getTrueCenter(self):
        return self.trueCenter;

    ##Movement

    def adjustSpeedController(self, keyBoardState):
        if keyBoardState["W"]:
            self.globalSpeedController.adjustVerticalSpeed(self.globalAcceleration, False);
        if keyBoardState["A"]:
            self.globalSpeedController.adjustHorizontalSpeed(-self.globalAcceleration, False);
        if keyBoardState["D"]:
            self.globalSpeedController.adjustHorizontalSpeed(self.globalAcceleration, False);
        if keyBoardState["S"]:
            self.globalSpeedController.adjustVerticalSpeed(-self.globalAcceleration, False);

        self.globalSpeedController.applyFriction(self.globalFriction);

    def calculateNextPosition(self):
        currentBackgroundLocation = self.getPos();
        return (currentBackgroundLocation[0] + self.globalSpeedController.getNetHorizontalSpeed(),
                currentBackgroundLocation[1] + self.globalSpeedController.getNetVerticalSpeed());

    def checkBoundaries(self):
        newBackgroundLocation = self.calculateNextPosition(); 
        
        #Check if camera is about to exceed bottom boundary
        if newBackgroundLocation[1] <= self.lowerBound:
            self.canContinueMovingDown = False;
        else:
            self.canContinueMovingDown = True;
        #Check if camera is about to exceed right boundary
        if newBackgroundLocation[0] <= self.rightBound:
            self.canContinueMovingRight = False;
        else:
            self.canContinueMovingRight = True;
        #Check if camera is about to exceed top boundary
        if newBackgroundLocation[1] >= self.upperBound:
            self.canContinueMovingUp = False;
        else:
            self.canContinueMovingUp = True;
        #Check if camera is about to exceed left boundary
        if newBackgroundLocation[0] >= self.leftBound:
            self.canContinueMovingLeft = False;
        else:
            self.canContinueMovingLeft = True;

    def snapCheck(self):

        self.globalDisplacementController.resetDisplacement();
        
        if not self.canContinueMovingDown:
            #Snap scene to lower bound
            if self.globalSpeedController.movingDown():
                self.globalSpeedController.adjustVerticalSpeed(self.BOUNCE_VALUE, True);
                self.globalDisplacementController.setVerticalDisplacement(self.getPos()[1] - self.lowerBound);
            
        if not self.canContinueMovingLeft:
            #Snap scene to left bound
            if self.globalSpeedController.movingLeft():
                self.globalSpeedController.adjustHorizontalSpeed(self.BOUNCE_VALUE, True);
                self.globalDisplacementController.setHorizontalDisplacement(self.leftBound - self.getPos()[0]);
            
        if not self.canContinueMovingRight:
            #Snap scene to right bound
            if self.globalSpeedController.movingRight():
                self.globalSpeedController.adjustHorizontalSpeed(-self.BOUNCE_VALUE, True);
                self.globalDisplacementController.setHorizontalDisplacement(self.rightBound - self.getPos()[0]);
            
        if not self.canContinueMovingUp:
            #Snap scene to upper bound
            if self.globalSpeedController.movingUp():
                self.globalSpeedController.adjustVerticalSpeed(-self.BOUNCE_VALUE, True);
                self.globalDisplacementController.setVerticalDisplacement(self.getPos()[1] - self.upperBound);        
    
    def moveBackground(self):
        #Move Right = +ve value ##Camera going Left
        #Move Left = -ve value ##Camera going Right
        #Move Up = +ve value ##Camera going Down
        #Move Down = -ve value ##Camera going Up
        self.backgroundPos[0] += -self.globalSpeedController.getNetHorizontalSpeed() + self.globalDisplacementController.getHorizontalDisplacement();
        self.backgroundPos[1] += -self.globalSpeedController.getNetVerticalSpeed() + self.globalDisplacementController.getVerticalDisplacement();    
         
    def updatePos(self, keyBoardState):
        self.adjustSpeedController(keyBoardState);
        self.checkBoundaries();
        self.snapCheck();
        self.moveBackground();

    def getGlobalSpeed(self):
        return self.globalSpeedController;

    def getGlobalDisplacement(self):
        return self.globalDisplacementController;
    
