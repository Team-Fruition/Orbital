import pygame;
import os;

#Color Constants
WHITE = (255, 255, 255);

#Directory Constants:
ART_ASSETS = "Art_Assets";

BUTTON = "Button";
LOGO = "Logo";
MAIN_MENU = "MainMenu";
PROJECTILES = "Projectiles";
SHIPS = "Ships";
FONTS = "Fonts"

#State Constants
START = "Start";
INSTRUCTIONS = "Instructions";
GAME = "Game";
GAMEOVER = "GameOver";

#Button Constants
BACK = "Back";
CREDITS = "Credits";
HELP = "Help";
OPTIONS = "Options";
PLAY = "Play";

#Projectile Constants
YELLOW_PROJECTILE = "Yellow_Projectile";
BLUE_PROJECTILE = "Blue_Projectile";
EXPLOSION = "Explosion";

#Ship Constants
DRONE = "Drone";
PLAYER_SHIP = "Player_Ship";

#Font Constants
STYLE = "ARDESTINE";

#Extension Constants
JPG_EX = ".jpg";
PNG_EX = ".png";
TTF_EX = ".ttf";

def nearest(num):
    return round(num/10.0)*10.0;

def urlConstructor(*folders):
    currentURL = os.getcwd();
    currentURL = os.path.join(currentURL, *folders);
    return currentURL;
    
def loadVanillaImg(rootURL, fileName):
    return pygame.image.load(os.path.join(rootURL, fileName));

def loadImg(rootURL, fileName):
    img = pygame.image.load(os.path.join(rootURL, fileName));
    img = img.convert_alpha();
    img.set_colorkey(WHITE);
    return img;
