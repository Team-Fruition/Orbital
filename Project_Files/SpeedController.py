class SpeedController:
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

    def getSpeed(self):
        return self.speed;

    def getNetHorizontalSpeed(self):
        return self.getSpeed()[self.HORIZONTAL_INDEX];

    def getNetVerticalSpeed(self):
        return self.getSpeed()[self.VERTICAL_INDEX];

    def adjustHorizontalSpeed(self, amt, setDirect):
        #Positive == Right
        #Negative == Left    
        if setDirect:
            self.speed[self.HORIZONTAL_INDEX] = amt;
        else:
            self.speed[self.HORIZONTAL_INDEX] += amt;

    def adjustVerticalSpeed(self, amt, setDirect):
        amt *= -1;
        #Positive == Up ##Stored as -ve component
        #Negative == Down ##Stored as +ve component
        if setDirect:
            self.speed[self.VERTICAL_INDEX] = amt;
        else:
            self.speed[self.VERTICAL_INDEX] += amt;

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

    def stopHorizontally(self):
        self.adjustHorizontalSpeed(self, 0, True);

    def stopVertically(self):
        self.adjustVerticalSpeed(self, 0, True);

    def movingLeft(self):
        return self.getNetHorizontalSpeed() < 0;

    def movingRight(self):
        return self.getNetHorizontalSpeed() > 0;

    def movingUp(self):
        return self.getNetVerticalSpeed() < 0;

    def movingDown(self):
        return self.getNetVerticalSpeed() > 0;
            

