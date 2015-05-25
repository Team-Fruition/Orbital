from supplementary import *;
from SpeedController import *;
from DisplacementController import *;

####Base Class

class Object:
    
    ####Properties

    ##Main

    name = "";

    ##Graphical
    spriteWidth = 0;
    spriteHeight = 0;

    #Holds all Sprites used for this object
    spriteImgList = [];

    #Counter for current index in spriteImgList
    spriteIndex = 0;    

    ##Positional

    #Controls position to render 
    #Spawns right in the center of the spawnArea by default.
    #__init__() displaceX and displaceY shifts starting/spawn position accordingly from center
    objectPos = [0, 0];

    #In-Game property
    spawnAreaTopLeft = [0, 0];
    spawnAreaBottomRight = [0, 0];

    boundaryRatio = 1;
    
    leftBound = 0;
    rightBound = 0;
    upperBound = 0;
    lowerBound = 0;
    
    ####Initialization Methods

    ##Graphical

    def fillImgList(self, url, name, indexLen, numFrames, ex):
        indexingVariable = 10 ** (indexLen);
        for index in range(0, numFrames):
            self.spriteImgList.append(loadImg(url, name + str(indexingVariable + index)[1:] + ex));

    def determineWidthAndHeight(self):
        self.spriteWidth = self.spriteImgList[0].get_width();
        self.spriteHeight = self.spriteImgList[0].get_height();        

    ##In-Game property

    def determineSpawnPos(self, displaceX, displaceY):

        spawnCenterX = (self.spawnAreaTopLeft[0] + self.spawnAreaBottomRight[0])/2;
        spawnCenterY = (self.spawnAreaTopLeft[1] + self.spawnAreaBottomRight[1])/2;
        
        displaceY *= -1;

        self.objectPos = [spawnCenterX - self.spriteWidth/2 + displaceX,
                          spawnCenterY - self.spriteHeight/2 + displaceY];

    def determineSpawnArea(self, spawnWidth, spawnHeight, spawnX, spawnY):
        self.spawnAreaTopLeft = [spawnX, spawnY];
        self.spawnAreaBottomRight = [spawnWidth, spawnHeight];

    #Assumes boundaryRatio == percentage area of hitbox when compared to spriteArea
    #boundaryRatio = 1 == hitbox of object = spriteArea
    #boundaryRatio = 0.5 == hitbox of object = direct center
    def setBoundaryRatio(self, ratio):
        self.boundaryRatio = max(ratio, 0.5);
    
    def determineBounds(self):
        self.leftBound = self.objectPos[0] + (1 - self.boundaryRatio) * self.spriteWidth;
        self.rightBound = self.objectPos[0] + self.boundaryRatio * self.spriteWidth;
        self.upperBound = self.objectPos[1] + (1 - self.boundaryRatio) * self.spriteHeight;
        self.lowerBound = self.objectPos[1] + self.boundaryRatio * self.spriteHeight;
        
    ##Init

    def __init__(self, spawnWidth, spawnHeight, displaceX, displaceY, boundaryRatio, objectName,
                 url , name, indexLen, numFrames, ex = PNG_EX, spawnX = 0, spawnY = 0):
        self.name = objectName;
        self.fillImgList(url, name, indexLen, numFrames, ex);
        self.determineSpawnArea(spawnWidth, spawnHeight, spawnX, spawnY);
        self.determineSpawnPos(displaceX, displaceY);
        self.setBoundaryRatio(boundaryRatio);
        self.determineBounds();

    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement):
        self.updateSprite(keyBoardState, currentMousePos, currentMouseState);
        self.updatePos(globalSpeed, globalDisplacement);
    
    def getSprite(self):
        return self.spriteImgList[self.spriteIndex];

    def getPos(self):
        return tuple(self.objectPos);

    ####Secondary Functions

    def checkIfMouseWithinBounds(self, currentMousePos):
        if self.leftBound <= currentMousePos[0] <= self.rightBound and self.topBound <= currentMousePos[1] <= self.bottomBound:
            return true;

    def updateSprite(self, keyBoardState, currentMousePos, currentMouseState):
        pass;

    def updatePos(self, globalSpeed, globalDisplacement):
        pass;

####Sub-Classes

class Logo(Object):

    def __init__(self, spawnWidth, spawnHeight, displaceX, displaceY, logoObjName):

        boundaryRatio = 1;
        spawnX = 0;
        spawnY = 0;
        url = urlConstructor(ART_ASSETS, LOGO);
        name = LOGO;
        indexLen = 3;
        numFrames = 1;
        ex = PNG_EX;
        
        super().__init__(spawnWidth, spawnHeight, displaceX, displaceY, boundaryRatio, logoObjName,
                         url, name, indexLen, numFrames, ex, spawnX, spawnY);

#Logo(1024, 1024, 0, -200, "Test");
