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

class speedList:
    #(Up, Down, Left, Right)
    UP_INDEX = 0;
    DOWN_INDEX = 1;
    LEFT_INDEX = 2;
    RIGHT_INDEX = 3;

    #Input values via the functions below according to a person's view of it on the screen
    #Move Left == -ve amt for adjustHorizontalSpeed()
    #Move Right == +ve amt for adjustHorizontalSpeed()
    #Move Up == +ve amt for adjustVerticalSpeed()
    #Move Down == -ve amt for adjustVerticalSpeed()
    speed = [0, 0, 0, 0];

    def __init__(self):
        self.speed = [0, 0, 0, 0];

    def adjustVerticalSpeed(self, amt):
        #Positive == Up
        #Negative == Down
        if amt < 0:
            self.speed[self.DOWN_INDEX] = amt;
        elif amt > 0:
            self.speed[self.UP_INDEX] = amt;
        else:
            self.speed[self.DOWN_INDEX] = 0;
            self.speed[self.UP_INDEX] = 0;

    def adjustHorizontalSpeed(self, amt):
        amt *= -1;
        #Positive == Right
        #Negative == Left
        if amt < 0:
            self.speed[self.LEFT_INDEX] = amt;
        elif amt > 0:
            self.speed[self.RIGHT_INDEX] = amt;
        else:
            self.speed[self.LEFT_INDEX] = 0;
            self.speed[self.RIGHT_INDEX] = 0;

    def adjustSpeed(self, horizontal, vertical):
        self.adjustHorizontalSpeed(horizontal);
        self.adjustVerticalSpeed(vertical);
    
    def getSpeedList(self):
        return self.speed;

    def getNetHorizontalSpeed(self):
        return self.speed[self.RIGHT_INDEX] + self.speed[self.LEFT_INDEX];

    def getNetVerticalSpeed(self):
        return self.speed[self.UP_INDEX] + self.speed[self.DOWN_INDEX];

    def noNetSpeed(self):
        return self.getNetHorizontalSpeed() == 0 and self.getNetVerticalSpeed() == 0;


    
