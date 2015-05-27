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
        
        #globalSpeed = self.background.getGlobalSpeed();
        #globalDisplacement = self.background.getGlobalDisplacement();

        globalSpeed = [0, 0];
        globalDisplacement = [0, 0];

        for item in self.currentObjectsInScene[1:]:
            item.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);    


class HelpMenu(Scene):

    def __init__(self, windowWidth, windowHeight, background):
        super().__init__(windowWidth, windowHeight, background);

        self.addObjectToScene(Button(windowWidth, windowHeight, 0, -250, BACK, BACK));

    def update(self, keyBoardState, currentMousePos, currentMouseState):
        
        self.background.update(keyBoardState, currentMousePos, currentMouseState);

        globalSpeed = [0, 0];
        globalDisplacement = [0, 0];

        for item in self.currentObjectsInScene[1:]:
            item.update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);

    
