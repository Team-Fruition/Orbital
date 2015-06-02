from collections import OrderedDict;

##from UIClass import *;
##from GameObjectClass import *;

from Object import *;

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

    def determineObjClass(self, obj):
        pass;

    def addObjectToScene(self, obj):
        
        storage = self.getStorage();

        objClass = obj.__class__.__name__;
        objID = obj.getObjID();
        
        if objClass not in storage:
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

        tupleOfObjects = tuple(self.getStorage().items());
        for classDict in tupleOfObjects[1:]:
            tupleOfClassObjects = tuple(classDict[1].items());
            for item in tupleOfClassObjects:
                item[1].update(keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement);
            
        
