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
        return list();

    def adjustCounterMax(self, value):
        self.counterMax = value;

####Instance Classes

#Green Projectile

class XYGunLauncher(Weapon):

    ####Initialization Methods

    def __init__(self, firer):

        startingCounter = 5;
        counterMax = 150;

        super().__init__(firer, startingCounter, counterMax);

        import ShipObjects;
        
        self.initializeBulletLoadout(ShipObjects.XYGun);

    def fire(self):

        bulletList = list();

        if self.counter >= self.counterMax:
            self.counter = 0;

            x = self.firer.objectPos[0] + self.firer.spriteWidth/2;
            y = self.firer.objectPos[1] + self.firer.spriteHeight/2;
            shipType = self.firer.shipType;
            direction = self.firer.spriteIndex * 6;        
            
            bulletList.append(self.bulletLoadout[0](x, y, shipType, direction));

        return bulletList;
        
class XYGunWeapon(Weapon):

    ####Initialization Methods

    def __init__(self, firer):

        startingCounter = 0;
        counterMax = 0;

        super().__init__(firer, startingCounter, counterMax);
        self.initializeBulletLoadout(GreenProjectile);

    def fire(self):

        bulletList = list();

        if self.counter >= self.counterMax:
            self.counter = 0;

            firer = self.firer;
            x = self.firer.objectPos[0] + self.firer.spriteWidth/2;
            y = self.firer.objectPos[1] + self.firer.spriteHeight/2;
            direction = self.firer.spriteIndex * 6;        
            
            bulletList.append(self.bulletLoadout[0](firer, x, y, direction));

        return bulletList;

#Firecracker Projectile

class Firecracker(Weapon):

    ####Initialization Methods

    def __init__(self, firer):

        startingCounter = 100;
        counterMax = 125;

        super().__init__(firer, startingCounter, counterMax);
        self.initializeBulletLoadout(FirecrackerProjectile);

    def fire(self):

        bulletList = list();
        
        if self.counter >= self.counterMax:
            self.counter = 0;

            firer = self.firer;
            x = self.firer.objectPos[0] + self.firer.spriteWidth/2;
            y = self.firer.objectPos[1] + self.firer.spriteHeight/2;
            direction = self.firer.spriteIndex * 6;        
            
            bulletList.append(self.bulletLoadout[0](firer, x, y, direction));
            bulletList.append(self.bulletLoadout[0](firer, x, y, direction - 30));
            bulletList.append(self.bulletLoadout[0](firer, x, y, direction + 30));

        return bulletList;

class LethalFlowerWeapon(Weapon):

    ####Initialization Methods

    def __init__(self, firer):

        startingCounter = 100;
        counterMax = 175;

        super().__init__(firer, startingCounter, counterMax);
        self.initializeBulletLoadout(FirecrackerProjectile);

    def fire(self):

        bulletList = list();

        if self.counter >= self.counterMax:
            self.counter = 0;

            firer = self.firer;
            x = self.firer.objectPos[0] + self.firer.spriteWidth/2;
            y = self.firer.objectPos[1] + self.firer.spriteHeight/2;
            direction = self.firer.spriteIndex * 6;

            for num in range(0, 4):
                bulletList.append(self.bulletLoadout[0](firer, x, y, direction));
                direction += 90;

        return bulletList;

#Hailstorm Projectile
            
class HailStorm(Weapon):

    ####Initialization Methods

    def __init__(self, firer):

        startingCounter = 75;
        counterMax = 100;
        
        super().__init__(firer, startingCounter, counterMax);
        self.initializeBulletLoadout(HailStormProjectile);

        self.alternateGunPort = False;

    def fire(self):

        bulletList = list();

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
            
            for num in range(0, 15):
                bulletList.append(self.bulletLoadout[0](firer, x + xOffSet, y + yOffSet, direction));

        return bulletList;

class HailStormArtilleryWeapon(Weapon):
    
    ####Initialization Methods

    def __init__(self, firer):

        startingCounter = 75;
        counterMax = 260;
        
        super().__init__(firer, startingCounter, counterMax);
        self.initializeBulletLoadout(HailStormProjectile);

        self.alternateGunPort = False;

    def fire(self):

        bulletList = list();

        if self.counter >= self.counterMax:
            self.counter = 0;

            firer = self.firer;
            x = self.firer.objectPos[0] + self.firer.spriteWidth/2;
            y = self.firer.objectPos[1] + self.firer.spriteHeight/2;
            direction = self.firer.spriteIndex * 6 + random.randrange(-15, 15);

            xOffSet = 10 * math.sin(math.radians(direction));
            yOffSet = 10 * math.cos(math.radians(direction));            

            if self.alternateGunPort:
                xOffSet *= -1;
                yOffSet *= -1;

            self.alternateGunPort = not self.alternateGunPort;

            for num in range(0, 4):
                bulletList.append(self.bulletLoadout[0](firer, x + xOffSet, y + yOffSet, direction));
            
        return bulletList;

#Yellow Projectile

class BasicWeapon(Weapon):

    ####Initialization Methods

    def __init__(self, firer):

        startingCounter = 15;
        counterMax = 37;
        
        super().__init__(firer, startingCounter, counterMax);
        self.initializeBulletLoadout(YellowProjectile);

    def fire(self):

        bulletList = list();
        
        if self.counter >= self.counterMax:
            self.counter = 0;

            firer = self.firer;
            x = self.firer.objectPos[0] + self.firer.spriteWidth/2;
            y = self.firer.objectPos[1] + self.firer.spriteHeight/2;
            direction = self.firer.spriteIndex * 6;

            xOffSet = 10 * math.sin(math.radians(direction));
            yOffSet = 10 * math.cos(math.radians(direction));

            bulletList.append(self.bulletLoadout[0](firer, x - xOffSet, y - yOffSet, direction));
            bulletList.append(self.bulletLoadout[0](firer, x + xOffSet, y + yOffSet, direction));
                               
        return bulletList;

class DroneWeapon(Weapon):

    ####Initialization Methods

    def __init__(self, firer):

        startingCounter = 15;
        counterMax = 35;
        
        super().__init__(firer, startingCounter, counterMax);
        self.initializeBulletLoadout(YellowProjectile);

        self.alternateGunPort = True;

    def fire(self):

        bulletList = list();
        
        if self.counter >= self.counterMax:
            self.counter = 0;

            firer = self.firer;
            x = self.firer.objectPos[0] + self.firer.spriteWidth/2;
            y = self.firer.objectPos[1] + self.firer.spriteHeight/2;
            direction = self.firer.spriteIndex * 6;

            xOffSet = 20 * math.sin(math.radians(direction));
            yOffSet = 20 * math.cos(math.radians(direction));

            bulletList = list();

            if self.alternateGunPort:
                bulletList.append(self.bulletLoadout[0](firer, x - xOffSet, y - yOffSet, direction));
            else:
                bulletList.append(self.bulletLoadout[0](firer, x + xOffSet, y + yOffSet, direction));

            self.alternateGunPort = not self.alternateGunPort;
            
        return bulletList;
