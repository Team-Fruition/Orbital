import pygame;
import random;

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
    backgroundSpriteWidth = 0;
    backgroundSpriteHeight = 0;
    
    ####Initialization Methods

    def initializeGroups(self):        
        self.objectsToRender = Group();
        self.objectsToUpdate = Group();

        self.button = Group();
        self.ships = Group();
        self.bullets = Group();
        self.enemies = Group();

    def initializeEnemies(self):
        self.enemyList = [EnemyShip1, ];
        self.spawnCounter = 0;
        self.spawnShip = 50;
        self.maxEnemySpawn = 10;

    def __init__(self, background):
        self.initializeGroups();
        self.initializeEnemies();
        
        self.background = background;
        self.backgroundSpriteWidth = self.background.spriteWidth;
        self.backgroundSpriteHeight = self.background.spriteHeight;
        self.objectsToRender.add(background);

        self.gameMode = False;

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

    ##Enemy Object

    def obtainRandomEnemyShip(self):
        return self.enemyList[random.randrange(0, len(self.enemyList))];

    def addEnemy(self):
        if self.spawnCounter >= self.spawnShip and len(self.ships.sprites()) <= self.maxEnemySpawn:
            self.spawnCounter = 0;
            self.spawnShip = random.randrange(50, 100);
            self.addShip(self.obtainRandomEnemyShip()(random.randrange(0, 850), random.randrange(0, 850)));
        else:
            self.spawnCounter += 1;

    ##Main Update Function
            
    def updateAllObjects(self, keyBoardState, currentMousePos, currentMouseState):
        self.background.update(keyBoardState, currentMousePos, currentMouseState);
        
        globalSpeed = self.background.getGlobalSpeed();
        globalDisplacement = self.background.getGlobalDisplacement();

        self.objectsToUpdate.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);

        if self.gameMode:
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

                if not self.background.rect.collidepoint(ship.objectPos):
                    ship.kill();

            self.bullets.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
            
            #Do Collision Checking Here
            objects = collideGroups(self.ships, self.bullets, False, False, collided = collideRectRatio(0.5));

            for ship, bullets in objects.items():
                for bullet in bullets:
                    if bullet.firerType != ship.shipType:
                        ship.damage(bullet.damage);
                        bullet.kill();

            self.addEnemy();
        
