from gameObject import *
from playGround import *
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import configuration as cfg
import enum

class GameState(enum.Enum):
    player1 = 0
    player2 = 1
    gameOver = 2

class MovementState(enum.Enum):
    default = 0
    forward = 1
    backward = 2
    left = 3
    right = 4
    up = 5
    down = 6

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode(cfg.displaySize, DOUBLEBUF | OPENGL)
        gluPerspective(cfg.FOV, cfg.displayAspectRatio, cfg.nearClippingPlane, cfg.farClippingPlane)

        self.isGameRunning = True
        self.state = GameState(0)
        self.movementState = MovementState(0)
        self.selectTitle = False
        self.objectRoot = GameObject()

        self.previousMousePosition = np.array([0, 0, 0])
        self.mouseHold = False

        self.constructScene()

    def constructScene(self):
        glTranslatef(0, 0, cfg.cameraZOffset)
        glRotatef(cfg.cameraXRotate, 1, 0, 0)

        self.playGround = PlayGround()
        self.playGround.setParent(self.objectRoot)

    def play(self):
        self.state = GameState.player1

        prevTime = pygame.time.get_ticks()
        while self.isGameRunning:
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
            self.update(dt)
            # Render
            self.render()

    def eventHandling(self):
        self.movementState = MovementState.default
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isGameRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.isGameRunning = False
                elif event.key == pygame.K_a: self.movementState = MovementState.left
                elif event.key == pygame.K_d: self.movementState = MovementState.right
                elif event.key == pygame.K_w: self.movementState = MovementState.forward
                elif event.key == pygame.K_s: self.movementState = MovementState.backward
                elif event.key == pygame.K_SPACE: self.movementState = MovementState.up
                elif event.key == pygame.K_LCTRL: self.movementState = MovementState.down
                elif event.key == pygame.K_f: self.selectTitle = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.previousMousePosition = pygame.mouse.get_pos()
                self.mouseHold = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseHold = False

    def update(self, deltaTime: float):
        self.objectRoot.update(deltaTime)

        if self.mouseHold:
            mousePos = pygame.mouse.get_pos()
            rotation = mousePos[0] - self.previousMousePosition[0]
            self.previousMousePosition = mousePos

            if rotation != 0:
                glRotatef(abs(rotation), 0, rotation, 0)

        if self.movementState != MovementState.default:
            plane = self.playGround.activePlane
            row = self.playGround.activeRow
            col = self.playGround.activeCol

            if self.movementState == MovementState.right:               row = row + 1 if row < cfg.nTitles - 1 else row
            elif self.movementState == MovementState.left:              row = row - 1 if row > 0 else row
            elif self.movementState == MovementState.up:                plane = plane + 1 if plane < cfg.nTitles - 1 else plane
            elif self.movementState == MovementState.down:          plane = plane - 1 if plane > 0  else plane
            elif self.movementState == MovementState.backward:  col = col + 1 if col < cfg.nTitles - 1 else col
            elif self.movementState == MovementState.forward:      col = col - 1 if col > 0 else col

            self.playGround.setActiveTitle(plane, row, col)

        if self.selectTitle:
            self.selectTitle = False
            titleState = None
            if self.state == GameState.player1: titleState = Title.State.player1
            elif self.state == GameState.player2: titleState = Title.State.player2
            if self.playGround.selectTitle(titleState):
                if titleState == Title.State.player1: self.state = self.state.player2
                elif titleState == Title.State.player2: self.state = self.state.player1

    def render(self):
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(cfg.backgroundColor[0], cfg.backgroundColor[1], cfg.backgroundColor[2], 1)

        # Draw to buffer
        self.objectRoot.render()

        # Display
        pygame.display.flip()
