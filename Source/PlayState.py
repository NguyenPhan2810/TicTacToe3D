from GameState import *
from PlayGround import *
import pygame
from OpenGL.GL import *
import configuration as cfg
import enum


class GameStatus(enum.Enum):
    player1 = 0
    player2 = 1
    gameOver = 2

class PlayState(BaseState):
    def __init__(self, player1Controller, player2Controller):
        self.isGameOver = False
        self.state = GameStatus(0)
        self.objectRoot = GameObject()
        self.players = [player1Controller, player2Controller]
        self.playGround = PlayGround()
        self.playGround.setParent(self.objectRoot)
        for player in self.players:
            player.setParent(self.objectRoot)


        self.previousMousePosition = np.array([0, 0, 0])
        self.mouseHold = False

    def constructor(self):
        BaseState.constructor(self)

        glTranslatef(0, 0, cfg.cameraZOffset)
        glRotatef(cfg.cameraXRotate, 1, 0, 0)

        self.objectRoot.reset()
        self.state = GameStatus.player1

    def reset(self):
        self.objectRoot.reset()

    def eventHandling(self, events):
        BaseState.eventHandling(self, events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isGameOver = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.previousMousePosition = pygame.mouse.get_pos()
                self.mouseHold = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseHold = False

        self.objectRoot.event(events)

        return False

    def update(self, deltaTime: float) -> bool:
        if self.isGameOver:
            return False

        BaseState.update(self, deltaTime)
        self.objectRoot.update(deltaTime)

        if self.mouseHold:
            mousePos = pygame.mouse.get_pos()
            rotation = (mousePos[0] - self.previousMousePosition[0]) * cfg.mouseRotationSensitivity
            self.previousMousePosition = mousePos

            if rotation != 0:
                glRotatef(abs(rotation), 0, rotation, 0)

        if self.state != GameStatus.gameOver:
            self.controller()

        return True

    def lateUpdate(self, deltaTime: float):
        BaseState.lateUpdate(self, deltaTime)

        self.objectRoot.lateUpdate(deltaTime)

    def draw(self):
        BaseState.draw(self)

        # Draw to buffer
        self.objectRoot.draw()

        return False

    def controller(self):
        playerIndex = 0 if self.state == self.state.player1 else 1
        activeTitle = self.players[playerIndex].activeTitle(self.playGround.title3dArray, self.state)
        if activeTitle is not None:
            self.playGround.setActiveTitle(activeTitle[0], activeTitle[1], activeTitle[2])
        else:
            self.playGround.setActiveTitle()
        if self.players[playerIndex].selectTitle() and activeTitle is not None:
            titleSelected = activeTitle
            titleState = None
            if self.state == GameStatus.player1:
                titleState = Title.State.player1
            elif self.state == GameStatus.player2:
                titleState = Title.State.player2
            self.playGround.activePlane = titleSelected[0]
            self.playGround.activeRow = titleSelected[1]
            self.playGround.activeCol = titleSelected[2]
            checkState = self.playGround.selectTitle(titleState)
            if checkState == True:
                if titleState == Title.State.player1:
                    self.state = self.state.player2
                elif titleState == Title.State.player2:
                    self.state = self.state.player1
            elif type(checkState) is not bool:
                self.state = GameStatus.gameOver
