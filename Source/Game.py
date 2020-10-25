from GameObject import *
from PlayGround import *
import pygame
import configuration as cfg
import PlayState
import MenuState

class Game:
    def __init__(self):
        self.statesStackChanged = False
        pygame.init()
        self.isGameRunning = True

        self.statesStack = []

    def play(self):
        self.pushState(MenuState.MenuState())
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
                if self.statesStackChanged:
                    self.statesStackChanged = False
                else:
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

    def popState(self, index = 0):
        if len(self.statesStack) == 0:
            return None

        state = self.statesStack.pop(index)
        state.destructor()
        self.statesStackChanged = True
        return state

    def pushState(self, state):
        if state is None:
            return

        state.constructor()
        self.statesStack.insert(0, state)
        self.statesStackchanged = True

    def update(self, deltaTime: float):
        stackSize = len(self.statesStack)
        for i in range(0, stackSize):
            state = self.statesStack[i]
            updateLowerState = state.update(deltaTime)
            state.lateUpdate(deltaTime)

            if state.requestPopState():
                self.popState()

            pushState = state.requestPushState()
            if pushState is not None:
                self.pushState(pushState)

            if not updateLowerState:
                break

        if len(self.statesStack) == 0:
            self.isGameRunning = False

    def render(self):
        if len(self.statesStack) != 0:
            self.statesStack[0].render()