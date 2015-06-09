import pygame;

from SceneManager import *;

pygame.init();

#Define and initialize surface to show to the user:
windowWidth = 800;
windowHeight = 800;

pygameFlags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF;
gameDisplay = pygame.display.set_mode((windowWidth, windowHeight));

#Define icon:
#pygame.display.set_icon(loadVanillaImg(urlConstructor(ART_ASSETS, PROJECTILES, BLUE_PROJECTILE), "0000" + PNG_EX));

#Define Window Title:
pygame.display.set_caption("Space Arena");

#Main Loop
def gameLoop():

    #Game Loop Variables:

    gameOver = False;
    gameExit = False;

    #Main Game Properties:
    framesPerSecond = 62;
    clock = pygame.time.Clock();

    keyBoardState = {"W":False, "A":False, "S":False, "D":False, "Q":False, "E":False};
    acceleration = 0.3;
    friction = 0.1;

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

        
