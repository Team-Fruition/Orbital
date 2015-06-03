import pygame;

from collections import OrderedDict;

####Class Variables

Group = pygame.sprite.OrderedUpdates;

from Object import *;

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

    def determineObjClass(self, obj):
        pass;

    def addObjectToScene(self, obj):
        self.objectsToRender.add(obj);
        self.objectsToUpdate.add(obj);

    def addButton(self, button):
        self.button.add(button);
        self.addObjectToScene(button);

    def getButtons(self):
        return self.button.sprites();

    def addShip(self, ship):
        self.ships.add(ship);
        self.addObjToScene(ship);

    def getShips(self):
        return self.ships.sprites();

    def addBullet(self, bullet):
        self.bullets.add(bullet);
        self.addObjectToScene(bullet);

    def removeObjectFromScene(self, obj):
        obj.kill();

    def getClassDictionary(self, cls):
        pass;

    def spawnShip(self):
        pass;

    def updateAllObjects(self, keyBoardState, currentMousePos, currentMouseState):
        self.background.update(keyBoardState, currentMousePos, currentMouseState);
        
        globalSpeed = self.background.getGlobalSpeed();
        globalDisplacement = self.background.getGlobalDisplacement();

        self.objectsToUpdate.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);

           
        
