from supplementary import *;
from backgroundClass import *;

class Scene:

    allObjects = [];

    currentObjectsInScene = [];

    BORDER = 5;
    BACKGROUND_INDEX = 0;
    PLAYER_SHIP = -1;

    #For checking camera boundaries in scene
    #Up to individual objects to check for own boundaries
    canContinueMovingLeft = True;
    canContinueMovingRight = True;
    canContinueMovingUp = True;
    canContinueMovingDown = True;

    #Actual camera boundaries (boundaries from perspective of camera)
    leftBound = 0; #Controls when the camera cannot go to the left any further
    rightBound = 0; #Controls when the camera cannot go to the right any further
    upperBound = 0; #Controls when the camera cannot go any higher
    lowerBound = 0; #Controls when the camera cannot go any lower

    globalShiftAmt = [0, 0];

    #To account for horizontal or vertical movement from the player's key presses
    globalSpeedList = SpeedList();

    #Environment Forces:
    globalAcceleration = 0;
    globalFriction = 0;
    
    def __init__(self, background, ships, projectiles, others, acceleration, friction):
        #Load everything here
        #Assume ships is a set of ship objects
        #Assume projectiles is a set of projectile objects
        #Assume others is a set of supplementary objects
        #Lower Index == Objects that will be "most behind" in the scene
        self.allObjects += [background, ];
        self.allObjects += others;
        self.allObjects += projectiles;
        self.allObjects += ships;

        self.addObjectToScene(background);

        self.leftBound = 0 - self.BORDER;
        self.rightBound = background.getPos()[0]*2 + self.BORDER;
        self.upperBound = 0 - self.BORDER;
        self.lowerBound = background.getPos()[1]*2 + self.BORDER;

        self.globalAcceleration = acceleration;
        self.globalFriction = friction;

    def addObjectToScene(self, obj):
        self.currentObjectsInScene.append(obj);

    def getObjectsToRender(self):
        return self.currentObjectsInScene;

    def getCurrentBackgroundCoordinates(self):
        return self.currentObjectsInScene[0].getPos();

    def determineNewSceneCoordinates(self):
        currentBackgroundLocation = self.getCurrentBackgroundCoordinates();
        return (currentBackgroundLocation[0] + self.globalSpeedList.getNetHorizontalSpeed(), currentBackgroundLocation[1] + self.globalSpeedList.getNetVerticalSpeed());

    def _checkBounds(self):
        newBackgroundLocation = self.determineNewSceneCoordinates(); 
        
        #Check if camera is about to exceed bottom boundary
        if newBackgroundLocation[1] <= self.lowerBound:
            self.canContinueMovingDown = False;
        else:
            self.canContinueMovingDown = True;
        #Check if camera is about to exceed right boundary
        if newBackgroundLocation[0] <= self.rightBound:
            self.canContinueMovingRight = False;
        else:
            self.canContinueMovingRight = True;
        #Check if camera is about to exceed top boundary
        if newBackgroundLocation[1] >= self.upperBound:
            self.canContinueMovingUp = False;
        else:
            self.canContinueMovingUp = True;
        #Check if camera is about to exceed left boundary
        if newBackgroundLocation[0] >= self.leftBound:
            self.canContinueMovingLeft = False;
        else:
            self.canContinueMovingLeft = True;

    def getShiftAmt(self):
        return self.globalShiftAmt;

    def setShiftAmt(self, amt_x, amt_y):
        self.globalShiftAmt = [amt_x, amt_y];

    def setShiftAmtX(self, amt_x):
        self.globalShiftAmt[0] = amt_x;

    def setShiftAmtY(self, amt_y):
        self.globalShiftAmt[1] = amt_y;

    def resetShiftAmt(self):
        self.globalShiftAmt = [0, 0];
            
    def update(self, W_pressed, A_pressed, S_pressed, D_pressed, Q_pressed, E_pressed, currentMousePos, currentMouseState):
        
        self.resetShiftAmt();
        
        if W_pressed:
            self.globalSpeedList.adjustVerticalSpeed(self.globalAcceleration - self.globalFriction, False);
        if A_pressed:
            self.globalSpeedList.adjustHorizontalSpeed(-self.globalAcceleration + self.globalFriction, False);
        if D_pressed:
            self.globalSpeedList.adjustHorizontalSpeed(self.globalAcceleration - self.globalFriction, False);
        if S_pressed:
            self.globalSpeedList.adjustVerticalSpeed(-self.globalAcceleration + self.globalFriction, False);

        self._checkBounds();
        
        if not self.canContinueMovingDown:
            #Snap scene to lower bound
            if self.globalSpeedList.movingDown():
                self.globalSpeedList.adjustVerticalSpeed(0, True);
                self.setShiftAmtY(self.lowerBound - self.getCurrentBackgroundCoordinates()[1]);
            
        if not self.canContinueMovingLeft:
            #Snap scene to left bound
            if self.globalSpeedList.movingLeft():
                self.globalSpeedList.adjustHorizontalSpeed(0, True);
                self.setShiftAmtX(self.leftBound - self.getCurrentBackgroundCoordinates()[0]);
            
        if not self.canContinueMovingRight:
            #Snap scene to right bound
            if self.globalSpeedList.movingRight():
                self.globalSpeedList.adjustHorizontalSpeed(0, True);
                self.setShiftAmtX(self.rightBound - self.getCurrentBackgroundCoordinates()[0]);
            
        if not self.canContinueMovingUp:
            #Snap scene to upper bound
            if self.globalSpeedList.movingUp():
                self.globalSpeedList.adjustVerticalSpeed(0, True);
                self.setShiftAmtY(self.upperBound - self.getCurrentBackgroundCoordinates()[1]);

                    
        for item in self.currentObjectsInScene:
            item.update(self.globalShiftAmt, self.globalSpeedList, currentMousePos, currentMouseState);
