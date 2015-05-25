import pygame;
import os;

#Directory Constants:
ART_ASSETS = "Art_Assets";

BUTTON = "Button";
LOGO = "Logo";
MAIN_MENU = "MainMenu";
PROJECTILES = "Projectiles";
SHIPS = "Ships";

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

