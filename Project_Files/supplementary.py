import pygame;
import os;

#Define colors:
white = (255, 255, 255);
black = (0, 0, 0);
red = (255, 0, 0);
blue = (0, 0, 255);
green = (0, 255, 0);

#Define constants:
MOUSELEFT = 1;
MOUSERIGHT = 3;

def nearest(num):
    return round(num/10.0)*10.0;

def urlConstructor(*folders):
    currentURL = os.getcwd();

    for folder in folders:
        currentURL = os.path.join(currentURL, folder);

    return currentURL;
    

def loadImg(rootURL, filename):
    return pygame.image.load(os.path.join(rootURL, filename));

class SpeedList:
    HORIZONTAL_INDEX = 0;
    VERTICAL_INDEX = 1;
    
    #Input values via the functions below according to a person's view of it on the screen
    #Attempt to Move Left == -ve amt for adjustHorizontalSpeed()
    #Attempt to Move Right == +ve amt for adjustHorizontalSpeed()
    #Attempt to Move Up == +ve amt for adjustVerticalSpeed()
    #Attempt to Move Down == -ve amt for adjustVerticalSpeed()
    speed = [0, 0];

    def __init__(self):
        self.speed = [0, 0];

    def adjustVerticalSpeed(self, amt, setDirect):
        amt *= -1;
        #Positive == Up ##Stored as -ve component
        #Negative == Down ##Stored as +ve component
        if setDirect:
            self.speed[self.VERTICAL_INDEX] = amt;
        else:
            self.speed[self.VERTICAL_INDEX] += amt;

    def adjustHorizontalSpeed(self, amt, setDirect):
        #Positive == Right
        #Negative == Left    
        if setDirect:
            self.speed[self.HORIZONTAL_INDEX] = amt;
        else:
            self.speed[self.HORIZONTAL_INDEX] += amt;

    def getNetHorizontalSpeed(self):
        return self.speed[self.HORIZONTAL_INDEX];

    def getNetVerticalSpeed(self):
        return self.speed[self.VERTICAL_INDEX];

    def getSpeedList(self):
        return self.speed;

    def stopHorizontally(self):
        self.speed[self.HORIZONTAL_INDEX] = 0;

    def stopVertically(self):
        self.speed[self.VERTICAL_INDEX] = 0;

    def movingLeft(self):
        return self.getNetHorizontalSpeed() < 0;

    def movingRight(self):
        return self.getNetHorizontalSpeed() > 0;

    def movingUp(self):
        return self.getNetVerticalSpeed() < 0;

    def movingDown(self):
        return self.getNetVerticalSpeed() > 0;
