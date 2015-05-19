import pygame;
import os;

def nearest(num):
    return round(num/10.0)*10.0;

def urlConstructor(*folders):
    currentURL = os.getcwd();

    for folder in folders:
        currentURL = os.path.join(currentURL, folder);

    return currentURL;
    

def loadImg(rootURL, filename):
    return pygame.image.load(os.path.join(rootURL, filename));
