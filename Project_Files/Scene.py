from collections import OrderedDict;

from UIClass import *;
from GameObjectClass import *;

####Base Class

class Scene:

    ####Object ID Methods
    numText = -1;
    numButtons = -1;
    numShips = -1;
    numBullets = -1;

    @classmethod
    def getTextID(cls):
        cls.numText += 1;
        return cls.numText;

    @classmethod
    def getButtonID(cls):
        cls.numButtons += 1;
        return cls.numButtons;

    @classmethod
    def getShipsID(cls):
        cls.numShips += 1;
        return cls.numShips;

    @classmethod
    def getBulletID(cls):
        cls.numBullets += 1;
        return cls.numBullets;

    def setObjIdentifier(self, obj):
        className = obj.__class__.__name__;
        
        if isinstance(obj, ShipBase) and not isinstance(obj, Player):
            obj.setIdentifier(className + str(self.getShipsID()));
        elif isinstance(obj, Text):
            obj.setIdentifier(className + str(self.getTextID()));
        elif isinstance(obj, Button):
            obj.setIdentifier(className + str(self.getButtonID()));

    ####Initialization Methods

    background = None;

    def __init__(self, windowWidth, windowHeight, background):
        self.windowWidth = windowWidth;
        self.windowHeight = windowHeight;
        self.currentObjectsInScene = OrderedDict();
        self.background = background;

        self.addObjectToScene(background);

    def addObjectToScene(self, obj):
        self.setObjIdentifier(obj);
        self.currentObjectsInScene[obj.getIdentifier()] = obj;

    def getAllObjectsInScene(self):
        return self.currentObjectsInScene.items();      
    
    def update(self, keyBoardState, currentMousePos, currentMouseState):

        self.background.update(keyBoardState, currentMousePos, currentMouseState);
        
        globalSpeed = [0, 0];
        globalDisplacement = [0, 0];

        for item in tuple(self.getAllObjectsInScene())[1:]:
            item[1].update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);

    def changeScene(self):
        for counter in range(0, self.numButtons + 1):
            buttonObj = self.currentObjectsInScene[str(Button.__name__) + str(counter)];
            if buttonObj.clicked == True:
                return buttonObj.getName();
                

####Sub-Classes

class MainMenu(Scene):

    def __init__(self, windowWidth, windowHeight, background):
        super().__init__(windowWidth, windowHeight, background);

        self.addObjectToScene(Logo(windowWidth, windowHeight, 0, 250));
        self.addObjectToScene(Button(windowWidth, windowHeight, 0, 50, PLAY));
        self.addObjectToScene(Button(windowWidth, windowHeight, 0, -50, HELP));    


class HelpMenu(Scene):

    def __init__(self, windowWidth, windowHeight, background):
        super().__init__(windowWidth, windowHeight, background);

        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 300, "Welcome to Space Arena!"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 265, "The objective of this game is to eliminate"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 230, "the enemies trying to attack your ship."));
        
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 175, "Use the WASD keys to pan the window."));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 140, "Your ship will automatically move to the"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 105, "position of the mouse cursor, which"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 70, "also re-orients it along the direction"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 35, "it takes to travel to that point."));
        
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, -20, "Left-Click to fire your main weapon."));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, -55, "Right-Click to fire your secondary weapon."));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, -90, "Q and E cycles through available secondary weapons."));
        
        self.addObjectToScene(Button(windowWidth, windowHeight, 0, -250, BACK));

class Game(Scene):

    def __init__(self, windowWidth, windowHeight, background):

        super().__init__(windowWidth, windowHeight, background);

        self.addObjectToScene(Text(windowWidth, windowHeight, -windowWidth/2 + 55, windowHeight/2 - 25, "SCORE: "));
        self.addObjectToScene(Player(windowWidth/2, windowHeight/2));

    def update(self, keyBoardState, currentMousePos, currentMouseState):

        self.background.update(keyBoardState, currentMousePos, currentMouseState);
        
        globalSpeed = self.background.getGlobalSpeed();
        globalDisplacement = self.background.getGlobalDisplacement();

        for item in tuple(self.getAllObjectsInScene())[1:]:
            item[1].update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
        
    def changeScene(self):
        pass;
    
