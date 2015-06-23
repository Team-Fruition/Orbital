import math;
import random;

from Object import *;
from WeaponObjects import *;
from ItemObjects import *;

####Constants

TEAM_PLAYER = "Player";
TEAM_ENEMY = "Enemy";

####Base Classes

class Ship(GameObject):

    ####Initialization Methods

    def initializeWeapons(self, priWeapon, altWeapon):
        if priWeapon != None:
            self.priWeapon = priWeapon(self);
        else:
            self.priWeapon = None;

        if altWeapon != None:
            self.altWeapon = altWeapon(self);
        else:
            self.altWeapon = None;

    def initializeObjectGameVariables(self, hitPoints, priWeapon, altWeapon, killScore):
        self.hitPoints = hitPoints;
        self.initializeWeapons(priWeapon, altWeapon);
        self.killScore = killScore;
        
        self.firePrimary = False;
        self.fireSecondary = False;
        self.dead = False;

    def __init__(self, url, shipType, x, y, hitPoints, priWeapon = None, altWeapon = None, killScore = 0):

        fileName = "";
        indexLen = 4;
        numFrames = 60;
        ex = PNG_EX;
        boundaryRatio = 0.7;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio);

        self.shipType = shipType;

        self.setStartingFrame(15);
        
        self.initializeObjectGameVariables(hitPoints, priWeapon, altWeapon, killScore);

    ####Primary Functions
        
    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updateBoundary();
        self.updateWeapons();

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

    def updateWeapons(self):
        if self.getPrimaryWeapon() != None:
            self.getPrimaryWeapon().update();            
        if self.getSecondaryWeapon() != None:
            self.getSecondaryWeapon().update();

    def fireMain(self):
        if self.priWeapon != None:
            self.objectStorage.addBullet(self.priWeapon.fire());

    def fireAlternate(self):
        if self.altWeapon != None:
            self.objectStorage.addBullet(self.altWeapon.fire());

    def getPrimaryWeapon(self):
        return self.priWeapon;

    def getSecondaryWeapon(self):
        return self.altWeapon;

    def damage(self, value):
        if self.hitPoints > value:
            self.hitPoints -= value;
        else:
            self.dead = True;
            self.kill();

####Instance Classes

#Lethal Flower

class LethalFlower(Ship):

    ####Initialization Methods

    def __init__(self, x, y):

        url = urlConstructor(ART_ASSETS, SHIPS, LETHAL_FLOWER);
        shipType = TEAM_ENEMY;
        hitPoints = 350;
        priWeapon = LethalFlowerWeapon;
        altWeapon = None;
        killScore = 400;

        super().__init__(url, shipType, x, y, hitPoints, priWeapon, altWeapon, killScore);

        self.disCounter = 200;
        self.disCounterMax = 200;

        self.updateDis();

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        super().update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
        self.updateSprite();
        self.updateDis();
        self.updatePos(globalSpeed, globalDisplacement);
        self.fireMain();

    ####Secondary Functions

    def updateSprite(self):
        if self.spriteIndex >= self.imgListLen - 1:
            self.spriteIndex = 0;
        else:
            self.spriteIndex += 1;

    def updateDis(self):
        if self.disCounter >= self.disCounterMax:
            self.disCounter = 0;
            self.xDis = random.randrange(-1, 1);
            self.yDis = random.randrange(-1, 1);
        else:
            self.disCounter += 1;

    def updatePos(self, globalSpeed, globalDisplacement):
        globalHorizontalChange = -globalSpeed.getNetHorizontalSpeed() + globalDisplacement.getHorizontalDisplacement();
        globalVerticalChange = -globalSpeed.getNetVerticalSpeed() + globalDisplacement.getVerticalDisplacement();

        self.objectPos[0] += globalHorizontalChange + self.xDis;
        self.objectPos[1] += globalVerticalChange + self.yDis;

    def kill(self):
        self.objectStorage.addItem(Health(self));
        super().kill();

#Hailstorm Artillery
        
class HailstormArtillery(Ship):

    ####Initialization Methods

    def initCoordinatesSystem(self):
        self.currentCoordinatesCount = 0;
        self.updateCoordinatesCounter = 25;
        self.determineNewCoordinates();
    
    def __init__(self, x, y):

        url = urlConstructor(ART_ASSETS, SHIPS, HAILSTORM_ARTILLERY);
        shipType = TEAM_ENEMY;
        hitPoints = 75;
        priWeapon = HailStormArtilleryWeapon;
        altWeapon = None;
        killScore = 150;

        super().__init__(url, shipType, x, y, hitPoints, priWeapon, altWeapon, killScore);

        self.initCoordinatesSystem();
        
        self.dirty = False;

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        super().update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
        self.updateCoordinates();
        self.updateSprite(self.projectedCoordinates);
        self.updatePos(globalSpeed, globalDisplacement);
        self.fireMain();

    ####Secondary Functions

    def determineNewCoordinates(self):
        playerPos = self.objectStorage.player.objectPos;
        
        self.projectedCoordinates = list(playerPos);

    def updateCoordinates(self):
        if self.currentCoordinatesCount >= self.updateCoordinatesCounter:
            self.currentCoordinatesCount = 0;
            self.determineNewCoordinates();
        else:
            self.currentCoordinatesCount += 1;

    def updatePos(self, globalSpeed, globalDisplacement):

        globalHorizontalChange = -globalSpeed.getNetHorizontalSpeed() + globalDisplacement.getHorizontalDisplacement();
        globalVerticalChange = -globalSpeed.getNetVerticalSpeed() + globalDisplacement.getVerticalDisplacement();

        if not self.dirty:

            self.dirty = True;
            
            xDis = self.determineHorizontalDisplacement(self.projectedCoordinates)/256;
            yDis = self.determineVerticalDisplacement(self.projectedCoordinates)/256;

            self.projectedCoordinates[0] += globalHorizontalChange;
            self.projectedCoordinates[1] += globalVerticalChange;
            
            self.objectPos[0] += globalHorizontalChange + xDis;
            self.objectPos[1] += globalVerticalChange + yDis;

        else:
            
            self.objectPos[0] += globalHorizontalChange;
            self.objectPos[1] += globalVerticalChange;

