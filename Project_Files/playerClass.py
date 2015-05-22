from supplementary import *;

import math;

#Path Constants:

ART_ASSETS = "Art_Assets";
SHIPS = "Ships";
PLAYER_SHIP = "Player_Ship";
PNG_EX = ".png";

class Player:

    #Constants

    #Variables
    playerImgList = [];
    playerWidth = 0;
    playerHeight = 0;
    playerCurrentDirection = 0; #0 being East, 180 being West

    #Controls position to render
    playerPos = [];
    centerPlayerPos = [];

    #Rotation frame count
    playerSpriteCount = 0;

    #

    def load(self):
        for index in range(0, 60):
            self.playerImgList.append(loadImg(urlConstructor(ART_ASSETS, SHIPS, PLAYER_SHIP), str(10000 + index)[1:] + PNG_EX));

    def __init__(self, window_width, window_height):
        self.load();

        self.playerWidth = self.playerImgList[0].get_width();
        self.playerHeight = self.playerImgList[0].get_height();

        self.centerPlayerPos = [window_width/2, window_height/2];
        self.playerPos = list(self.centerPlayerPos);

    def shiftPos(self, amt):
        self.playerPos[0] += amt_x[0];
        self.playerPos[1] += amt_y[1];

    def adjustPos(self, speed):
        #Move Right = +ve value 
        #Move Left = -ve value 
        #Move Up = +ve value 
        #Move Down = -ve value 
        self.playerPos[0] += speed.getNetHorizontalSpeed();
        self.playerPos[1] += speed.getNetVerticalSpeed();          
        
    def update(self, gameState):
        #Controls positioning
        if gameState.getLockStatus():
            self.adjustPos(gameState["speed"]);
            self.shiftPos(gameState["shiftAmt"]);

      
