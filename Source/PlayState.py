from GameState import *
from PlayGround import *
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import configuration as cfg
from pygame.locals import *
import enum

class GameStatus(enum.Enum):
    player1 = 0
    player2 = 1
    gameOver = 2


class PlayState(BaseState):
    def __init__(self, player1Controller, player2Controller):
        self.exit = False
        self.state = GameStatus(0)
        self.pushState = None
        self.objectRoot = GameObject()
        self.players = [player1Controller, player2Controller]
        self.playGround = PlayGround()
        self.playGround.setParent(self.objectRoot)

        for player in self.players:
            player.setParent(self.objectRoot)

        self.playgroundRotationX = 0
        self.mouseHold = False

    def constructor(self):
        self.objectRoot.constructor()

        pygame.display.set_mode(cfg.displaySize, DOUBLEBUF | OPENGL)
        glEnable(GL_DEPTH_TEST)
        gluPerspective(cfg.FOV, cfg.displayAspectRatio, cfg.nearClippingPlane, cfg.farClippingPlane)
        glFrontFace(GL_CW)
        glTranslatef(0, 0, cfg.cameraZOffset)
        glRotatef(cfg.cameraXRotate, 1, 0, 0)
        self.playgroundRotationX = cfg.cameraXRotate
        glClearColor(cfg.backgroundColor[0] / 255, cfg.backgroundColor[1] / 255, cfg.backgroundColor[2] / 255, 1)

        self.objectRoot.reset()
        self.state = GameStatus.player1

    def destructor(self):
        self.objectRoot.destructor()

    def reset(self):
        self.objectRoot.reset()
        self.state = GameStatus.player1
        self.state = GameStatus(0)

        self.playgroundRotationX = 0
        self.mouseHold = False
        self.pushState = None
        self.exit = False

    def eventHandling(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset()
                if event.key == pygame.K_ESCAPE:
                    self.exit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.mouse.get_rel()
                    self.mouseHold = True
                elif event.button == 4:
                    self.playGround.transform.scale *= cfg.playGroundZoomAmount
                elif event.button == 5:
                    self.playGround.transform.scale /= cfg.playGroundZoomAmount
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouseHold = False

        self.objectRoot.event(events)

        return False

    def update(self, deltaTime: float) -> bool:
        # Terminal check
        if self.exit:
            from MenuState import MenuState
            self.pushState = MenuState()

        # Update object tree
        BaseState.update(self, deltaTime)
        self.objectRoot.update(deltaTime)

        # Update playground
        if self.mouseHold:
            dx, dy = pygame.mouse.get_rel()
            rotationX = dy * cfg.mouseRotationSensitivity
            rotationY = dx * cfg.mouseRotationSensitivity
            self.playgroundRotationX += rotationX
            if -cfg.playGroundMaxRotationX <= self.playgroundRotationX <= cfg.playGroundMaxRotationX:
                glRotatef(rotationX, 1, 0, 0)
            self.playgroundRotationX = max(self.playgroundRotationX, -cfg.playGroundMaxRotationX)
            self.playgroundRotationX = min(self.playgroundRotationX, cfg.playGroundMaxRotationX)
            self.playGround.transform.rotation[1] -= rotationY

        # Check picking
        self.updatePicking()

        # Game over
        if not self.isGameOver():
            self.controller()

        return True

    def lateUpdate(self, deltaTime: float):
        self.objectRoot.lateUpdate(deltaTime)

    def render(self):
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        BaseState.render(self)

        # Draw to buffer
        self.objectRoot.draw()

        # Display
        pygame.display.flip()

    def isGameOver(self):
        return self.state == GameStatus.gameOver

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

    def requestPushState(self):
        return self.pushState

    def requestPopState(self):
        return self.exit

    def updatePicking(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.objectRoot.drawPicking()

        x, y = pygame.mouse.get_pos()
        y = cfg.displaySize[1] - y  # This is to match OpenGL and pygame up
        r, g, b = glReadPixels(x, y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
        pixelColor = (r, g, b)
        self.objectRoot.updatePicking(pixelColor)
