from GameObject import *
from PlayGround import *
import pygame
from pygame.locals import *
import configuration as cfg
import PlayState
import MenuState
from OpenGL.GLU import *
from Controller import HumanController, MinMaxController

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode(cfg.displaySize, DOUBLEBUF | OPENGL)
        gluPerspective(cfg.FOV, cfg.displayAspectRatio, cfg.nearClippingPlane, cfg.farClippingPlane)

        self.isGameRunning = True

        self.statesStack = [MenuState.MenuState()]
        #self.statesStack += [PlayState.PlayState(MinMaxController(), MinMaxController())]


    def play(self):
        for state in self.statesStack:
            state.constructor()

        prevTime = pygame.time.get_ticks()

        while self.isGameRunning:
                # Time
                currentTime = pygame.time.get_ticks()
                dt = (currentTime - prevTime) / 1000
                if dt < cfg.timePerFrame:
                    pygame.time.wait(int((cfg.timePerFrame - dt) * 1000))
                    dt = cfg.timePerFrame
                prevTime = currentTime

                # Proceed
                self.eventHandling()
                self.update(dt)
                self.render()

        for state in self.statesStack:
            state.destructor()

    def eventHandling(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.isGameRunning = False

        for state in self.statesStack:
            if not state.eventHandling(events):
                break

    def update(self, deltaTime: float):
        stackSize = len(self.statesStack)
        for i in range(0, stackSize):
            if not self.statesStack[i].update(deltaTime):
                self.statesStack.pop(i).destructor()
                i -= 1
                stackSize -= 1
                continue
            self.statesStack[i].lateUpdate(deltaTime)

        if len(self.statesStack) == 0:
            self.isGameRunning = False

    def render(self):
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(cfg.backgroundColor[0] / 255, cfg.backgroundColor[1] / 255, cfg.backgroundColor[2] / 255, 1)

        for i in range(len(self.statesStack) - 1, -1, -1):
            if not self.statesStack[i].draw():
                break

        # Display
        pygame.display.flip()