#Drone
        
class Drone(Ship):

    ####Initialization Methods

    def initCoordinatesSystem(self):
        self.currentCoordinatesCount = 0;
        self.updateCoordinatesCounter = 100;
        self.determineNewCoordinates();
    
    def __init__(self, x, y):

        url = urlConstructor(ART_ASSETS, SHIPS, DRONE);
        shipType = TEAM_ENEMY;
        hitPoints = 100;
        priWeapon = DroneWeapon;
        altWeapon = None;
        killScore = 100;

        super().__init__(url, shipType, x, y, hitPoints, priWeapon, altWeapon, killScore);

        self.initCoordinatesSystem();

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        super().update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
        self.updateCoordinates();
        self.updateSprite(self.projectedCoordinates);
        self.updatePos(globalSpeed, globalDisplacement);
        self.fireMain();

    ####Secondary Functions

    def determineNewCoordinates(self):
        self.projectedCoordinates = [random.randrange(-250, 250) + self.objectPos[0],
                                     random.randrange(-250, 250) + self.objectPos[1]]         

    def updateCoordinates(self):
        if self.currentCoordinatesCount >= self.updateCoordinatesCounter:
            self.currentCoordinatesCount = 0;
            self.updateCoordinatesCounter = random.randrange(75, 125);
            self.determineNewCoordinates();
        else:
            self.currentCoordinatesCount += 1;

    def updatePos(self, globalSpeed, globalDisplacement):

        globalHorizontalChange = -globalSpeed.getNetHorizontalSpeed() + globalDisplacement.getHorizontalDisplacement();
        globalVerticalChange = -globalSpeed.getNetVerticalSpeed() + globalDisplacement.getVerticalDisplacement();
     
        xDis = self.determineHorizontalDisplacement(self.projectedCoordinates)/16;
        yDis = self.determineVerticalDisplacement(self.projectedCoordinates)/16;

        self.projectedCoordinates[0] += globalHorizontalChange;
        self.projectedCoordinates[1] += globalVerticalChange;
        
        self.objectPos[0] += globalHorizontalChange + xDis;
        self.objectPos[1] += globalVerticalChange + yDis;

#Player

class Player(Ship):

    ####Constants

    HITPOINTS = 1000;

    ####Initialization Methods

    def initializeMultipleWeaponCapability(self, startingWeapon):
        self.weaponList = [startingWeapon, ];
        self.weaponListIndex = 0;
        self.previousQInput = False;
        self.previousEInput = False;
        
    def __init__(self, x, y):

        url = urlConstructor(ART_ASSETS, SHIPS, PLAYER_SHIP);
        shipType = TEAM_PLAYER;
        hitPoints = self.HITPOINTS;
        priWeapon = BasicWeapon;
        altWeapon = HailStorm;

        super().__init__(url, shipType, x, y, hitPoints, priWeapon, altWeapon);

        self.initializeMultipleWeaponCapability(self.altWeapon);
        self.addNewWeapon(Firecracker);

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        super().update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
        self.updateSprite(currentMousePos);
        self.updatePos(currentMousePos, globalSpeed, globalDisplacement);
        self.checkIfSwapWeapons(keyBoardState);
        self.fireMain(currentMouseState);
        self.fireAlternate(currentMouseState);
        
    ####Secondary Functions

    def updatePos(self, currentMousePos, globalSpeed, globalDisplacement):

        xDis = self.determineHorizontalDisplacement(currentMousePos)/16;
        yDis = self.determineVerticalDisplacement(currentMousePos)/16;

        globalHorizontalChange = -globalSpeed.getNetHorizontalSpeed() + globalDisplacement.getHorizontalDisplacement();
        globalVerticalChange = -globalSpeed.getNetVerticalSpeed() + globalDisplacement.getVerticalDisplacement();
        
        self.objectPos[0] += globalHorizontalChange + xDis;
        self.objectPos[1] += globalVerticalChange + yDis;
    
    def checkIfSwapWeapons(self, keyBoardState):

        if keyBoardState["Q"] == True:
            if self.previousQInput == False:
                self.previousQInput = True;
                if self.weaponListIndex == 0:
                    self.weaponListIndex = len(self.weaponList) - 1;
                else:
                    self.weaponListIndex -= 1;
        else:
            self.previousQInput = False;
            
        if keyBoardState["E"] == True:
            if self.previousEInput == False:
                self.previousEInput = True;
                if self.weaponListIndex == len(self.weaponList) - 1:
                    self.weaponListIndex = 0;
                else:
                    self.weaponListIndex += 1;
        else:
            self.previousEInput = False;

        if keyBoardState["Q"] == False and keyBoardState["E"] == False:
            return;

        self.altWeapon = self.weaponList[self.weaponListIndex];

    def fireMain(self, currentMouseState):
        if currentMouseState[0] == 1:
            super().fireMain();

    def fireAlternate(self, currentMouseState):
        if currentMouseState[2] == 1:
            super().fireAlternate();

    def getSecondaryWeapon(self):
        return self.weaponList[self.weaponListIndex];

    def addNewWeapon(self, weapon):
        if issubclass(weapon, Weapon):
            self.weaponList.append(weapon(self));
