class DisplacementController:

    HORIZONTAL_INDEX = 0;
    VERTICAL_INDEX = 1;

    #Input values via the functions below according to a person's view of it on the screen
    #Attempt to Move Left == -ve amt for setHorizontalDisplacement()
    #Attempt to Move Right == +ve amt for setHorizontalDisplacement()
    #Attempt to Move Up == +ve amt for setVerticalDisplacement()
    #Attempt to Move Down == -ve amt for setVerticalDisplacement()
    displacement = [0, 0];

    def __init__(self):
        self.displacement = [0, 0];

    def getDisplacement(self):
        return self.displacement;

    def setHorizontalDisplacement(self, amt):
        #Positive == Right
        #Negative == Left
        self.displacement[self.HORIZONTAL_INDEX] = amt;

    def setVerticalDisplacement(self, amt):
        amt *= -1;
        #Positive == Up
        #Negative == Down
        self.displacement[self.VERTICAL_INDEX] = amt;

    def getHorizontalDisplacement(self):
        return self.getDisplacement()[self.HORIZONTAL_INDEX];

    def getVerticalDisplacement(self):
        return self.getDisplacement()[self.VERTICAL_INDEX];

    def resetDisplacement(self):
        self.displacement = [0, 0];
