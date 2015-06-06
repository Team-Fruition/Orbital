import pygame;

from Object import *;
from UIObjects import *;
from ShipObjects import *;
from WeaponObjects import *;
from BulletObjects import *;

####Function Executables

collideRectRatio = pygame.sprite.collide_rect_ratio;
collideGroups = pygame.sprite.groupcollide;

####Class Variables

Group = pygame.sprite.OrderedUpdates;

class ObjectStorage:

    background = None;
    
    ####Initialization Methods

    def initializeGroups(self):        
        self.objectsToRender = Group();
        self.objectsToUpdate = Group();

        self.button = Group();
        self.ships = Group();
        self.bullets = Group();

    def __init__(self, background):
        self.initializeGroups();
        self.background = background;
        self.objectsToRender.add(background);

    ####Operations

    def getAllObjects(self):
        return self.objectsToRender.sprites();

    ##Generic Object Add

    def addObjectToScene(self, obj):
        self.objectsToRender.add(obj);
        self.objectsToUpdate.add(obj);

    ##Button Object Add
    
    def addButton(self, button):
        self.button.add(button);
        self.addObjectToScene(button);

    def getButtons(self):
        return self.button.sprites();

    ##Ship Object Add

    def addShip(self, ship):
        self.ships.add(ship);
        self.objectsToRender.add(ship);

    def getShips(self):
        return self.ships.sprites();

    ##Bullet Object Add

    def addBullet(self, bullet):
        self.bullets.add(bullet);
        self.objectsToRender.add(bullet);

    def getBullets(self):
        return self.bullet.sprites();

    def removeBullet(self, bullet):
        bullet.kill();

    def removeObjectFromScene(self, obj):
        obj.kill();

    def spawnShip(self):
        pass;

    def updateAllObjects(self, keyBoardState, currentMousePos, currentMouseState):
        self.background.update(keyBoardState, currentMousePos, currentMouseState);
        
        globalSpeed = self.background.getGlobalSpeed();
        globalDisplacement = self.background.getGlobalDisplacement();

        self.objectsToUpdate.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);

        #Do Ship and Bullet updates here
        shipsList = self.getShips();

        for ship in shipsList:
            ship.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
            
            if ship.firePrimary == True:
                bulletList = ship.getPrimaryWeapon().fire();
                self.addBullet(bulletList);                    
            if ship.fireSecondary == True:
                bulletList = ship.getSecondaryWeapon().fire();
                self.addBullet(bulletList);

        self.bullets.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
        
        #Do Collision Checking Here
        objects = collideGroups(self.ships, self.bullets, False, False, collided = collideRectRatio(0.5));

        for ship, bullets in objects.items():
            for bullet in bullets:
                if bullet.firer != ship:
                    ship.damage(bullet.damage);
                    bullet.kill();
        
