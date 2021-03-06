import pygame;
import os;

#Color Constants
WHITE = (255, 255, 255);

#Directory Constants:
ART_ASSETS = "Art_Assets";

BAR = "Bar";
BUTTON = "Button";
LOGO = "Logo";
MAIN_MENU = "MainMenu";
PROJECTILES = "Projectiles";
SHIPS = "Ships";
FONTS = "Fonts";
DROPS = "Drops";
WEAPON_ICONS = "WeaponIcons";

SOUND_ASSETS = "Sound_Assets";

MUSIC = "Music";
SOUND = "Sound";

#State Constants
START = "Start";
INSTRUCTIONS = "Instructions";
GAME = "Game";
GAMEOVER = "GameOver";

#Bar Constants
##HPBAR = "Destine_Bar";
##HPEMPTY = "Health_Depleted";
##HPPIECE = "Health";

UI = "UI";
HPBAR = "UI_HP_Bar";
HPBARBACKING = "UI_HP_Bar_Backing";
PROGRESSBAR = "UI_Progress_Bar";
PROGRESSBARBACKING = "UI_Progress_Bar_Backing";

#Button Constants
BACK = "Back";
CREDITS = "Credits";
HELP = "Help";
OPTIONS = "Options";
PLAY = "Play";

#Projectile Constants
YELLOW_PROJECTILE = "Yellow_Projectile";
BLUE_PROJECTILE = "Blue_Projectile";
PINK_PROJECTILE = "Pink_Projectile";
GREEN_PROJECTILE = "Green_Projectile";
WHITE_PROJECTILE = "White_Projectile";

#Ship Constants
LETHAL_FLOWER = "Lethal_Flower";
HAILSTORM_ARTILLERY = "Hailstorm_Artillery";
DRONE = "Drone";
PLAYER_SHIP = "Player_Ship";

XYGUN = "XYGun";

#Font Constants
STYLE = "ARDESTINE";

#Drop Constants
HEALTH = "Health";

#Music Constants
BACKGROUND_MUSIC = "Subtle_Bodies";

#Extension Constants
JPG_EX = ".jpg";
PNG_EX = ".png";
TTF_EX = ".ttf";
MP3_EX = ".mp3";

#Game Constants
TEAM_PLAYER = "Player";
TEAM_ENEMY = "Enemy";

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

def loadMusic(rootURL, filename):
    pass;
