import pygame;

from supplementary import *;
from DisplacementController import *;
from SpeedController import *;

####Base Classes

class Object(pygame.sprite.Sprite):

    ####Object ID Methods

    numObj = 0;

    @classmethod
    def getObjNum(cls):
        return cls.numObj;

    @classmethod
    def incrementObjNum(cls):
        cls.numObj += 1;

    @classmethod
    def getClassName(cls):
        return cls.__name__;
    
    def setObjID(self):
        self.ID = str(self.getClassName()).join(str(self.getObjNum()));
        self.incrementObjNum();

    def getObjID(self):
        return self.ID;

    ####Static Variables
    
    spriteImgList = None;
    spriteWidth = None;
    spriteHeight = None;
    numObj = 0;

    ####Initialization Methods
    
    @classmethod
    def fillImgList(cls, url, fileName, indexLen, numFrames, ex):
        if cls.spriteImgList == None:
            cls.spriteImgList = [];
            indexingVariable = 10 ** (indexLen);
            for index in range(0, numFrames):
                cls.spriteImgList.append(loadImg(url, fileName + str(indexingVariable + index)[1:] + ex).convert());

    @classmethod
    def determineWidthAndHeight(cls):
        if cls.spriteWidth == None or cls.spriteHeight == None:
            cls.spriteWidth = cls.spriteImgList[0].get_width();
            cls.spriteHeight = cls.spriteImgList[0].get_height();

    def setStartingFrame(self, frame=0):
        self.spriteIndex = frame;

    def setBoundaryRatio(self, boundaryRatio):
        self.boundaryRatio = min(1, max(0.5, boundaryRatio));

    def setPos(self, x, y):
        self.objectPos = [x, y];

    def __init__(self, url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio):
        super().__init__();

        self.fillImgList(url, fileName, indexLen, numFrames, ex);
        self.setStartingFrame();

        self.determineWidthAndHeight();
        self.setPos(x, y);
        self.setBoundaryRatio(boundaryRatio);
        self.updateBoundary();
        self.setObjID();

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updateSprite(keyBoardState, currentMousePos, currentMouseState);
        self.updatePos(globalSpeed, globalDisplacement);
        self.updateBoundary();

    def getSprite(self):
        return self.getSpriteList()[self.spriteIndex];

    def getPos(self):
        return self.objectPos;

    ####Secondary Functions

    @classmethod
    def getSpriteList(cls):
        return cls.spriteImgList;
    
    @classmethod
    def getSpriteWidth(cls):
        return cls.spriteWidth;

    @classmethod
    def getSpriteHeight(cls):
        return cls.spriteHeight;

    def centralizeAndDisplace(self, windowWidth, windowHeight, displaceX, displaceY):
        screenCenterX = windowWidth/2;
        screenCenterY = windowHeight/2;

        displaceY *= -1;

        self.objectPos = [screenCenterX - self.spriteWidth/2 + displaceX,
                          screenCenterY - self.spriteHeight/2 + displaceY];        

    def updateBoundary(self):

        objectPos = self.getPos();
        boundaryRatio = self.boundaryRatio;
        spriteWidth = self.getSpriteWidth();
        spriteHeight = self.getSpriteHeight();
        
        leftBoundPos = objectPos[0] + (1 - boundaryRatio) * spriteWidth;
        rightBound = objectPos[0] + boundaryRatio * spriteWidth;
        upperBoundPos = objectPos[1] + (1 - boundaryRatio) * spriteHeight;
        lowerBound = objectPos[1] + boundaryRatio * spriteHeight;

        boundaryWidth = rightBound - leftBoundPos;
        boundaryHeight = lowerBound - upperBoundPos;

        self.rect = pygame.Rect(leftBoundPos, upperBoundPos, boundaryWidth, boundaryHeight);

    def updateSprite(self, keyBoardState, currentMousePos, currentMouseState):
        #Modify self.spriteIndex
        pass;

    def updatePos(self, globalSpeed, globalDisplacement):
        #Modify self.rect.x and self.rect.y
        pass;

####Instance Classes

class Background(Object):

    ####Static Constants
    BORDER = 16;
    BOUNCE_VALUE = 5;

    ####Static Variables
    spriteRefreshDelay = 5;
    spriteLoopBackwards = False;
    
    ####Initialization Methods

    def determineCameraBoundaries(self):
        self.leftBound = 0 - self.BORDER;
        self.rightBound = self.getPos()[0]*2 + self.BORDER;
        self.upperBound = 0 - self.BORDER;
        self.lowerBound = self.getPos()[1]*2 + self.BORDER;

    def initializeControllers(self):
        self.globalSpeedController = SpeedController();
        self.globalDisplacementController = DisplacementController();

    def setAccelerationAndFriction(self, acceleration, friction):
        self.globalAcceleration = acceleration;
        self.globalFriction = friction;
    
    def __init__(self, windowWidth, windowHeight, acceleration, friction):

        url = urlConstructor(ART_ASSETS, MAIN_MENU);
        fileName = MAIN_MENU;
        indexLen = 3;
        numFrames = 6;
        ex = JPG_EX;
        x = 0;
        y = 0;
        boundaryRatio = 0.9;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio);

        self.setStartingFrame(0);
        self.setPos(-self.spriteWidth/2 + windowWidth/2, -self.spriteHeight/2 + windowHeight/2);
        self.determineCameraBoundaries();
        self.initializeControllers();
        self.setAccelerationAndFriction(acceleration, friction);

    ####Primary Methods
        
    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updateSprite();
        self.updatePos(keyBoardState);
    
    ####Secondary Methods

    ##Graphical
    def updateSprite(self):
        if self.spriteRefreshDelay >= 10:
            if self.spriteLoopBackwards == False:
                self.spriteIndex += 1;
                if self.spriteIndex >= len(self.spriteImgList):
                    self.spriteLoopBackwards = True;
                    self.spriteIndex -= 1;
            else:
                self.spriteIndex -= 1;
                if self.spriteIndex <= 0:
                    self.spriteLoopBackwards = False;
                    self.spriteIndex +=1;
                
            self.spriteRefreshDelay = 0;
        else:
            self.spriteRefreshDelay += 1;    
        
    ##Movement

    def getGlobalSpeed(self):
        return self.globalSpeedController;

    def getGlobalDisplacement(self):
        return self.globalDisplacementController;            
    
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
        self.objectPos[0] += -self.globalSpeedController.getNetHorizontalSpeed() + self.globalDisplacementController.getHorizontalDisplacement();
        self.objectPos[1] += -self.globalSpeedController.getNetVerticalSpeed() + self.globalDisplacementController.getVerticalDisplacement();    
         
    def updatePos(self, keyBoardState):
        self.adjustSpeedController(keyBoardState);
        self.checkBoundaries();
        self.snapCheck();
        self.moveBackground();
