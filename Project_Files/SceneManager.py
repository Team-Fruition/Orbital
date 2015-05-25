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

    def addScene(self, state, scene):
        self.allScenes[state] = scene;

    def changeState(self, newScene):
        self.currentScene = newScene;        

    def getCurrentScene(self):
        return self.allScenes[self.currentScene];

    def getObjectsToRender(self):
        return self.getCurrentScene().getAllObjectsInScene();

    def update(self, keyBoardState, currentMousePos, currentMouseState):
        self.getCurrentScene().update(keyBoardState, currentMousePos, currentMouseState);

    #Add Button Logic Here
