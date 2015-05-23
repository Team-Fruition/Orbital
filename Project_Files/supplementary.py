import pygame;
import os;

#Directory Constants:
ART_ASSETS = "Art_Assets";

BUTTON = "Button";
LOGO = "Logo";
MAIN_MENU = "MainMenu";
PROJECTILES = "Projectiles";
SHIPS = "Ships";

#Button Constants
BACK_BUTTON = "BackButton";
HELP_BUTTON = "HelpButton";
PLAY_BUTTON = "PlayButton";

#Projectile Constants
YELLOW_PROJECTILE = "Yellow_Projectile"
EXPLOSION = "Explosion";

#Ship Constants
ENEMY_SHIP_1 = "Enemy_Ship_1";
PLAYER_SHIP = "Player_Ship";

#Extension Constants
JPG_EX = ".jpg";
PNG_EX = ".png";

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

    def applyFriction(self, friction):
        #friction should be a +ve value
        if self.getNetHorizontalSpeed() <= -friction:
            self.adjustHorizontalSpeed(friction, False);
        elif self.getNetHorizontalSpeed() >= friction:
            self.adjustHorizontalSpeed(-friction, False);
        else:
            self.adjustHorizontalSpeed(0, True);

        if self.getNetVerticalSpeed() <= -friction:
            self.adjustVerticalSpeed(-friction, False);
        elif self.getNetVerticalSpeed() >= friction:
            self.adjustVerticalSpeed(friction, False);
        else:
            self.adjustVerticalSpeed(0, True);        
            
