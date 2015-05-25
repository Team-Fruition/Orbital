from supplementary import *;
from Background import *;
from Scene import *;

class SceneManager:

    allScenes = [];

    #Scene Indexes
    MAIN_MENU = 0;
    HELP = 1;
    GAME = 2;
    GAMEOVER = 3;

    #Variables
    currentScene = MAIN_MENU;

    def __init__(self, windowWidth, windowHeight, acceleration, friction):

        #Load Background
        background = Background(windowWidth, windowHeight, acceleration, friction);
        
        #Load Scenes here
        self.addScene(MainMenu(windowWidth, windowHeight, background));
        
        pass;

    def addScene(self, scene):
        self.allScenes.append(scene);

    def changeState(self, newScene):
        self.currentScene = newScene;        

    def getCurrentScene(self):
        return self.allScenes[self.currentScene];

    def getObjectsToRender(self):
        return self.getCurrentScene().getAllObjectsInScene();

    def update(self, keyBoardState, currentMousePos, currentMouseState):
        self.getCurrentScene().update(keyBoardState, currentMousePos, currentMouseState);

    #Add Button Logic Here
