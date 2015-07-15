from ObjectStorage import *;
from Object import *;

####Base Class

class Scene:

    ####Initialization Methods

    background = None;

    def __init__(self, windowWidth, windowHeight, background):
        self.windowWidth = windowWidth;
        self.windowHeight = windowHeight;
        self.background = background;
        
        self.currentObjectsInScene = ObjectStorage(background, windowWidth, windowHeight);
        GameObject.currentObjectStorage = self.currentObjectsInScene;

    def addObjectToScene(self, obj):
        self.currentObjectsInScene.determineAndAddObject(obj);

    def getObjectStorage(self):
        return self.currentObjectsInScene;

    def getAllObjectsInScene(self):
        return self.currentObjectsInScene.getAllObjects();      
    
    def update(self, keyBoardState, currentMousePos, currentMouseState):
        GameObject.currentObjectStorage = self.currentObjectsInScene;
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

        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 335, "Welcome to Space Arena!"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 300, "The objective of this game is to score"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 265, "as many points as possible by destroying"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 230, "enemy spacecrafts."));
        
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 185, "Use the WASD keys to pan the camera."));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 150, "Your ship will automatically move to the"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 115, "position of the mouse cursor, which"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 80, "also re-orients it along the direction"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 45, "it takes to travel to that point."));
        
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 0, "Left-Click to fire your main weapon."));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, -35, "Right-Click to fire your secondary weapon."));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, -70, "Q and E cycles through available secondary weapons."));

        self.addObjectToScene(Text(windowWidth, windowHeight, 0, -115, "Secondary Weapons are acquired when the"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, -150, "difficulty increases, which is determined"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, -185, "by certain score thresholds."));
        
        self.addObjectToScene(Button(windowWidth, windowHeight, 0, -250, BACK));

class Game(Scene):

    def __init__(self, windowWidth, windowHeight, background):
        super().__init__(windowWidth, windowHeight, background);
        self.currentObjectsInScene.gameMode = True;
        
        self.player = Player(windowWidth/2, windowHeight + 30);
        self.addObjectToScene(self.player);
        
        self.getObjectStorage().interface += [UIObj(self.windowWidth, self.windowHeight, 0, self.windowHeight/2 - 65), ];
        self.addObjectToScene(Text(windowWidth, windowHeight, -185, self.windowHeight/2 - 74, "HP"));
        
    def changeScene(self):
        if self.player.dead:
            return GAMEOVER;

class GameOver(Scene):

    def __init__(self, windowWidth, windowHeight, background, finalScore):
        super().__init__(windowWidth, windowHeight, background);

        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 245, "GAME OVER"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 215, "Final Score:"));
        self.addObjectToScene(Text(windowWidth, windowHeight, 0, 185, str(finalScore)));

        self.addObjectToScene(Button(windowWidth, windowHeight, 0, -10, BACK));
        
    
