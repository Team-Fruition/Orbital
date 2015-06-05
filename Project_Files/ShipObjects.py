from Object import *;
from WeaponObjects import *;

####Base Classes

class Ship(GameObject):

    ####Initialization Methods

    def __init__(self, url, x, y, hitPoints, priWeapon = None, altWeapon = None):

        fileName = "";
        indexLen = 4;
        numFrames = 60;
        ex = PNG_EX;
        boundaryRatio = 0.7;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio);

        self.setStartingFrame(15);
        
        self.hitPoints = hitPoints;
        self.priWeapon = priWeapon;
        self.altWeapon = altWeapon;
        
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

    def fireMain(self):
        self.firePrimary = False;

    def fireAlternate(self):
        self.fireSecondary = False;

    def getPrimaryWeapon(self):
        return self.priWeapon;

    def getSecondaryWeapon(self):
        return self.altWeapon;

    def damage(self, value):
        if self.hitpoints > value:
            self.hitpoints -= value;
        else:
            self.dead = True;
            self.kill();

####Instance Classes

#Player

class Player(Ship):

    ####Initialization Methods

    def initializeMultipleWeaponCapability(self, startingWeapon):
        self.weaponList = [startingWeapon, ];
        self.weaponListIndex = 0;
        self.previousQInput = False;
        self.previousEInput = False;
        
    def __init__(self, x, y):

        url = urlConstructor(ART_ASSETS, SHIPS, PLAYER_SHIP);
        hitPoints = 1000;
        priWeapon = BasicWeapon(self);
        altWeapon = None;

        super().__init__(url, x, y, hitPoints, priWeapon, altWeapon);

        self.initializeMultipleWeaponCapability(altWeapon);

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updateSprite(currentMousePos);
        self.updatePos(currentMousePos, globalSpeed, globalDisplacement);
        self.updateBoundary();
        self.checkIfSwapWeapons(keyBoardState);
        self.fireMain(currentMouseState);
        self.fireAlternate(currentMouseState);
        self.getPrimaryWeapon().update();
        
    ####Secondary Functions

    def updatePos(self, currentMousePos, globalSpeed, globalDisplacement):

        xDis = self.determineHorizontalDisplacement(currentMousePos)/16;
        yDis = self.determineVerticalDisplacement(currentMousePos)/16;
        
        self.objectPos[0] += -globalSpeed.getNetHorizontalSpeed() + globalDisplacement.getHorizontalDisplacement() + xDis;
        self.objectPos[1] += -globalSpeed.getNetVerticalSpeed() + globalDisplacement.getVerticalDisplacement() + yDis;

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
            self.firePrimary = True;
        else:
            self.firePrimary = False;

    def fireAlternate(self, currentMouseState):
        if currentMouseState[2] == 1:
            self.fireSecondary = True;
        else:
            self.fireSecondary = False;

    def getSecondaryWeapon(self):
        return self.weaponList[self.weaponListIndex];
