class Scene:

    background = None;

    currentObjectsInScene = [];

    def __init__(self, background):
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
