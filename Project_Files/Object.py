from supplementary import *;
from SpeedController import *;
from DisplacementController import *;

####Base Class

class Object:
    
    ####Initialization Methods

    ##Graphical

    def fillImgList(self, url, fileName, indexLen, numFrames, ex):
        indexingVariable = 10 ** (indexLen);
        for index in range(0, numFrames):
            self.spriteImgList.append(loadImg(url, fileName + str(indexingVariable + index)[1:] + ex));

    def determineWidthAndHeight(self):
        self.spriteWidth = self.spriteImgList[0].get_width();
        self.spriteHeight = self.spriteImgList[0].get_height();        

    ##In-Game property

    def determineSpawnArea(self, spawnWidth, spawnHeight, spawnX, spawnY):
        self.spawnAreaTopLeft = [spawnX, spawnY];
        self.spawnAreaBottomRight = [spawnWidth, spawnHeight];        

    def determineSpawnPos(self, displaceX, displaceY):

        spawnCenterX = (self.spawnAreaTopLeft[0] + self.spawnAreaBottomRight[0])/2;
        spawnCenterY = (self.spawnAreaTopLeft[1] + self.spawnAreaBottomRight[1])/2;
        
        displaceY *= -1;

        self.objectPos = [spawnCenterX - self.spriteWidth/2 + displaceX,
                          spawnCenterY - self.spriteHeight/2 + displaceY];
        
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
                 url, fileName, indexLen, numFrames, ex = PNG_EX, spawnX = 0, spawnY = 0):

        ####Properties

        ##Main

        self.name = objectName;
        
        ##Graphical
        self.spriteWidth = 0;
        self.spriteHeight = 0;

        #Holds all Sprites used for this object
        self.spriteImgList = [];

        #Counter for current index in spriteImgList
        self.spriteIndex = 0;    

        ##Positional

        #Controls position to render 
        #Spawns right in the center of the spawnArea by default.
        #__init__() displaceX and displaceY shifts starting/spawn position accordingly from center
        self.objectPos = [0, 0];

        #In-Game property
        self.spawnAreaTopLeft = [0, 0];
        self.spawnAreaBottomRight = [0, 0];

        self.boundaryRatio = 1;
        
        self.leftBound = 0;
        self.rightBound = 0;
        self.upperBound = 0;
        self.lowerBound = 0;
        
        ####Initialization Procedures
        
        self.fillImgList(url, fileName, indexLen, numFrames, ex);
        self.determineWidthAndHeight();
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
        if self.leftBound <= currentMousePos[0] <= self.rightBound and self.upperBound <= currentMousePos[1] <= self.lowerBound:
            return True;

    def checkIfMouseLeftClicked(self, currentMouseState):
        return currentMouseState[0] == 1;

    def checkIfMouseRightClicked(self, currentMouseState):
        return currentMouseState[1] == 1;

    def getName(self):
        return self.name;

    def updateSprite(self, keyBoardState, currentMousePos, currentMouseState):
        pass;

    def updatePos(self, globalSpeed, globalDisplacement):
        pass;

####Sub-Classes

class Logo(Object):

    def __init__(self, spawnWidth, spawnHeight, displaceX, displaceY, logoObjName):

        boundaryRatio = 1;
        url = urlConstructor(ART_ASSETS, LOGO);
        fileName = LOGO;
        indexLen = 3;
        numFrames = 1;
        
        super().__init__(spawnWidth, spawnHeight, displaceX, displaceY, boundaryRatio, logoObjName,
                         url, fileName, indexLen, numFrames);


class Button(Object):

    INACTIVE = 0;
    ACTIVE = 1;

    def __init__(self, spawnWidth, spawnHeight, displaceX, displaceY, buttonObjName,
                 fileName):

        boundaryRatio = 0.7;
        spawnX = 0;
        spawnY = 0;
        url = urlConstructor(ART_ASSETS, BUTTON);
        indexLen = 2;
        numFrames = 2;

        self.clicked = False;

        super().__init__(spawnWidth, spawnHeight, displaceX, displaceY, boundaryRatio, buttonObjName,
                         url, fileName, indexLen, numFrames);

        self.spriteIndex = self.INACTIVE;

    def determineIfClicked(self, currentMousePos, currentMouseState):
        if self.checkIfMouseWithinBounds(currentMousePos) and self.checkIfMouseLeftClicked(currentMouseState):
            self.clicked = True;
        else:
            self.clicked = False;

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement):
        self.updateSprite(keyBoardState, currentMousePos, currentMouseState);
        self.determineIfClicked(currentMousePos, currentMouseState);

    def updateSprite(self, keyBoardState, currentMousePos, currentMouseState):
        if self.checkIfMouseWithinBounds(currentMousePos):
            self.spriteIndex = self.ACTIVE;
        else:
            self.spriteIndex = self.INACTIVE;

class Text(Object):

    #Color Constant
    TEXTCOLOR = (255, 255, 255);

    def loadFont(rootURL, fontSize):
        pygame.font.init();
        return pygame.font.Font(rootURL, fontSize);    

    #Font Variable
    gameFont = loadFont(urlConstructor(ART_ASSETS, FONTS, STYLE + TTF_EX), 25);

    def renderFont(self, string):
        self.spriteImgList.append(self.gameFont.render(string, True, self.TEXTCOLOR));
        
    def fillImgList(self, url, text, indexLen, numFrames, ex):
        self.renderFont(text);

    def __init__(self, spawnWidth, spawnHeight, displaceX, displaceY, textContent):

        boundaryRatio = 1;
        spawnX = 0;
        spawnY = 0;
        url = None;
        indexLen = None;
        numFrames = None;
        ex = None;
        objectName = None;

        super().__init__(spawnWidth, spawnHeight, displaceX, displaceY, boundaryRatio, objectName,
                         url, textContent, indexLen, numFrames, ex, spawnX, spawnY);

    
