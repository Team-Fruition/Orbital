from ObjectStorage import *;
from Object import *;

####Base Class

class Scene:

    ####Initialization Methods

    background = None;

    def __init__(self, windowWidth, windowHeight, background):
        self.windowWidth = windowWidth;
        self.windowHeight = windowHeight;
        self.currentObjectsInScene = ObjectStorage(background);
        self.background = background;

    def addObjectToScene(self, obj):
        if isinstance(obj, Bullet):
            self.currentObjectsInScene.addBullet(obj);
        elif isinstance(obj, Ship):
            self.currentObjectsInScene.addShip(obj);
        elif isinstance(obj, Button):
            self.currentObjectsInScene.addButton(obj);
        else:
            self.currentObjectsInScene.addObjectToScene(obj);

    def getAllObjectsInScene(self):
        return self.currentObjectsInScene.getAllObjects();      
    
    def update(self, keyBoardState, currentMousePos, currentMouseState):
        self.currentObjectsInScene.updateAllObjects(keyBoardState, currentMousePos, currentMouseState);

    def changeScene(self):
        buttons = self.currentObjectsInScene.getButtons();

        for button in buttons:
            if button.clicked == True:
                return button.getName();
                

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

        self.player = Player(windowWidth/2, windowHeight + 30);
        self.addObjectToScene(self.player);
        
    def changeScene(self):
        if self.player.dead:
            return GAMEOVER;
    
