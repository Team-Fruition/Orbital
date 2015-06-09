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

Group = pygame.sprite.Group;

class ObjectStorage:

    background = None;
    backgroundSpriteWidth = 0;
    backgroundSpriteHeight = 0;
    
    ####Initialization Methods

    def initializeGroups(self):        
        self.objectsToUpdate = Group();

        self.UIObject = Group();
        self.button = Group();
        self.ships = Group();
        self.bullets = Group();

    def initializeEnemies(self):
        self.enemyList = [Drone, ];
        self.spawnCounter = 0;
        self.spawnShip = 50;
        self.maxEnemySpawn = 10;

    def __init__(self, background, windowWidth, windowHeight):
        self.initializeGroups();
        self.initializeEnemies();
        
        self.background = background;
        self.backgroundSpriteWidth = self.background.spriteWidth;
        self.backgroundSpriteHeight = self.background.spriteHeight;
        self.windowWidth = windowWidth;
        self.windowHeight = windowHeight;

        self.score = 0;
        self.renderedScore = [];

        self.gameMode = False;

    ####Operations

    def getAllObjects(self):
        return [self.background, ] + self.bullets.sprites() + self.ships.sprites() + self.UIObject.sprites() + self.renderedScore;

    ##Generic Object Add

    def determineAndAddObject(self, obj):
        if isinstance(obj, Bullet):
            self.addBullet(obj);
        elif isinstance(obj, Ship):
            self.addShip(obj);
        elif isinstance(obj, UIElement):
            self.addUIObject(obj);
        else:
            pass;

    def addObjectToScene(self, obj):
        self.objectsToUpdate.add(obj);

    ##Button Object Add
    
    def addButton(self, button):
        self.button.add(button);
        self.addObjectToScene(button);

    ##UI Object Add

    def getButtons(self):
        return self.button.sprites();

    def addUIObject(self, UIobj):
        self.UIObject.add(UIobj);

        if isinstance(UIobj, Button):
            self.button.add(UIobj);

        self.addObjectToScene(UIobj);

    ##Ship Object Add

    def addShip(self, ship):
        self.ships.add(ship);

    def getShips(self):
        return self.ships.sprites();

    ##Bullet Object Add

    def addBullet(self, bullet):
        self.bullets.add(bullet);

    def getBullets(self):
        return self.bullet.sprites();

    def removeBullet(self, bullet):
        bullet.kill();

    def removeObjectFromScene(self, obj):
        obj.kill();

    ##Enemy Object

    def determineSpawnPoint(self):

        XBOUNDS = 128;
        YBOUNDS = 128;
        
        possibleValueX = [random.randrange(-XBOUNDS, 0), random.randrange(self.windowWidth, self.windowWidth + XBOUNDS)];
        possibleValueY = [random.randrange(-YBOUNDS, 0), random.randrange(self.windowHeight, self.windowHeight + YBOUNDS)];

        xIndex = random.randrange(0, 2);
        yIndex = random.randrange(0, 2);

        return [possibleValueX[xIndex], possibleValueY[yIndex]];

    def obtainRandomEnemyShip(self):
        return self.enemyList[random.randrange(0, len(self.enemyList))];

    def addEnemy(self):
        if self.spawnCounter >= self.spawnShip and len(self.ships.sprites()) <= self.maxEnemySpawn:
            self.spawnCounter = 0;
            self.spawnShip = random.randrange(50, 100);
            spawnPoint = self.determineSpawnPoint();
            self.addShip(self.obtainRandomEnemyShip()(spawnPoint[0], spawnPoint[1]));
        else:
            self.spawnCounter += 1;

    ##Main Update Function

    def updateScore(self):
        scoreString = str(self.score);
        bufferLen = 20 - len(scoreString);
        finalString = bufferLen * "0" + scoreString;
        self.renderedScore = [Text(self.windowWidth, self.windowHeight, -self.windowWidth/2 + 225, self.windowHeight/2 - 25, finalString), ];
            
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
            
            #Do Collision Checking here
            objects = collideGroups(self.ships, self.bullets, False, False, collided = collideRectRatio(0.5));

            for ship, bullets in objects.items():
                for bullet in bullets:
                    if bullet.firerType != ship.shipType:
                        ship.damage(bullet.damage);
                        if ship.dead == True:
                            self.score += ship.killScore;      
                        bullet.kill();

            #Perform other miscellaneous operations here
            self.addEnemy();
            self.updateScore();

        
