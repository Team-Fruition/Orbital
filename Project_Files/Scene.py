from Object import *;

####Base Class

class Scene:

    background = None;

    def __init__(self, windowWidth, windowHeight, background):
        self.windowWidth = windowWidth;
        self.windowHeight = windowHeight;
        self.currentObjectsInScene = [];
        self.currentButtonsInScene = [];
        self.background = background;

        self.addObjectToScene(background);

    def addObjectToScene(self, obj):

        if isinstance(obj, Button):
            self.currentButtonsInScene.append(obj);
        
        self.currentObjectsInScene.append(obj);

    def getAllObjectsInScene(self):
        return self.currentObjectsInScene;
    
    def update(self, keyBoardState, currentMousePos, currentMouseState):

        self.background.update(keyBoardState, currentMousePos, currentMouseState);
        
        globalSpeed = self.background.getGlobalSpeed();
        globalDisplacement = self.background.getGlobalDisplacement();

        for item in self.currentObjectsInScene[1:]:
            item.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);

    def changeScene(self):
        for button in self.currentButtonsInScene:
            if button.clicked == True:
                return button.getName();
        else:
            return None;

####Sub-Classes

class MainMenu(Scene):

    def __init__(self, windowWidth, windowHeight, background):
        super().__init__(windowWidth, windowHeight, background);

        self.addObjectToScene(Logo(windowWidth, windowHeight, 0, 250, LOGO));
        self.addObjectToScene(Button(windowWidth, windowHeight, 0, 50, PLAY, PLAY));
        self.addObjectToScene(Button(windowWidth, windowHeight, 0, -50, HELP, HELP));

    def update(self, keyBoardState, currentMousePos, currentMouseState):

        self.background.update(keyBoardState, currentMousePos, currentMouseState);

        globalSpeed = [0, 0];
        globalDisplacement = [0, 0];

        for item in self.currentObjectsInScene[1:]:
            item.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);    


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
        
        self.addObjectToScene(Button(windowWidth, windowHeight, 0, -250, BACK, BACK));

    def update(self, keyBoardState, currentMousePos, currentMouseState):
        
        self.background.update(keyBoardState, currentMousePos, currentMouseState);

        globalSpeed = [0, 0];
        globalDisplacement = [0, 0];

        for item in self.currentObjectsInScene[1:]:
            item.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);

class Game(Scene):

    def __init__(self, windowWidth, windowHeight, background):

        super().__init__(windowWidth, windowHeight, background);

        self.addObjectToScene(Text(windowWidth, windowHeight, -windowWidth/2 + 50, windowHeight/2 - 25, "SCORE"));

    def changeScene(self):
        pass;
    
