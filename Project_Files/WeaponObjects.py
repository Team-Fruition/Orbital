from Object import *;
from BulletObjects import *;

####Base Classes

class Weapon:

    ####Initialization Methods

    def initializeBulletLoadout(self, *args):
        self.bulletLoadout = args;

    def __init__(self, firer):
        self.firer = firer;
        self.initializeBulletLoadout(list());

    ####Secondary Functions

    def fire(self):
        return self.bulletLoadout;

    def update(self):
        pass;

####Instance Classes

class BasicWeapon(Weapon):

    ####Initialization Methods

    def __init__(self, firer):
        super().__init__(firer);
        self.initializeBulletLoadout(YellowProjectile);

        self.counterMax = 75;
        self.counter = 45;

    def fire(self):
        if self.counter >= self.counterMax:
            self.counter = 0;

            firer = self.firer;
            x = self.firer.objectPos[0] + self.firer.spriteWidth/2;
            y = self.firer.objectPos[1] + self.firer.spriteHeight/2;
            direction = self.firer.spriteIndex * 6;

            bulletList = list();

            for item in self.bulletLoadout:
                bulletList.append(item(firer, x, y, direction));
                               
            return bulletList;
        
        return list();

    def update(self):
        if self.counter == self.counterMax:
            return;
        else:
            self.counter += 1;
