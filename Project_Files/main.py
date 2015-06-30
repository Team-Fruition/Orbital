import pygame;

from SceneManager import *;
from supplementary import *;

pygame.init();

#Define and initialize surface to show to the user:

def getCurrentWindowWidthAndHeight():
    infoObj = pygame.display.Info();

    windowWidth = infoObj.current_w;
    windowHeight = infoObj.current_h;

    return (windowWidth, windowHeight);

infoObj = getCurrentWindowWidthAndHeight();

windowWidth = infoObj[0];
windowHeight = infoObj[1];

pygameFlags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF;
pygameResizableFlag = pygame.RESIZABLE;
gameDisplay = pygame.display.set_mode((windowWidth, windowHeight), pygameFlags);

#Define icon:
#pygame.display.set_icon(loadVanillaImg(urlConstructor(ART_ASSETS, PROJECTILES, BLUE_PROJECTILE), "0000" + PNG_EX));

#Define Window Title:
pygame.display.set_caption("Space Arena");

#Set Background Music:
pygame.mixer.music.load(urlConstructor(SOUND_ASSETS, MUSIC, BACKGROUND_MUSIC) + MP3_EX);
pygame.mixer.music.play(-1);
pygame.mixer.music.set_volume(0.05);

#Main Loop
def gameLoop():

    #Game Loop Variables:

    gameOver = False;
    gameExit = False;

    #Main Game Properties:
    framesPerSecond = 62;
    clock = pygame.time.Clock();

    keyBoardState = {"W":False, "A":False, "S":False, "D":False, "Q":False, "E":False};
    acceleration = 0.5;
    friction = 0.2;

    pauseState = False;

    #Initialize SceneManager Here:

    sceneManager = SceneManager(windowWidth, windowHeight, acceleration, friction);

    #Main Game Loop:
    while not gameExit:

        #Event Detection and Handling

        for event in pygame.event.get():        #Get events in real time

            #DEBUG: Print individual event info
            #print(event);
            
            if event.type == pygame.QUIT:       #Detect for Quit Event 
                gameExit = True;

            if event.type == pygame.KEYDOWN:    #Detect for Key press
                if event.key == pygame.K_a:     #Detect for A Key
                    keyBoardState["A"] = True;
                if event.key == pygame.K_d:     #Detect for D Key
                    keyBoardState["D"] = True;
                if event.key == pygame.K_w:     #Detect for W Key
                    keyBoardState["W"] = True;
                if event.key == pygame.K_s:     #Detect for S Key
                    keyBoardState["S"] = True;
                if event.key == pygame.K_q:     #Detect for Q Key
                    keyBoardState["Q"] = True;
                if event.key == pygame.K_e:     #Detect for E key
                    keyBoardState["E"] = True;
                if event.key == pygame.K_SPACE: #Detect for Space Key
                    pauseState = not pauseState;

            if event.type == pygame.KEYUP:      #Detect for Key release
                if event.key == pygame.K_a or event.key == pygame.K_d:             
                    keyBoardState["A"] = False;
                    keyBoardState["D"] = False;
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    keyBoardState["W"] = False;
                    keyBoardState["S"] = False;
                if event.key == pygame.K_q or event.key == pygame.K_e:
                    keyBoardState["Q"] = False;
                    keyBoardState["E"] = False;

        if not pauseState:
            currentMousePos = pygame.mouse.get_pos();
            currentMouseState = pygame.mouse.get_pressed();

            #Update all objects in current Scene
            sceneManager.update(keyBoardState, currentMousePos, currentMouseState);

            currentObjectsInCurrentScene = sceneManager.getObjectsToRender();
            
            #Render Loop Here
            for item in currentObjectsInCurrentScene:
                gameDisplay.blit(item.getSprite(), item.getPos());

            pygame.display.update();

        #Control FPS:
        clock.tick(framesPerSecond);

        #DEBUG: Print FPS Information
        #print(clock.get_fps());

    pygame.quit();
    quit();

gameLoop();

        
