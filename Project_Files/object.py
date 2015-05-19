class object:

    width = 0;
    height = 0;
    
    x = 0;
    y = 0;

    change_x = 0;
    change_y = 0;

    active_area_x = 0;
    actove_area_y = 0;

    acceleration = 0;
    friction = 0;
    
    def set_Pos(self, x, y):
        self.x = x;
        self.y = y;

    def _set_Boundaries(self, x, y, width, height):
        self.left_bound = x;
        self.top_bound = y;
        self.right_bound = x + width;
        self.bottom_bound = y + height;        

    def set_acceleration(self, acceleration):
        self.acceleration = acceleration;

    def set_friction(self, friction):
        self.friction = friction;
    
    def __init__(self, x, y, width, height, acceleration, friction):
        set_Pos(x, y);
        _set_Boundaries(x, y, width, height);
        set_acceleration(acceleration);
        set_friction(self, friction);

    def collisionCheck(self, other):
        collision = False;
        
        if self_left_bound <= other_right_bound and self_right_bound >= other_right_bound and ((self_top_bound >= other_top_bound and self_top_bound <= other_bottom_bound) or (self_bottom_bound >= other_top_bound and self_bottom_bound <= other_bottom_bound)):
            #self has hit other from the left
            collision = True;
        elif self_top_bound <= other_bottom_bound and self_bottom_bound >= other_bottom_bound and ((self_left_bound <= other_right_bound and self_left_bound >= other_left_bound) or (self_right_bound >= other_left_bound and self_right_bound <= other_right_bound)):
            #self has hit other from the bottom
            collision = True;
        elif self_bottom_bound >= other_top_bound and self_bottom_bound <= other_bottom_bound and ((self_left_bound <= other_right_bound and self_left_bound >= other_left_bound) or (self_right_bound >= other_left_bound and self_right_bound <= other_right_bound)):
            #self has hit other from the top
            collision = True;
        elif self_right_bound >= other_left_bound and self_left_bound <= other_left_bound and ((self_top_bound >= other_top_bound and self_top_bound <= other_bottom_bound) or (self_bottom_bound >= other_top_bound and self_bottom_bound <= other_bottom_bound)):
            #self has hit other from the right
            collision = True;

        return collision;

    def updatePosition(accelerate_Forward = False, accelerate_Left = False, accelerate_Back = False, accelerate_Right = False):
        
        #Handle acceleration:
        if accelerate_Left == True:
            self.change_x += -self.acceleration;

        if accelerate_Right == True:
            self.change_x += self.acceleration;
        
        if accelerate_Back == True:
            self.change_y += self.acceleration;

        if accelerate_Forward == True:
            self.change_y += -self.acceleration;


        #Handle friction:
        if self.change_x > self.friction:
            self.change_x += -self.friction;
        elif self.change_x > 0 and D_pressed == False:
            self.change_x = 0;
            
        if self.change_x < -self.friction:
            self.change_x += self.friction;
        elif self.change_x < 0 and A_pressed == False:
            self.change_x = 0;
            
        if self.change_y > self.friction:
            self.change_y += -self.friction;
        elif self.change_y > 0 and S_pressed == False:
            self.change_y = 0;

        if self.change_y < -self.friction:
            self.change_y += self.friction;
        elif self.change_y < 0 and W_pressed == False:
            self.change_y = 0;
     
        #Update position
        self.x += self.change_x;
        self.y += self.change_y;

    def updateBounds():
        self.left_bound = self.x;
        self.top_bound = self.y;
        self.right_bound = self.x + self.width;
        self.bottom_bound = self.y + self.height;           
    
    def update():
        updatePosition();
        updateBounds();

    
