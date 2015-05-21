import pygame;

from supplementary import *;

#Constants:

ART_ASSETS = "Art_Assets";
MAIN_MENU = "MainMenu";
JPG_EX = ".jpg";

class Background:

    #Constants initialization
    BLACK = (0, 0, 0);

    #Variables initialization
    backgroundImgList = [];
    backgroundWidth = 0;
    backgroundHeight = 0;

    #Controls position to render
    backgroundPos = [];
    centerBackgroundPos = [];

    #Position at which background's center is at (0, 0)
    trueCenter = [];
    
    #Controls if backgroundSpriteCount increases or decreases
    backgroundLoopBackwards = False;

    #Counter for current frame of animation
    backgroundSpriteCount = 0;

    #Prevents background from updating too quickly
    backgroundDelay = 3;

    #Fill backgroundImgList with the images required
    def load(self):
        for index in range(0, 18):
            self.backgroundImgList.append(loadImg(urlConstructor(ART_ASSETS, MAIN_MENU), MAIN_MENU + str(1000 + index)[1:] + JPG_EX));
                
    def __init__(self, window_width, window_height):
        self.load();

        self.backgroundWidth = self.backgroundImgList[0].get_width();
        self.backgroundHeight = self.backgroundImgList[0].get_height();

        self.trueCenter = [-self.backgroundWidth/2, -self.backgroundHeight/2];
        self.centerBackgroundPos = [-self.backgroundWidth/2 + window_width/2, -self.backgroundHeight/2 + window_height/2];
        self.backgroundPos = [self.centerBackgroundPos[0], self.centerBackgroundPos[1]];

    def update(self, shiftAmt, speed = None):
        #Controls positioning
        self.adjustPos(speed);
        self.shiftPos(shiftAmt[0], shiftAmt[1]);
        #Controls refresh rate
        self.refreshBackgroundSprite();

    def refreshBackgroundSprite(self):
        if self.backgroundDelay >= 5:
            if self.backgroundLoopBackwards == False:
                self.backgroundSpriteCount += 1;
                if self.backgroundSpriteCount >= len(self.backgroundImgList):
                    self.backgroundLoopBackwards = True;
                    self.backgroundSpriteCount -= 1;
            else:
                self.backgroundSpriteCount -= 1;
                if self.backgroundSpriteCount <= 0:
                    self.backgroundLoopBackwards = False;
                    self.backgroundSpriteCount +=1;
                
            self.backgroundDelay = 0;
        else:
            self.backgroundDelay += 1;
            
    def getSprite(self):
        return self.backgroundImgList[self.backgroundSpriteCount];

    def resetPos(self):
        self.backgroundPos = [self.centerBackgroundPos[0], self.centerBackgroundPos[1]];
    
    def getPos(self):
        return (self.backgroundPos[0], self.backgroundPos[1]);

    def getTrueCenter(self):
        return self.trueCenter;

    def setHorizontalCoordinates(self, coordinate):
        self.background[0] = coordinate;

    def setVerticalCoordinates(self, coordinate):
        self.background[1] = coordinate;
    
    def setPos(self, coordinates):
        self.setHorizontalCoordinates(coordinates[0]);
        self.setVerticalCoordinates(coordinates[1]);

    def shiftPos(self, amt_x, amt_y):
        self.backgroundPos[0] += amt_x;
        self.backgroundPos[1] += amt_y;
    
    def adjustPos(self, speed):
        #Move Right = +ve value ##Camera going Left
        #Move Left = -ve value ##Camera going Right
        #Move Up = +ve value ##Camera going Down
        #Move Down = -ve value ##Camera going Up
        if not speed == None:
            self.backgroundPos[0] += -speed.getNetHorizontalSpeed();
            self.backgroundPos[1] += -speed.getNetVerticalSpeed();
