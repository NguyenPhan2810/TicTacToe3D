from GameObject import *
from PlayGround import *
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import configuration as cfg
import enum
from Controller import HumanController, MinMaxController

class GameState(enum.Enum):
    player1 = 0
    player2 = 1
    gameOver = 2

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode(cfg.displaySize, DOUBLEBUF | OPENGL)
        gluPerspective(cfg.FOV, cfg.displayAspectRatio, cfg.nearClippingPlane, cfg.farClippingPlane)

        self.isGameRunning = True
        self.state = GameState(0)
        self.objectRoot = GameObject()
        self.players = [MinMaxController(maxDepthSearch=1), MinMaxController(maxDepthSearch=2)]
        self.playGround = PlayGround()
        self.playGround.setParent(self.objectRoot)
        for player in self.players:
            player.setParent(self.objectRoot)


        self.previousMousePosition = np.array([0, 0, 0])
        self.mouseHold = False

        self.constructScene()

    def constructScene(self):
        glTranslatef(0, 0, cfg.cameraZOffset)
        glRotatef(cfg.cameraXRotate, 1, 0, 0)

    def play(self):
        while self.isGameRunning:
            self.state = GameState.player1
            prevTime = pygame.time.get_ticks()

            isGamePlaying = True
            while self.isGameRunning and isGamePlaying:
                # Time
                currentTime = pygame.time.get_ticks()
                dt = (currentTime - prevTime) / 1000
                if dt < cfg.timePerFrame:
                    pygame.time.wait(int((cfg.timePerFrame - dt) * 1000))
                    dt = cfg.timePerFrame

                prevTime = currentTime
                # Events
                self.eventHandling()
                # Update
                isGamePlaying = self.update(dt)
                self.lateUpdate(dt)
                # Render
                self.render()

            if self.isGameRunning:
                pygame.time.wait(5000)
                self.objectRoot.reset()

    def reset(self):
        self.objectRoot.reset()

    def eventHandling(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.isGameRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.isGameRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.previousMousePosition = pygame.mouse.get_pos()
                self.mouseHold = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseHold = False

        self.objectRoot.event(events)

    def update(self, deltaTime: float) -> bool:
        self.objectRoot.update(deltaTime)

        if self.mouseHold:
            mousePos = pygame.mouse.get_pos()
            rotation = mousePos[0] - self.previousMousePosition[0]
            self.previousMousePosition = mousePos

            if rotation != 0:
                glRotatef(abs(rotation), 0, rotation, 0)

        playerIndex = 0 if self.state == self.state.player1 else 1
        activeTitle = self.players[playerIndex].activeTitle(self.playGround.title3dArray, self.state)
        if activeTitle is not None:
            self.playGround.setActiveTitle(activeTitle[0], activeTitle[1], activeTitle[2])
        else:
            self.playGround.setActiveTitle()
        if self.players[playerIndex].selectTitle() and activeTitle is not None:
            titleSelected = activeTitle
            titleState = None
            if self.state == GameState.player1: titleState = Title.State.player1
            elif self.state == GameState.player2: titleState = Title.State.player2
            self.playGround.activePlane = titleSelected[0]
            self.playGround.activeRow = titleSelected[1]
            self.playGround.activeCol = titleSelected[2]
            checkState = self.playGround.selectTitle(titleState)
            if checkState == True:
                if titleState == Title.State.player1: self.state = self.state.player2
                elif titleState == Title.State.player2: self.state = self.state.player1
            elif type(checkState) is not bool:
                print(checkState)
                return False
        return True

    def lateUpdate(self, deltaTime: float):
        self.objectRoot.lateUpdate(deltaTime)

    def render(self):
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(cfg.backgroundColor[0] / 255, cfg.backgroundColor[1] / 255, cfg.backgroundColor[2] / 255, 1)

        # Draw to buffer
        self.objectRoot.render()

        # Display
        pygame.display.flip()
