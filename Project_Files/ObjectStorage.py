from collections import OrderedDict;

from UIClass import *;
from GameObjectClass import *;

class ObjectStorage:

    background = None;
    
    ####Initialization Methods

    def __init__(self, background):
        self.currentObjectsInScene = OrderedDict();
        self.background = background;
        self.addObjectToScene(background);

    ####Operations

    def getStorage(self):
        return self.currentObjectsInScene;

    def addObjectToScene(self, obj):
        currentKeys = self.getStorage().keys();
        objClass = obj.__class__.__name__;
        objID = obj.getObjID();
        
        for key in currentKeys:
            if key == objClass:
                self.currentObjectsInScene[key][objID] = obj;
                return;
        else:
            self.currentObjectsInScene[objClass] = OrderedDict();
            self.currentObjectsInScene[objClass][objID] = obj;

    def removeObjectFromScene(self, obj):
        objClass = obj.__class__.__name__;
        objID = obj.getObjID();

        del self.currentObjectsInScene[objClass][objID];

    def getClassDictionary(self, cls):
        return self.currentObjectsInScene[cls.__name__];

    def updateAllObjects(self, keyBoardState, currentMousePos, currentMouseState):
        self.background.update(keyBoardState, currentMousePos, currentMouseState);
        
        globalSpeed = self.background.getGlobalSpeed();
        globalDisplacement = self.background.getGlobalDisplacement();

        for classDict in tuple(self.getStorage().items())[1:]:
            for item in tuple(classDict[1].items()):
                item[1].update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
            
        
