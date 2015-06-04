import pygame;
import math;

from supplementary import *;
from DisplacementController import *;
from SpeedController import *;

####Function Executables

rectGenerator = pygame.Rect;

####Base Classes

class GameObject(pygame.sprite.Sprite):

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

    ####Initialization Methods
    
    @classmethod
    def fillImgList(cls, url, fileName, indexLen, numFrames, ex):
        if cls.spriteImgList == None:
            cls.spriteImgList = [];
            indexingVariable = 10 ** (indexLen);
            for index in range(0, numFrames):
                cls.spriteImgList.append(loadImg(url, fileName + str(indexingVariable + index)[1:] + ex));

    @classmethod
    def determineWidthAndHeight(cls):
        if cls.spriteWidth == None or cls.spriteHeight == None:
            cls.spriteWidth = cls.spriteImgList[0].get_width();
            cls.spriteHeight = cls.spriteImgList[0].get_height();

    def setBoundaryRatio(self, boundaryRatio):
        self.boundaryRatio = min(1, max(0.5, boundaryRatio));

    def setStartingFrame(self, frame=0):
        self.spriteIndex = frame;

    def setPos(self, x, y):
        self.objectPos = [x, y];

    def initSpeedAndDisplacementControllers(self):
        self.localSpeed = SpeedController();
        self.localDisplacement = DisplacementController();

    def __init__(self, url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio):
        super(GameObject, self).__init__();

        self.fillImgList(url, fileName, indexLen, numFrames, ex);
        self.setStartingFrame();

        self.setBoundaryRatio(boundaryRatio);

        self.determineWidthAndHeight();
        self.setPos(x, y);
        
        self.setObjID();

    ####Primary Functions
        
    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        pass;
    
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

    def updateSprite(self, keyBoardState, currentMousePos, currentMouseState):
        #Modify self.spriteIndex
        pass;

    def updatePos(self, globalSpeed, globalDisplacement):
        #Modify self.objectPos
        self.objectPos[0] += -globalSpeed.getNetHorizontalSpeed() + globalDisplacement.getHorizontalDisplacement();
        self.objectPos[1] += -globalSpeed.getNetVerticalSpeed() + globalDisplacement.getVerticalDisplacement();

    def updateBoundary(self):
        #Modify self.rect
        self.rect = rectGenerator(tuple(self.objectPos), (self.getSpriteWidth(), self.getSpriteHeight()));

class UIElement(GameObject):

    ####Initialization Methods

    def fillImgList(self, url, fileName, indexLen, numFrames, ex):
        self.spriteImgList = [];
        indexingVariable = 10 ** (indexLen);
        for index in range(0, numFrames):
            self.spriteImgList.append(loadImg(url, fileName + str(indexingVariable + index)[1:] + ex));

    def determineWidthAndHeight(self):
        self.spriteWidth = self.spriteImgList[0].get_width();
        self.spriteHeight = self.spriteImgList[0].get_height();

    def __init__(self, url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio,
                 windowWidth, windowHeight, displaceX, displaceY):
        
        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio);
        self.centralizeAndDisplace(windowWidth, windowHeight, displaceX, displaceY);

    ####Secondary Functions
        
    def getSpriteList(self):
        return self.spriteImgList;
    
    def getSpriteWidth(self):
        return self.spriteWidth;

    def getSpriteHeight(self):
        return self.spriteHeight;

    def centralizeAndDisplace(self, windowWidth, windowHeight, displaceX, displaceY):
        screenCenterX = windowWidth/2;
        screenCenterY = windowHeight/2;

        displaceY *= -1;

        self.objectPos = [screenCenterX - self.spriteWidth/2 + displaceX,
                          screenCenterY - self.spriteHeight/2 + displaceY];      

