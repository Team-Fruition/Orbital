from Object import *;
from supplementary import *;

####Base Classes

class Bullet(GameObject):

    ####Constants
    fileName = "";
    indexLen = 4;
    numFrames = 1;
    ex = PNG_EX;
    boundaryRatio = 0.7;

    playerBulletSprite = None;

    ####Assumptions
    #self.direction is in degrees (i.e. ship.spriteIndex * 60 is passed in as the argument to bullet.updateDirection()

    ####Player Projectile Setting

    @classmethod
    def initPlayerBulletSprite(cls):
        if cls.playerBulletSprite == None:
            url = urlConstructor(ART_ASSETS, PROJECTILES, WHITE_PROJECTILE);
            indexingVariable = 10 ** (cls.indexLen);
            cls.playerBulletSprite = loadImg(url, cls.fileName + str(indexingVariable)[1:] + cls.ex);

    ####Initialization Methods

    def centralizeBulletFromGivenPoint(self, x, y):
        self.setPos(x - self.spriteWidth/2, y - self.spriteHeight/2);
        
    def __init__(self, url, firer, damage, x, y, speedMult, direction):

        self.initPlayerBulletSprite();
        
        super().__init__(url, self.fileName, self.indexLen, self.numFrames, self.ex, x, y, self.boundaryRatio);
        self.centralizeBulletFromGivenPoint(x, y);
        self.updateBoundary();

        self.killCounter = 0;
        self.killCounterMax = 150;
        
        self.firer = firer;
        self.firerType = self.firer.shipType;
        self.damage = damage;
        self.speedMult = speedMult;
        self.direction = direction;

        self.determineSpeedVector();

    ####Primary Functions
        
    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updatePos(globalSpeed, globalDisplacement);
        self.updateBoundary();
        self.updateKillCounter();

    ####Secondary Functions

    def getSprite(self):
        if self.firerType == TEAM_PLAYER:
            return self.playerBulletSprite;
        else:
            return super().getSprite();

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

##Green Projectile

class GreenProjectile(Bullet):

    ####Initialization Methods

    def __init__(self, firer, x, y, direction):

        url = urlConstructor(ART_ASSETS, PROJECTILES, GREEN_PROJECTILE);
        damage = 10;
        speedMult = 20;

        super().__init__(url, firer, damage, x, y, speedMult, direction);

        self.killCounterMax = 75;

##Firecracker Projectile

class FirecrackerProjectile(Bullet):

    ####Initialization Methods

    def __init__(self, firer, x, y, direction):

        url = urlConstructor(ART_ASSETS, PROJECTILES, PINK_PROJECTILE);
        damage = 40;
        speedMult = 7;

        self.originalDirection = direction;

        super().__init__(url, firer, damage, x, y, speedMult, direction);

        self.killCounterMax = 50;

        self.spawnCounter = 0;
        self.spawnCounterMax = 2;

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updatePos(globalSpeed, globalDisplacement);
        self.updateBoundary();
        self.updateKillCounter();
        self.updateSpawnCounter();

    ####Secondary Functions

    def updateSpawnCounter(self):
        if self.spawnCounter >= self.spawnCounterMax:
            self.spawnCounter = 0;

            firer = self.firer;
            x = self.objectPos[0] + self.spriteWidth/2;
            y = self.objectPos[1] + self.spriteHeight/2;
            direction = random.randrange(0, 360);

            bulletList = list();

            for counter in range(0, 4):
                bulletList.append(SubFirecrackerProjectile(firer, x, y, direction));
                direction += 90;

            self.objectStorage.addListOfBullets(bulletList);
            
        else:
            self.spawnCounter += 1;        

class SubFirecrackerProjectile(Bullet):

    ####Initialization Methods

    def __init__(self, firer, x, y, direction):

        url = urlConstructor(ART_ASSETS, PROJECTILES, PINK_PROJECTILE);
        damage = 5;
        speedMult = 5;

        super().__init__(url, firer, damage, x, y, speedMult, direction);
        
        self.killCounterMax = 10;

##Hailstorm Projectile

class HailStormProjectile(Bullet):

    ####Initialization Methods

    def __init__(self, firer, x, y, direction):

        url = urlConstructor(ART_ASSETS, PROJECTILES, BLUE_PROJECTILE);
        damage = 7;
        speedMult = random.randrange(10, 20);

        self.speedUp = False;
        self.originalDirection = direction;
        direction += random.randrange(-45, 45);

        super().__init__(url, firer, damage, x, y, speedMult, direction);

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updateSpeed();
        self.determineSpeedVector();
        self.updatePos(globalSpeed, globalDisplacement);
        self.updateBoundary();
        self.updateKillCounter();

    ####Secondary Functions

    def updateSpeed(self):
        if self.speedUp:
            self.speedMult += 0.3;
        else:
            self.speedMult -= 1;
            if self.speedMult <= 0:
                self.speedUp = True;
                self.updateDirection(self.originalDirection);

##Basic Projectile

class YellowProjectile(Bullet):

    ####Initialization Methods

    def __init__(self, firer, x, y, direction):

        url = urlConstructor(ART_ASSETS, PROJECTILES, YELLOW_PROJECTILE);
        damage = 30;
        speedMult = 10;

        super().__init__(url, firer, damage, x, y, speedMult, direction);
        

    
