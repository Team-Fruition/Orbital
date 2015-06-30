from Object import *;

####Base Classes

class UIElement(GameObject):

    ####Initialization Methods

    def fillImgList(self, url, fileName, indexLen, numFrames, ex):
        self.spriteImgList = [];
        indexingVariable = 10 ** (indexLen);
        for index in range(0, numFrames):
            self.spriteImgList.append(loadImg(url, fileName + str(indexingVariable + index)[1:] + ex));

    def determineWidthAndHeight(self):
        self.spriteWidth = self.spriteImgList[0].get_width();
        self.spriteHeight = self.spriteImgList[0].get_height();

    def __init__(self, url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio,
                 windowWidth, windowHeight, displaceX, displaceY):
        
        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio);
        self.centralizeAndDisplace(windowWidth, windowHeight, displaceX, displaceY);

    ####Secondary Functions
        
    def getSpriteList(self):
        return self.spriteImgList;
    
    def getSpriteWidth(self):
        return self.spriteWidth;

    def getSpriteHeight(self):
        return self.spriteHeight;

    def centralizeAndDisplace(self, windowWidth, windowHeight, displaceX, displaceY):
        screenCenterX = windowWidth/2;
        screenCenterY = windowHeight/2;

        displaceY *= -1;

        self.objectPos = [screenCenterX - self.spriteWidth/2 + displaceX,
                          screenCenterY - self.spriteHeight/2 + displaceY];


####Instance Classes

#HPBar

class HPBar(UIElement):

    ####Initialization Methods

    def __init__(self, windowWidth, windowHeight, displaceX, displaceY):

        url = urlConstructor(ART_ASSETS, BAR);
        fileName = HPBAR;
        indexLen = 3;
        numFrames = 1;
        ex = PNG_EX;
        x = 0;
        y = 0;
        boundaryRatio = 1;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio,
                         windowWidth, windowHeight, displaceX, displaceY);
        self.updateBoundary();

class HPBarBacking(UIElement):

    ####Initialization Methods

    def __init__(self, windowWidth, windowHeight, displaceX, displaceY):

        url = urlConstructor(ART_ASSETS, BAR);
        fileName = HPEMPTY;
        indexLen = 3;
        numFrames = 1;
        ex = PNG_EX;
        x = 0;
        y = 0;
        boundaryRatio = 1;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio,
                         windowWidth, windowHeight, displaceX, displaceY);
        self.updateBoundary();

class HP(UIElement):

    #Initialization Methods

    img = None;

    def __init__(self, windowWidth, windowHeight, displaceX, displaceY, ship):

        url = urlConstructor(ART_ASSETS, BAR);
        fileName = HPPIECE;
        indexLen = 3;
        numFrames = 1;
        ex = PNG_EX;
        x = 0;
        y = 0;
        boundaryRatio = 1;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio,
                         windowWidth, windowHeight, displaceX, displaceY);
        self.updateBoundary();

        hitPoints = ship.hitPoints;
        maxHitPoints = ship.maxHitPoints;

        percentage = max(0, min(1, hitPoints/maxHitPoints));

        img = super().getSprite();
        self.img = img;
        
        width = int(percentage * self.getSpriteWidth());
        height = self.getSpriteHeight();
        
        newImage = pygame.Surface((width, height));
        newImage.set_colorkey((0, 0, 0));
        newImage.blit(img, (0, 0), (0, 0, width, height));

        self.croppedSprite = newImage;

        self.objectPos[0] += 26;
        self.objectPos[1] -= 3;

    def getSprite(self):
        return self.croppedSprite;

#Button

class Button(UIElement):

    ####Constants
    INACTIVE = 0;
    ACTIVE = 1;

    ####Initialization Methods

    def updateBoundary(self):
        objectPos = self.getPos();
        boundaryRatio = self.boundaryRatio;
        spriteWidth = self.getSpriteWidth();
        spriteHeight = self.getSpriteHeight();

        leftBoundPos = objectPos[0] + (1 - boundaryRatio) * spriteWidth;
        rightBound = objectPos[0] + boundaryRatio * spriteWidth;
        upperBoundPos = objectPos[1] + (1 - boundaryRatio) * spriteHeight;
        lowerBound = objectPos[1] + boundaryRatio * spriteHeight;

        boundaryWidth = rightBound - leftBoundPos;
        boundaryHeight = lowerBound - upperBoundPos;

        self.rect = rectGenerator(leftBoundPos, upperBoundPos, boundaryWidth, boundaryHeight);       

    def __init__(self, windowWidth, windowHeight, displaceX, displaceY, buttonConstant):
        
        url = urlConstructor(ART_ASSETS, BUTTON);
        fileName = buttonConstant;
        indexLen = 2;
        numFrames = 2;
        ex = PNG_EX;
        x = 0;
        y = 0;
        boundaryRatio = 0.7;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio,
                         windowWidth, windowHeight, displaceX, displaceY);
        self.updateBoundary();

        self.name = buttonConstant;
        self.clicked = False;

    ####Primary Functions
        
    def update(self, keyBoardState, currentMousePos, currentMouseState, globalSpeed = SpeedController(), globalDisplacement = DisplacementController()):
        self.updateSprite(currentMousePos);
        self.determineIfClicked(currentMousePos, currentMouseState);
    
    ####Secondary Functions

    def checkIfMouseWithinBounds(self, currentMousePos):
        return self.rect.collidepoint(currentMousePos) == 1;

    def checkIfMouseLeftClicked(self, currentMouseState):
        return currentMouseState[0] == 1;

    def updateSprite(self, currentMousePos):
        if self.checkIfMouseWithinBounds(currentMousePos):
            self.spriteIndex = self.ACTIVE;
        else:
            self.spriteIndex = self.INACTIVE;

    def determineIfClicked(self, currentMousePos, currentMouseState):
        self.clicked = (self.checkIfMouseWithinBounds(currentMousePos)
                        and self.checkIfMouseLeftClicked(currentMouseState));

    def getName(self):
        return self.name;

#Logo
        
class Logo(UIElement):

    ####Initialization Methods

    def __init__(self, windowWidth, windowHeight, displaceX, displaceY):
        
        url = urlConstructor(ART_ASSETS, LOGO);
        fileName = LOGO;
        indexLen = 3;
        numFrames = 1;
        ex = PNG_EX;
        x = 0;
        y = 0;
        boundaryRatio = 1;

        super().__init__(url, fileName, indexLen, numFrames, ex, x, y, boundaryRatio,
                         windowWidth, windowHeight, displaceX, displaceY);
    
#Text

class Text(UIElement):

    ####Constants
    
    TEXTCOLOR = (255, 255, 255);      

    ####Initialization Methods

    def loadFont(rootURL, fontSize):
        pygame.font.init();
        return pygame.font.Font(rootURL, fontSize);

    gameFont = loadFont(urlConstructor(ART_ASSETS, FONTS, STYLE + TTF_EX), 25);

    def fillImgList(self, textContent):
        self.spriteImgList = [];
        self.setStartingFrame();
        self.listLen = 1;
        self.spriteImgList.append(self.gameFont.render(textContent, True, self.TEXTCOLOR));
        
    def __init__(self, windowWidth, windowHeight, displaceX, displaceY, textContent):
        pygame.sprite.Sprite.__init__(self);
        self.fillImgList(textContent);
        self.determineWidthAndHeight();
        self.centralizeAndDisplace(windowWidth, windowHeight, displaceX, displaceY);

        self.setObjID();

    ####Secondary Functions

    def getSpriteList(self):
        return self.spriteImgList;
