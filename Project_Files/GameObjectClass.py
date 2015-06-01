import math;

from supplementary import *;
from SpeedController import *;
from DisplacementController import *;

####Base Classes

class GameObject:

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
        self.ID = str(self.getClassName()) + str(self.getObjNum());
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
    def getSpriteList(cls):
        return cls.spriteImgList;

    @classmethod
    def determineWidthAndHeight(cls):
        if cls.spriteWidth == None or cls.spriteHeight == None:
            cls.spriteWidth = cls.spriteImgList[0].get_width();
            cls.spriteHeight = cls.spriteImgList[0].get_height();

    @classmethod
    def getSpriteWidth(cls):
        return cls.spriteWidth;

    @classmethod
    def getSpriteHeight(cls):
        return cls.spriteHeight;

    def setBoundaryRatio(self, boundaryRatio):
        self.boundaryRatio = min(1, max(0.5, boundaryRatio));

    def setPosition(self, startX, startY):
        self.objectPos = [startX, startY];

    def __init__(self, url, fileName, indexLen, numFrames, ex, startX, startY, boundaryRatio):
        self.fillImgList(url, fileName, indexLen, numFrames, ex);
        self.determineWidthAndHeight();
        self.setBoundaryRatio(boundaryRatio);
        self.setPosition(startX, startY);

        self.setObjID();
        self.delete = False;
        self.fire = False;
        
    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement):
        self.updateSprite(keyBoardState, currentMousePos, currentMouseState);
        self.updatePos(globalSpeed, globalDisplacement);
        self.updateBoundary();

    def getSprite(self):
        return self.getSpriteList()[self.spriteIndex];

    def getPos(self):
        return tuple(self.objectPos);

    ####Secondary Functions

    def updateSprite(self, keyBoardState, currentMousePos, currentMouseState):
        pass;

    def updatePos(self, globalSpeed, globalDisplacement):
        pass;
    
    def updateBoundary(self):
        self.leftBound = self.objectPos[0] + (1 - self.boundaryRatio) * self.getSpriteWidth();
        self.rightBound = self.objectPos[0] + self.boundaryRatio * self.getSpriteWidth();
        self.upperBound = self.objectPos[1] + (1 - self.boundaryRatio) * self.getSpriteHeight();
        self.lowerBound = self.objectPos[1] + self.boundaryRatio * self.getSpriteHeight();

    def getIdentifier(self):
        return self.identifier;

    def setIdentifier(self, identifier):
        self.identifier = identifier;

    def destroyObj(self):
        self.delete = True;

class ShipBase(GameObject):

    def __init__(self, url, startX, startY, hitPoints):

        fileName = "";
        indexLen = 4;
        numFrames = 60;
        ex = PNG_EX;
        boundaryRatio = 0.75;

        super().__init__(url, fileName, indexLen, numFrames, ex, startX, startY, boundaryRatio);
        
        self.spriteIndex = 15;
        self.hitPoints = hitPoints;

    def destroy(self):
        return self.hitPoints <= 0;

    def fire(self):
        pass;

####Instance Classes

##Class Constants
PLAYER = "Player"
ENEMY = "Enemy"
BULLET = "Bullet"

class Player(ShipBase):

    def __init__(self, startX, startY):

        url = urlConstructor(ART_ASSETS, SHIPS, PLAYER_SHIP);
        hitPoints = 1000;

        super().__init__(url, startX, startY, hitPoints);

    ####Secondary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement):
        self.updateSprite(currentMousePos);
        self.updatePos(currentMousePos, globalSpeed, globalDisplacement);
        self.updateBoundary();

    def determineHorizontalDisplacement(self, currentMousePos):
        return currentMousePos[0] - (self.objectPos[0] + self.getSpriteWidth()/2);

    def determineVerticalDisplacement(self, currentMousePos):
        return currentMousePos[1] - (self.objectPos[1] + self.getSpriteHeight()/2);

    def approximateRotation(self, degrees):
        self.spriteIndex = min(59, int(degrees/360 * 60));

    def updateSprite(self, currentMousePos):
        xDis = self.determineHorizontalDisplacement(currentMousePos);
        yDis = -self.determineVerticalDisplacement(currentMousePos);
        hyp = math.hypot(xDis, yDis);

        if xDis > 0 and yDis > 0:
            self.approximateRotation(math.degrees(math.asin(yDis/hyp)));
        elif xDis < 0 and yDis > 0:
            self.approximateRotation(180 - math.degrees(math.asin(yDis/hyp)));
        elif xDis < 0 and yDis < 0:
            self.approximateRotation(180 + math.degrees(math.atan(yDis/xDis)));
        elif xDis > 0 and yDis < 0:
            self.approximateRotation(360 - math.degrees(math.acos(xDis/hyp)));
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

    def updatePos(self, currentMousePos, globalSpeed, globalDisplacement):

        xDis = self.determineHorizontalDisplacement(currentMousePos)/16;
        yDis = self.determineVerticalDisplacement(currentMousePos)/16;
        
        self.objectPos[0] += -globalSpeed.getNetHorizontalSpeed() + globalDisplacement.getHorizontalDisplacement() + xDis;
        self.objectPos[1] += -globalSpeed.getNetVerticalSpeed() + globalDisplacement.getVerticalDisplacement() + yDis;

    def fire(self, currentMouseState):
        if currentMouseState[0] == 1:
            pass;

    def getIdentifier(self):
        return PLAYER;
        
class EnemyShip1(ShipBase):

    def __init__(self, startX, startY):

        url = urlConstructor(ART_ASSETS, SHIPS, ENEMY_SHIP_1);

        super().__init__(url, startX, startY);
