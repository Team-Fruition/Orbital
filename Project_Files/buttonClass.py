from supplementary import *;

class Button:

    #Constants
    NUM_BUTTON_IMAGES = 10;
    
    PLAY = 0;
    HELP = 1;
    BACK = 2;
    CREDITS = 3;
    OPTIONS = 4;
    
    INACTIVE = 0;
    ACTIVE = 1;
    
    imgStates = [];
    imgWidth = 0;
    imgHeight = 0;

    leftBound = 0;
    rightBound = 0;
    topBound = 0;
    bottomBound = 0;
    
    renderPos = [];

    currentState = PLAY;
    activeState = INACTIVE;

    clicked = False;

    def load(self):
        for index in range(0, self.NUM_BUTTON_IMAGES, 2):
            self.imgStates.append([loadImg(urlConstructor(ART_ASSETS, BUTTON), str(100 + index)[1:] + PNG_EX), loadImg(urlConstructor(ART_ASSETS, BUTTON), str(100 + index + 1)[1:] + PNG_EX]);

    def __init__(self, window_width, window_height, DISPLACE_X = 0, DISPLACE_Y = 0):
        self.load();

        self.imgWidth = self.imgStates[0].get_width();
        self.imgHeight = self.imgStates[0].get_height();

        self.renderPos = [window_width/2 - self.imgWidth/2 + DISPLACE_X, window_height/2 - self.imgHeight/2 + DISPLACE_Y];

        self.leftBound = self.renderPos[0] + self.imgWidth/4;
        self.rightBound = self.renderPos[0] + 3*self.imgWidth/4;
        self.topBound = self.renderPos[1] + self.imgWidth/4;
        self.bottomBound = self.renderPos[1] + 3*self.imgWidth/4;

    def mouseWithinBounds(self, currentMousePos):

        mouseX = currentMousePos[0];
        mouseY = currentMousePos[1];

        if mouseX >= self.leftBound and mouseX <= self.rightBound and mouseY <= self.bottomBound and mouseY >= self.topBound:
            return True;
        else:
            return False;

    def changeState(self, keyBoardState):
        if keyBoardState["Q"]:
            if self.currentState == self.PLAY:
                self.currentState = self.HELP;
            else:
                self.currentState -= 1;

        if keyBoardState["E"]:
            if self.currentState == self.HELP:
                self.currentState = self.PLAY;
            else:
                self.currentState += 1;

    def update(self, shiftAmt, speed, *args):
        keyBoardState = args[0];
        currentMousePos = args[1];
        currentMouseState = args[2];

        self.changeState(keyBoardState);

        if self.mouseWithinBounds():
            self.activeState = self.ACTIVE;
                                  
            if currentMouseState[0] == True:
                self.clicked = True;
        else:
            self.activeState = self.INACTIVE;

    def getPos(self):
        return (self.renderPos[0], self.renderPos[1]);

    def getSprite(self):
        return self.imgStates[self.currentState][self.activeState];
