from supplementary import *;

####Base Classes

class Object:

    ####Object ID Methods

    numObj = 0;

    @classmethod
    def getObjNum(cls):
        return cls.numObj;

    @classmethod
    def incrementObjNum(cls):
        cls.numObj += 1;

    @classmethod
    def getClassName(cls):
        return cls.__name__;
    
    def setObjID(self):
        self.ID = str(self.getClassName()) + str(self.getObjNum());
        self.incrementObjNum();

    def getObjID(self):
        return self.ID;
    
    ####Initialization Methods

    ##Positional

    def setSpawnPos(self, startX, startY):
        self.objectPos = [startX, startY];

    ##Init

    def __init__(self, startX, startY, name):

        ####Properties

        ##General

        self.setObjID();
        self.name = name;
        self.delete = False;

        ##Positional

        self.setSpawnPos(startX, startY);


    ####Primary Functions

    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement):
        self.updateSprite(keyBoardState, currentMousePos, currentMouseState);
        self.updatePos(globalSpeed, globalDisplacement);
    
    def getSprite(self):
        pass;

    def getPos(self):
        return tuple(self.objectPos);

    ####Secondary Functions

    def getName(self):
        return self.name;

    def getIdentifier(self):
        return self.identifier;

    def setIdentifier(self, identifier):
        self.identifier = identifier;

    def updateSprite(self, keyBoardState, currentMousePos, currentMouseState):
        pass;

    def updatePos(self, globalSpeed, globalDisplacement):
        pass;

    def destroyObj(self):
        self.delete = True;


class StaticImmovableElement(Object):

    ####Initialization Methods

    ##Graphical

    def fillImgList(self, url, fileName, indexLen, numFrames, ex):
        self.spriteIndex = 0;
        self.listLen = numFrames;
        self.spriteImgList = [];
        
        indexingVariable = 10 ** (indexLen);
        
        for index in range(0, numFrames):
            self.spriteImgList.append(loadImg(url, fileName + str(indexingVariable + index)[1:] + ex));

    def determineWidthAndHeight(self):
        self.spriteWidth = self.spriteImgList[0].get_width();
        self.spriteHeight = self.spriteImgList[0].get_height();

    ##Init

    def __init__(self, startX, startY, name, url, fileName, indexLen, numFrames, ex):

        super().__init__(startX, startY, name);

        self.fillImgList(url, fileName, indexLen, numFrames, ex);
        self.determineWidthAndHeight();

    def centralizeAndDisplace(self, windowWidth, windowHeight, displaceX, displaceY):
        screenCenterX = windowWidth/2;
        screenCenterY = windowHeight/2;

        displaceY *= -1;

        self.objectPos = [screenCenterX - self.spriteWidth/2 + displaceX,
                          screenCenterY - self.spriteHeight/2 + displaceY];

    ####Primary Functions

    def getSprite(self):
        return self.spriteImgList[self.spriteIndex];

class InteractiveImmovableElement(StaticImmovableElement):
    
    ####Initialization Functions

    #Assumes boundaryRatio == percentage area of hitbox when compared to spriteArea
    #boundaryRatio = 1 == hitbox of object = spriteArea
    #boundaryRatio = 0.5 == hitbox of object = direct center
    def setBoundaryRatio(self, ratio):
        self.boundaryRatio = min(1, max(ratio, 0.5));
    
    def determineBounds(self):
        self.leftBound = self.objectPos[0] + (1 - self.boundaryRatio) * self.spriteWidth;
        self.rightBound = self.objectPos[0] + self.boundaryRatio * self.spriteWidth;
        self.upperBound = self.objectPos[1] + (1 - self.boundaryRatio) * self.spriteHeight;
        self.lowerBound = self.objectPos[1] + self.boundaryRatio * self.spriteHeight;

    ##Init
    
    def __init__(self, startX, startY, boundaryRatio, name, url, fileName, indexLen, numFrames, ex):
        super().__init__(startX, startY, name, url, fileName, indexLen, numFrames, ex);
        
        self.setBoundaryRatio(boundaryRatio);

    ####Secondary Functions
    
    def checkIfMouseWithinBounds(self, currentMousePos):
        return (self.leftBound <= currentMousePos[0] <= self.rightBound
                and self.upperBound <= currentMousePos[1] <= self.lowerBound);

    def checkIfMouseLeftClicked(self, currentMouseState):
        return currentMouseState[0] == 1;

####"Instance" Classes

##Class Constants
TEXT = "Text"
LOGO = "Logo"
BUTTON = "Button"

class Text(StaticImmovableElement):

    ####Constants
    TEXTCOLOR = (255, 255, 255);      

    ####Initialization Functions

    def loadFont(rootURL, fontSize):
        pygame.font.init();
        return pygame.font.Font(rootURL, fontSize);

    gameFont = loadFont(urlConstructor(ART_ASSETS, FONTS, STYLE + TTF_EX), 25);

    def fillImgList(self, textContent):
        self.spriteImgList = [];
        self.spriteIndex = 0;
        self.listLen = 1;
        self.spriteImgList.append(self.gameFont.render(textContent, True, self.TEXTCOLOR));        

    def __init__(self, windowWidth, windowHeight, displaceX, displaceY, textContent):
        self.fillImgList(textContent);
        self.determineWidthAndHeight();
        self.centralizeAndDisplace(windowWidth, windowHeight, displaceX, displaceY);

        self.setObjID();
        self.delete = False;
        
class Logo(StaticImmovableElement):

    ####Initialization Functions

    def __init__(self, windowWidth, windowHeight, displaceX, displaceY):

        startX = 0;
        startY = 0;
        objectID = LOGO;
        url = urlConstructor(ART_ASSETS, LOGO);
        fileName = LOGO;
        indexLen = 3;
        numFrames = 1;
        ex = PNG_EX;

        super().__init__(startX, startY, objectID, url, fileName, indexLen, numFrames, ex);
        self.centralizeAndDisplace(windowWidth, windowHeight, displaceX, displaceY);

    def getIdentifier(self):
        return LOGO;

class Button(InteractiveImmovableElement):

    ####Constants
    INACTIVE = 0;
    ACTIVE = 1;

    def __init__(self, windowWidth, windowHeight, displaceX, displaceY, buttonConstant):

        startX = 0;
        startY = 0;
        boundaryRatio = 0.75;
        objectID = buttonConstant;
        url = urlConstructor(ART_ASSETS, BUTTON);
        fileName = buttonConstant;
        indexLen = 2;
        numFrames = 2;
        ex = PNG_EX;

        self.clicked = False;

        super().__init__(startX, startY, boundaryRatio, objectID, url, fileName, indexLen, numFrames, ex);
        self.centralizeAndDisplace(windowWidth, windowHeight, displaceX, displaceY);
        self.determineBounds();

        self.spriteIndex = self.INACTIVE;

    ####Primary Functions
    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed, globalDisplacement):
        self.updateSprite(currentMousePos);
        self.determineIfClicked(currentMousePos, currentMouseState);

    ####Secondary Functions
    def updateSprite(self, currentMousePos):
        if self.checkIfMouseWithinBounds(currentMousePos):
            self.spriteIndex = self.ACTIVE;
        else:
            self.spriteIndex = self.INACTIVE;
    
    def determineIfClicked(self, currentMousePos, currentMouseState):
        self.clicked = (self.checkIfMouseWithinBounds(currentMousePos)
                        and self.checkIfMouseLeftClicked(currentMouseState));


