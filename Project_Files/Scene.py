from Object import *;

####Base Class

class Scene:

    background = None;

    def __init__(self, windowWidth, windowHeight, background):
        self.windowWidth = windowWidth;
        self.windowHeight = windowHeight;
        self.currentObjectsInScene = [];
        self.background = background;

        self.addObjectToScene(background);

    def addObjectToScene(self, obj):
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
        pass;

####Sub-Classes

class MainMenu(Scene):

    def __init__(self, windowWidth, windowHeight, background):
        super().__init__(windowWidth, windowHeight, background);

        self.addObjectToScene(Logo(windowWidth, windowHeight, 0, 250, "Logo"));
        self.addObjectToScene(Button(windowWidth, windowHeight, 0, 50, "Play", PLAY));
        self.addObjectToScene(Button(windowWidth, windowHeight, 0, -50, "Help", HELP));

    def update(self, keyBoardState, currentMousePos, currentMouseState):

        self.background.update(keyBoardState, currentMousePos, currentMouseState);
        
        globalSpeed = self.background.getGlobalSpeed();
        globalDisplacement = self.background.getGlobalDisplacement();

        for item in self.currentObjectsInScene[1:]:
            item.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);    