class Ship(GameObject):

    ####Initialization Methods

    def __init__(self, url, x, y, hitPoints, weapon = None):

        fileName = "";
        indexLen = 4;
        numFrames = 60;
        ex = PNG_EX;
        boundaryRatio = 0.7;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio);

        self.setStartingFrame(15);
        self.initSpeedAndDisplacementControllers();
        
        self.hitPoints = hitPoints;
        self.weapon = weapon;
        
        self.firePrimary = False;
        self.fireSecondary = False;
        self.dead = False;

    ####Primary Functions
        
    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        pass;

    ####Secondary Functions
    
    def approximateRotation(self, degrees):
        return min(59, int(degrees/360 * 60));    
    
    def determineHorizontalDisplacement(self, XYcoordinates):
        return XYcoordinates[0] - (self.objectPos[0] + self.getSpriteWidth()/2);

    def determineVerticalDisplacement(self, XYcoordinates):
        return XYcoordinates[1] - (self.objectPos[1] + self.getSpriteHeight()/2);

    def updateSprite(self, coordinates):
        xDis = self.determineHorizontalDisplacement(coordinates);
        yDis = -self.determineVerticalDisplacement(coordinates);
        hyp = math.hypot(xDis, yDis);

        if xDis > 0 and yDis > 0:
            self.spriteIndex = self.approximateRotation(math.degrees(math.asin(yDis/hyp)));
        elif xDis < 0 and yDis > 0:
            self.spriteIndex = self.approximateRotation(180 - math.degrees(math.asin(yDis/hyp)));
        elif xDis < 0 and yDis < 0:
            self.spriteIndex = self.approximateRotation(180 + math.degrees(math.atan(yDis/xDis)));
        elif xDis > 0 and yDis < 0:
            self.spriteIndex = self.approximateRotation(360 - math.degrees(math.acos(xDis/hyp)));
        elif xDis == 0 and yDis > 0:
            self.spriteIndex = 15;
        elif xDis == 0 and yDis < 0:
            self.spriteIndex = 45;
        elif xDis > 0 and yDis == 0:
            self.spriteIndex = 0;
        elif xDis < 0 and yDis == 0:
            self.spriteIndex = 30;
        elif xDis == 0 and yDis == 0:
            return;

    def updatePos(self):
        #Modify self.objectPos
        self.objectPos[0] += -globalSpeed.getNetHorizontalSpeed() + globalDisplacement.getHorizontalDisplacement();
        self.objectPos[1] += -globalSpeed.getNetVerticalSpeed() + globalDisplacement.getVerticalDisplacement();        

    def fireMain(self):
        self.firePrimary = False;

    def fireAlternate(self):
        self.fireSecondary = False;

    def damage(self, value):
        if self.hitpoints > value:
            self.hitpoints -= value;
        else:
            self.dead = True;
            self.kill();

class Bullet(GameObject):

    ####Initialization Methods

    def __init__(self, url, x, y):

        indexLen = 4;
        numFrames = 1;
        ex = PNG_EX;
        boundaryRatio = 0.7;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio);

class Weapon:

    ####Initialization Methods

    def __init__(self, ship):
        self.ship = ship;

####Instance Classes

##Game Objects

#Player

class Player(Ship):

    ####Initialization Methods

    def __init__(self, x, y):

        url = urlConstructor(ART_ASSETS, SHIPS, PLAYER_SHIP);
        hitPoints = 1000;
        weapon = None;

        super().__init__(url, x, y, hitPoints, weapon);

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updateSprite(currentMousePos);
        self.updatePos(currentMousePos, globalSpeed, globalDisplacement);
        self.updateBoundary();
        self.fireMain(currentMouseState);
        self.fireAlternate(currentMouseState);
        
    ####Secondary Functions

    def updatePos(self, currentMousePos, globalSpeed, globalDisplacement):

        xDis = self.determineHorizontalDisplacement(currentMousePos)/16;
        yDis = self.determineVerticalDisplacement(currentMousePos)/16;
        
        self.objectPos[0] += -globalSpeed.getNetHorizontalSpeed() + globalDisplacement.getHorizontalDisplacement() + xDis;
        self.objectPos[1] += -globalSpeed.getNetVerticalSpeed() + globalDisplacement.getVerticalDisplacement() + yDis;

    def fireMain(self, currentMouseState):
        if currentMouseState[0] == 1:
            self.firePrimary = True;
        else:
            self.firePrimary = False;

    def fireAlternate(self, currentMouseState):
        if currentMouseState[2] == 1:
            self.fireSecondary = True;
        else:
            self.fireSecondary = False;
            
