import pygame;
import random;

from Object import *;
from UIObjects import *;
from ShipObjects import *;
from WeaponObjects import *;
from BulletObjects import *;
from ItemObjects import *;

####Function Executables

collideRectRatio = pygame.sprite.collide_rect_ratio;
collideGroups = pygame.sprite.groupcollide;
collideSprite = pygame.sprite.spritecollide;

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
        self.items = Group();

    def initializeEnemies(self):
        self.spawnCounter = 0;
        self.spawnShip = 50;

        self.enemyCount = 0;        
        self.maxEnemySpawn = 10;

        testEnemyList = [];
        enemyList0 = [Drone, ];
        enemyList1 = [Drone, Drone, Drone, Drone, HailstormArtillery];
        enemyList2 = [Drone, Drone, Drone, HailstormArtillery, HailstormArtillery];
        enemyList3 = [Drone, Drone, HailstormArtillery, HailstormArtillery, LethalFlower];

        self.allEnemyLists = [enemyList0, enemyList1, enemyList2, enemyList3];
        self.currentDifficultyLevel = 0;

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

        self.renderedHealth = [];

        self.gameMode = False;

    ####Operations

    def getAllObjects(self):
        return ([self.background, ] + self.bullets.sprites() + self.ships.sprites()
                + self.items.sprites() + self.UIObject.sprites() + self.renderedScore + self.renderedHealth);

    ##Generic Object Add

    def determineAndAddObject(self, obj):
        if isinstance(obj, Bullet):
            self.addBullet(obj);
        elif isinstance(obj, Ship):
            self.addShip(obj);
        elif isinstance(obj, Item):
            self.addItem(obj);            
        elif isinstance(obj, UIElement):
            self.addUIObject(obj);
        else:
            pass;

    def determineAndAddListOfObjects(self, objList):
        for item in objList:
            self.determineAndAddObject(item);

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

    def addPlayer(self, player):
        self.player = player;
        
    def addShip(self, ship):
        if isinstance(ship, Player):
            self.addPlayer(ship);
        
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

    ##Item Object Add

    def addItem(self, item):
        self.items.add(item);

    def getItems(self):
        return self.items.sprites();

    ##Enemy Object

    def upgradeDifficulty(self):
        if self.currentDifficultyLevel < len(self.allEnemyLists) - 1:
            self.currentDifficultyLevel += 1;

    def determineSpawnPoint(self):
        XBOUNDS = 256;
        YBOUNDS = 256;
        
        possibleValueX = [random.randrange(-XBOUNDS, 0), random.randrange(self.windowWidth, self.windowWidth + XBOUNDS)];
        possibleValueY = [random.randrange(-YBOUNDS, 0), random.randrange(self.windowHeight, self.windowHeight + YBOUNDS)];

        xIndex = random.randrange(0, 2);
        yIndex = random.randrange(0, 2);

        return [possibleValueX[xIndex], possibleValueY[yIndex]];

    def getEnemyList(self):
        return self.allEnemyLists[self.currentDifficultyLevel];

    def obtainRandomEnemyShip(self):
        enemyList = self.getEnemyList();
        
        return enemyList[random.randrange(0, len(enemyList))];

    def addEnemy(self):
        if self.spawnCounter >= self.spawnShip and self.enemyCount <= self.maxEnemySpawn:
            self.spawnCounter = 0;
            self.enemyCount += 1;
            self.spawnShip = random.randrange(50, 100);
            spawnPoint = self.determineSpawnPoint();
            self.addShip(self.obtainRandomEnemyShip()(spawnPoint[0], spawnPoint[1]));
        else:
            self.spawnCounter += 1;

    ##Main Update Function

    def updateScore(self):
        scoreString = str(self.score);
        bufferLen = 20 - len(scoreString);
        if bufferLen >= 0:
            finalString = bufferLen * "0" + scoreString;
            self.renderedScore = [Text(self.windowWidth, self.windowHeight, -self.windowWidth/2 + 225, self.windowHeight/2 - 25, finalString), ];

    def updateHealth(self):
        healthString = str(int(self.player.hitPoints/self.player.HITPOINTS * 100));
        bufferLen = 3 - len(healthString);
        if bufferLen >= 0:
            finalString = bufferLen * "0" + healthString;
            self.renderedHealth = [Text(self.windowWidth, self.windowHeight, -self.windowWidth/2 + 490, self.windowHeight/2 - 25, finalString), ];

    def updateDifficulty(self):
        if self.score >= 1000 and self.currentDifficultyLevel == 0:
            self.upgradeDifficulty();
        elif self.score >= 2000 and self.currentDifficultyLevel == 1:
            self.upgradeDifficulty();
        elif self.score >= 3500 and self.currentDifficultyLevel == 2:
            self.upgradeDifficulty();
        elif self.score >= 5000 and self.currentDifficultyLevel == 3:
            self.upgradeDifficulty();

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

                if not self.background.rect.collidepoint(ship.objectPos):
                    ship.kill();

            self.bullets.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
            self.items.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
            
            #Do Collision Checking here
            objects = collideGroups(self.ships, self.bullets, False, False, collided = collideRectRatio(0.5));

            for ship, bullets in objects.items():         
                for bullet in bullets:
                    if bullet.firerType != ship.shipType:
                        ship.damage(bullet.damage);   
                        bullet.kill();                       
                if ship.dead == True:
                    self.score += ship.killScore;

            items = collideSprite(self.player, self.items, True, collided = collideRectRatio(0.6));

            for item in items:
                item.effect(self.player);

            #Perform other miscellaneous operations here
            self.addEnemy();
            self.updateScore();
            self.updateHealth();
            self.updateDifficulty();
