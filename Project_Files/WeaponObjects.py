from Object import *;
from BulletObjects import *;

####Base Classes

class Weapon:

    ####Initialization Methods

    def initializeBulletLoadout(self, *args):
        self.bulletLoadout = args;

    def __init__(self, firer, startingCounter = 45, counterMax = 60):
        self.firer = firer;
        self.initializeBulletLoadout(list());
        
        self.counterMax = counterMax;
        self.counter = startingCounter;

    ####Primary Functions
        
    def update(self):
        if self.counter >= self.counterMax:
            return;
        else:
            self.counter += 1;

    ####Secondary Functions

    def fire(self):
        return self.bulletLoadout;

####Instance Classes

class BasicWeapon(Weapon):

    ####Initialization Methods

    def __init__(self, firer):

        startingCounter = 15;
        counterMax = 45;
        
        super().__init__(firer, startingCounter, counterMax);
        self.initializeBulletLoadout(YellowProjectile);

    def fire(self):
        if self.counter >= self.counterMax:
            self.counter = 0;

            firer = self.firer;
            x = self.firer.objectPos[0] + self.firer.spriteWidth/2;
            y = self.firer.objectPos[1] + self.firer.spriteHeight/2;
            direction = self.firer.spriteIndex * 6;

            xOffSet = 10 * math.sin(math.radians(direction));
            yOffSet = 10 * math.cos(math.radians(direction));

            bulletList = list();

            bulletList.append(self.bulletLoadout[0](firer, x - xOffSet, y - yOffSet, direction));
            bulletList.append(self.bulletLoadout[0](firer, x + xOffSet, y + yOffSet, direction));
                               
            return bulletList;
        
        return list();

class DroneWeapon(Weapon):

    ####Initialization Methods

    def __init__(self, firer):

        startingCounter = 15;
        counterMax = 45;
        
        super().__init__(firer, startingCounter, counterMax);
        self.initializeBulletLoadout(YellowProjectile);

    def fire(self):
        if self.counter >= self.counterMax:
            self.counter = 0;

            firer = self.firer;
            x = self.firer.objectPos[0] + self.firer.spriteWidth/2;
            y = self.firer.objectPos[1] + self.firer.spriteHeight/2;
            direction = self.firer.spriteIndex * 6;

            xOffSet = 20 * math.sin(math.radians(direction));
            yOffSet = 20 * math.cos(math.radians(direction));

            bulletList = list();

            bulletList.append(self.bulletLoadout[0](firer, x - xOffSet, y - yOffSet, direction));
            bulletList.append(self.bulletLoadout[0](firer, x + xOffSet, y + yOffSet, direction));
                               
            return bulletList;
        
        return list();

class HailStorm(Weapon):

    ####Initialization Methods

    def __init__(self, firer):
        super().__init__(firer, 100, 125);
        self.initializeBulletLoadout(HailStormProjectile);

        self.alternateGunPort = False;

    def fire(self):
        if self.counter >= self.counterMax:
            self.counter = 0;

            firer = self.firer;
            x = self.firer.objectPos[0] + self.firer.spriteWidth/2;
            y = self.firer.objectPos[1] + self.firer.spriteHeight/2;
            direction = self.firer.spriteIndex * 6;

            xOffSet = 10 * math.sin(math.radians(direction));
            yOffSet = 10 * math.cos(math.radians(direction));            

            if self.alternateGunPort:
                xOffSet *= -1;
                yOffSet *= -1;

            self.alternateGunPort = not self.alternateGunPort;

            bulletList = list();

            for num in range(0, 15):
                bulletList.append(self.bulletLoadout[0](firer, x + xOffSet, y + yOffSet, direction));
            
            return bulletList;

        return list();


