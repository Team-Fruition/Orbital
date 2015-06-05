from Object import *;

####Base Classes

class Bullet(GameObject):

    ####Assumptions
    #self.direction is in degrees (i.e. ship.spriteIndex * 60 is passed in as the argument to bullet.updateDirection()

    ####Initialization Methods

    def centralizeBulletFromGivenPoint(self, x, y):
        self.setPos(x - self.spriteWidth/2, y - self.spriteHeight/2);
        
    def __init__(self, url, firer, damage, x, y, speedMult, direction):

        fileName = "";
        indexLen = 4;
        numFrames = 1;
        ex = PNG_EX;
        boundaryRatio = 0.7;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio);
        self.centralizeBulletFromGivenPoint(x, y);
        self.updateBoundary();

        self.killCounter = 0;
        self.killCounterMax = 150;
        
        self.updateFirer(firer);
        self.updateDamage(damage);
        self.updateSpeed(speedMult);        
        self.updateDirection(direction);

        self.determineSpeedVector();

    ####Primary Functions
        
    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updatePos(globalSpeed, globalDisplacement);
        self.updateBoundary();
        self.updateKillCounter();

    ####Secondary Functions

    def updateKillCounter(self):
        if self.killCounter >= self.killCounterMax:
            self.kill();
        else:
            self.killCounter += 1;

    def updateFirer(self, firer):
        self.firer = firer;

    def updateDamage(self, damage):
        self.damage = damage;

    def updateSpeed(self, speedMult):
        self.speedMult = speedMult;

    def updateDirection(self, direction):
        self.direction = direction;

    def determineSpeedVector(self):
        #Modify self.localSpeed here

        radDirection = math.radians(self.direction);
        
        speedx = 1 * self.speedMult * math.cos(radDirection);
        speedy = 1 * self.speedMult * math.sin(radDirection);

        self.localSpeed.adjustHorizontalSpeed(speedx, True);
        self.localSpeed.adjustVerticalSpeed(speedy, True);

    def updatePos(self, globalSpeed, globalDisplacement):
        #Modify self.objectPos
        self.objectPos[0] += (-globalSpeed.getNetHorizontalSpeed() + self.localSpeed.getNetHorizontalSpeed()
                              + globalDisplacement.getHorizontalDisplacement() + self.localDisplacement.getHorizontalDisplacement());
        self.objectPos[1] += (-globalSpeed.getNetVerticalSpeed() + self.localSpeed.getNetVerticalSpeed()
                              + globalDisplacement.getVerticalDisplacement() + self.localDisplacement.getVerticalDisplacement());

####Instance Classes

#Yellow Projectile

class YellowProjectile(Bullet):

    ####Initialization Methods

    def __init__(self, firer, x, y, direction):

        url = urlConstructor(ART_ASSETS, PROJECTILES, YELLOW_PROJECTILE);
        damage = 30;
        speedMult = 10;

        super().__init__(url, firer, damage, x, y, speedMult, direction);
        
