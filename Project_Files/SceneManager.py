from supplementary import *;
from Object import Background;
from Scene import *;

class SceneManager:

    allScenes = dict();

    #Variables
    currentScene = START;

    def __init__(self, windowWidth, windowHeight, acceleration, friction):

        #Load Background
        self.windowWidth = windowWidth;
        self.windowHeight = windowHeight;
        self.background = Background(windowWidth, windowHeight, acceleration, friction);
        
        #Load Scenes here
        
        mainMenu = MainMenu(windowWidth, windowHeight, self.background);
        self.addScene(START, mainMenu);

        helpScreen = HelpMenu(windowWidth, windowHeight, self.background);
        self.addScene(INSTRUCTIONS, helpScreen);

    def addScene(self, state, scene):
        self.allScenes[state] = scene;

    def changeState(self, newScene):
        self.currentScene = newScene;        

    def getCurrentScene(self):
        return self.allScenes[self.currentScene];

    def getObjectsToRender(self):
        return self.getCurrentScene().getAllObjectsInScene();

    #Screen Logic
    def determineSceneChange(self):
        
        #Main Menu Button Logic
        if self.currentScene == START:
            if self.getCurrentScene().changeScene() == PLAY:
                self.addScene(GAME, Game(self.windowWidth, self.windowHeight, self.background));
                self.changeState(GAME);
            elif self.getCurrentScene().changeScene() == HELP:
                self.changeState(INSTRUCTIONS);

        #Help Screen Button Logic
        #Keep below as an elif check
        elif self.currentScene == INSTRUCTIONS:
            if self.getCurrentScene().changeScene() == BACK:
                self.changeState(START);

        #Game Screen Logic
        elif self.currentScene == GAME:
            if self.getCurrentScene().changeScene() == True:
                self.changeState(START);
        
    def update(self, keyBoardState, currentMousePos, currentMouseState):
        self.getCurrentScene().update(keyBoardState, currentMousePos, currentMouseState);

        self.determineSceneChange();
