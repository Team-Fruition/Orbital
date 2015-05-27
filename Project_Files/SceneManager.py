from supplementary import *;
from Background import *;
from Scene import *;

class SceneManager:

    allScenes = dict();

    #Variables
    currentScene = START;

    def __init__(self, windowWidth, windowHeight, acceleration, friction):

        #Load Background
        background = Background(windowWidth, windowHeight, acceleration, friction);
        
        #Load Scenes here
        
        mainMenu = MainMenu(windowWidth, windowHeight, background);
        self.addScene(START, mainMenu);

        helpScreen = HelpMenu(windowWidth, windowHeight, background);
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
                print("Play Button Clicked");
            if self.getCurrentScene().changeScene() == HELP:
                self.changeState(INSTRUCTIONS);

        #Help Screen Button Logic
        elif self.currentScene == INSTRUCTIONS:
            if self.getCurrentScene().changeScene() == BACK:
                self.changeState(START);
        
    def update(self, keyBoardState, currentMousePos, currentMouseState):
        self.getCurrentScene().update(keyBoardState, currentMousePos, currentMouseState);

        self.determineSceneChange();