##UI Elements

#Button

class Button(UIElement):

    ####Constants
    INACTIVE = 0;
    ACTIVE = 1;

    ####Initialization Methods

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

        self.rect = rectGenerator(leftBoundPos, upperBoundPos, boundaryWidth, boundaryHeight);       

    def __init__(self, windowWidth, windowHeight, displaceX, displaceY, buttonConstant):
        
        url = urlConstructor(ART_ASSETS, BUTTON);
        fileName = buttonConstant;
        indexLen = 2;
        numFrames = 2;
        ex = PNG_EX;
        x = 0;
        y = 0;
        boundaryRatio = 0.7;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio,
                         windowWidth, windowHeight, displaceX, displaceY);
        self.updateBoundary();

        self.name = buttonConstant;
        self.clicked = False;

    ####Primary Functions
        
    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updateSprite(currentMousePos);
        self.determineIfClicked(currentMousePos, currentMouseState);
    
    ####Secondary Functions

    def checkIfMouseWithinBounds(self, currentMousePos):
        return self.rect.collidepoint(currentMousePos) == 1;

    def checkIfMouseLeftClicked(self, currentMouseState):
        return currentMouseState[0] == 1;

    def updateSprite(self, currentMousePos):
        if self.checkIfMouseWithinBounds(currentMousePos):
            self.spriteIndex = self.ACTIVE;
        else:
            self.spriteIndex = self.INACTIVE;

    def determineIfClicked(self, currentMousePos, currentMouseState):
        self.clicked = (self.checkIfMouseWithinBounds(currentMousePos)
                        and self.checkIfMouseLeftClicked(currentMouseState));

    def getName(self):
        return self.name;

#Logo
        
class Logo(UIElement):

    ####Initialization Methods

    def __init__(self, windowWidth, windowHeight, displaceX, displaceY):
        
        url = urlConstructor(ART_ASSETS, LOGO);
        fileName = LOGO;
        indexLen = 3;
        numFrames = 1;
        ex = PNG_EX;
        x = 0;
        y = 0;
        boundaryRatio = 1;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio,
                         windowWidth, windowHeight, displaceX, displaceY);
    
#Text

class Text(UIElement):

    ####Constants
    
    TEXTCOLOR = (255, 255, 255);      

    ####Initialization Methods

    def loadFont(rootURL, fontSize):
        pygame.font.init();
        return pygame.font.Font(rootURL, fontSize);

    gameFont = loadFont(urlConstructor(ART_ASSETS, FONTS, STYLE + TTF_EX), 25);

    def fillImgList(self, textContent):
        self.spriteImgList = [];
        self.setStartingFrame();
        self.listLen = 1;
        self.spriteImgList.append(self.gameFont.render(textContent, True, self.TEXTCOLOR));
        
    def __init__(self, windowWidth, windowHeight, displaceX, displaceY, textContent):
        pygame.sprite.Sprite.__init__(self);
        self.fillImgList(textContent);
        self.determineWidthAndHeight();
        self.centralizeAndDisplace(windowWidth, windowHeight, displaceX, displaceY);

        self.setObjID();

    ####Secondary Functions

    def getSpriteList(self):
        return self.spriteImgList;

#Background

class Background(GameObject):

    ####Static Constants
    
    BORDER = 16;
    BOUNCE_VALUE = 5;

    ####Static Variables
    
    spriteRefreshDelay = 5;
    spriteLoopBackwards = False;
    
    ####Initialization Methods

    @classmethod
    def fillImgList(cls, url, fileName, indexLen, numFrames, ex):
        if cls.spriteImgList == None:
            cls.spriteImgList = [];
            indexingVariable = 10 ** (indexLen);
            for index in range(0, numFrames):
                cls.spriteImgList.append(loadImg(url, fileName + str(indexingVariable + index)[1:] + ex));

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

    ####Primary Functions
        
    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updateSprite();
        self.updatePos(keyBoardState);
    
    ####Secondary Functions

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
