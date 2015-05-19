import pygame;

from supplementary import *;

#Constants:

ART_ASSETS = "Art_Assets";
MAIN_MENU = "MainMenu";
JPG_EX = ".jpg";

def loadBackground():

    background = [];
    
    for index in range(0, 18):
        background.append(loadImg(urlConstructor(ART_ASSETS, MAIN_MENU), MAIN_MENU + str(1000 + index)[1:] + JPG_EX));

    return background;
