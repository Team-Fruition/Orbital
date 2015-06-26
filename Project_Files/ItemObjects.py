from Object import *;

####Base Classes

class Item(GameObject):

    ####Initialization Methods

    def __init__(self, url, x, y, speedMult, direction):

        fileName = "";
        indexLen = 3;
        numFrames = 11;
        ex = PNG_EX;
        boundaryRatio = 0.7;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio);
        self.updateBoundary();
        
        self.spriteRefreshDelay = 0;
        self.spriteLoopBackwards = False;
        
        self.killCounter = 0;
        self.killCounterMax = 150;

        self.speedMult = speedMult;
        self.direction = direction;
        self.determineSpeedVector();

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updatePos(globalSpeed, globalDisplacement);
        self.updateBoundary();
        self.updateKillCounter();
        self.updateLocalSpeed();
        self.updateSprite();

    ####Secondary Functions

    def determineSpeedVector(self):
        #Modify self.localSpeed here

        radDirection = math.radians(self.direction);
        
        speedx = 1 * self.speedMult * math.cos(radDirection);
        speedy = 1 * self.speedMult * math.sin(radDirection);

        self.localSpeed.adjustHorizontalSpeed(speedx, True);
        self.localSpeed.adjustVerticalSpeed(speedy, True);

    def updateKillCounter(self):
        if self.killCounter >= self.killCounterMax:
            self.kill();
        else:
            self.killCounter += 1;

    def updateLocalSpeed(self):
        self.localSpeed.applyFriction(0.5);

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

####Instance Classes

##Health

class Health(Item):

    ####Initialization Methods

    def __init__(self, dropper):

        url = urlConstructor(ART_ASSETS, DROPS, HEALTH);
        x = dropper.objectPos[0] + dropper.spriteWidth/2;
        y = dropper.objectPos[1] + dropper.spriteHeight/2;
        speedMult = 1;
        direction = dropper.spriteIndex;

        super().__init__(url, x, y, speedMult, direction);

        self.objectPos[0] -= self.spriteWidth/2;
        self.objectPos[1] -= self.spriteHeight/2;

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        super().update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);

    ####Secondary Functions

    def effect(self, ship):
        if ship.hitPoints <= 1200:
            ship.hitPoints += 100;
        else:
            ship.hitPoints = 1200;

        
