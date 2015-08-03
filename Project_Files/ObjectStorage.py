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
        self.alliedShips = Group();
        self.enemyShips = Group();

        self.bullets = Group();
        self.alliedBullets = Group();
        self.enemyBullets = Group();
        
        self.items = Group();

    def initializeEnemies(self):

        self.enemy = Group();
        
        self.spawnCounter = 0;
        self.spawnShip = 50;
 
        self.maxEnemySpawn = 10;

        testEnemyList = [];
        enemyList0 = [Drone, ];
        enemyList1 = [Drone, Drone, HailstormArtillery];
        enemyList2 = [Drone, Drone, Drone, HailstormArtillery, HailstormArtillery];
        enemyList3 = [Drone, Drone, HailstormArtillery, HailstormArtillery, LethalFlower];
        enemyList4 = [Drone, HailstormArtillery, HailstormArtillery, LethalFlower];
        enemyList5 = [HailstormArtillery, HailstormArtillery, HailstormArtillery, LethalFlower];

        self.allEnemyLists = [enemyList0, enemyList1, enemyList2, enemyList3, enemyList4, enemyList5];
        self.currentDifficultyLevel = 0;

    def initializeDifficultyThresholds(self):

        self.scoreAdvancement = {};

        self.scoreAdvancement["-1"] = (0, None);
        self.scoreAdvancement["0"] = (1500, HailStorm);
        self.scoreAdvancement["1"] = (3000, None);
        self.scoreAdvancement["2"] = (4500, None);
        self.scoreAdvancement["3"] = (5750, Firecracker);
        self.scoreAdvancement["4"] = (8000, XYGunLauncher);

    def __init__(self, background, windowWidth, windowHeight):
        
        self.initializeGroups();
        self.initializeEnemies();
        self.initializeDifficultyThresholds();
        
        self.background = background;
        self.backgroundSpriteWidth = self.background.spriteWidth;
        self.backgroundSpriteHeight = self.background.spriteHeight;
        self.windowWidth = windowWidth;
        self.windowHeight = windowHeight;

        self.score = 0;
        self.renderedScore = [];

        self.renderedHealth = [];

        self.renderedDifficulty = [];

        self.gameMode = False;

        self.interface = [];

    ####Operations

    def getAllObjects(self):
        return ([self.background, ] + self.bullets.sprites() + self.ships.sprites()
                + self.items.sprites() + self.renderedScore + self.renderedHealth
                + self.interface + self.renderedDifficulty + self.UIObject.sprites());

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

    def getButtons(self):
        return self.button.sprites();

    ##UI Object Add

    def addUIObject(self, UIobj):
        self.UIObject.add(UIobj);

        if isinstance(UIobj, Button):
            self.button.add(UIobj);

        self.addObjectToScene(UIobj);

    ##Ship Object Add

    def addPlayer(self, player):
        self.player = player;

    def addAlliedShip(self, ship):
        self.alliedShips.add(ship);

    def addEnemyShip(self, ship):
        self.enemyShips.add(ship);
        
    def addShip(self, ship):
        if ship.shipType == TEAM_PLAYER:
            self.addAlliedShip(ship);
        elif ship.shipType == TEAM_ENEMY:
            self.addEnemyShip(ship);
        
        if isinstance(ship, Player):
            self.addPlayer(ship);
        
        self.ships.add(ship);

    def addListOfShips(self, listShips):
        for ship in listShips:
            self.addShip(ship);

    def getShips(self):
        return self.ships.sprites();

    ##Bullet Object Add

    def addAlliedBullets(self, bullet):
        self.alliedBullets.add(bullet);

    def addEnemyBullets(self, bullet):
        self.enemyBullets.add(bullet);

    def addBullet(self, bullet):

        if bullet.firerType == TEAM_PLAYER:
            self.addAlliedBullets(bullet);
        elif bullet.firerType == TEAM_ENEMY:
            self.addEnemyBullets(bullet);

        self.bullets.add(bullet);

    def addListOfBullets(self, listBullets):
        for bullet in listBullets:
            self.addBullet(bullet);

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
        XBOUNDS = 2;
        YBOUNDS = 2;
        SHIPSIZE = 128;
        
        possibleValueX = [random.randrange(-XBOUNDS, 0), random.randrange(self.windowWidth - SHIPSIZE - XBOUNDS, self.windowWidth - SHIPSIZE)];
        possibleValueY = [random.randrange(-YBOUNDS, 0), random.randrange(self.windowHeight - SHIPSIZE - YBOUNDS, self.windowHeight - SHIPSIZE)];

        xIndex = random.randrange(0, 2);
        yIndex = random.randrange(0, 2);

        firstPossibleSet = [possibleValueX[xIndex], possibleValueY[yIndex]];
        secondPossibleSet = [random.randrange(0, self.windowWidth - SHIPSIZE), random.randrange(0 + SHIPSIZE, self.windowHeight)];

        return secondPossibleSet;

    def getEnemyList(self):
        return self.allEnemyLists[self.currentDifficultyLevel];

    def obtainRandomEnemyShip(self):
        enemyList = self.getEnemyList();
        
        return enemyList[random.randrange(0, len(enemyList))];

    def addEnemy(self):
        if self.spawnCounter >= self.spawnShip and len(self.enemy.sprites()) < self.maxEnemySpawn:
            self.spawnCounter = 0;
            self.spawnShip = random.randrange(50, 100);
            spawnPoint = self.determineSpawnPoint();

            ship = self.obtainRandomEnemyShip()(spawnPoint[0], spawnPoint[1])
            self.addShip(ship);
            self.enemy.add(ship);
            
        else:
            self.spawnCounter += 1;

    ##Main Update Function

    def updateScore(self):
        
        displaceX = 0;
        displaceY = self.windowHeight/2 - 65;

        self.renderedScore = [ProgressBarBacking(self.windowWidth, self.windowHeight, displaceX, displaceY),
                              ProgressBar(self.windowWidth, self.windowHeight, displaceX, displaceY), ];

    def updateHealth(self):

        displaceX = 0;
        displaceY = self.windowHeight/2 - 65;
        
        self.renderedHealth = [HPBarBacking(self.windowWidth, self.windowHeight, displaceX, displaceY),
                               HPBar(self.windowWidth, self.windowHeight, displaceX, displaceY, self.player), ];

    def updateDifficulty(self):

        difficultyString = str(self.currentDifficultyLevel);

        bufferLen = 2 - len(difficultyString);
        if bufferLen >= 0:
            finalString = bufferLen * "0" + difficultyString;
            self.renderedDifficulty = [Text(self.windowWidth, self.windowHeight, 195, self.windowHeight/2 - 74, finalString), ];

        if difficultyString in self.scoreAdvancement:
            levelData = self.scoreAdvancement[difficultyString];

            if self.score >= levelData[0]:
                self.upgradeDifficulty();
                self.player.addNewWeapon(levelData[1]);

    def processCollisions(self, objects):
        for ship, bullets in objects.items():         
            for bullet in bullets:
                if bullet.firerType != ship.shipType:
                    ship.damage(bullet.damage);   
                    bullet.kill();                       
            if ship.dead == True:
                self.score += ship.killScore;        

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

                if not isinstance(ship, Player) and not self.background.rect.colliderect(ship.rect):
                    ship.killCleanly();

            self.bullets.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
            self.items.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
            
            #Do Collision Checking here
            objects = collideGroups(self.alliedShips, self.enemyBullets, False, False, collided = collideRectRatio(0.5));

            self.processCollisions(objects);

            objects = collideGroups(self.enemyShips, self.alliedBullets, False, False, collided = collideRectRatio(0.5));

            self.processCollisions(objects);

            items = collideSprite(self.player, self.items, True, collided = collideRectRatio(0.6));

            for item in items:
                item.effect(self.player);

            #Perform other miscellaneous operations here
            self.addEnemy();
            self.updateScore();
            self.updateHealth();
            self.updateDifficulty();
