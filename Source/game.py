from  gameObject import *
from playGround import *
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Game:
    def  __init__(self):
        pygame.init()
        displaySize = (800, 800)
        displayAspectRatio = displaySize[0]/displaySize[1]
        pygame.display.set_mode(displaySize, DOUBLEBUF|OPENGL)
        gluPerspective(30, displayAspectRatio, 0.1, 50.0)
        self.backgroundColor = (0.2, 0.2, 0.2)

        self.isGameRunning = True
        self.objectRoot = GameObject()

        self.previousMousePosition = np.array([0, 0, 0])
        self.mouseHold = False

        self.constructScene()

    def constructScene(self):
        glTranslatef(0,  0, -7)
        glRotatef(22, 1, 0, 0)

        self.playGround = PlayGround()
        self.playGround.setParent(self.objectRoot)

    def play(self):
        while self.isGameRunning:
            # Events
            self.eventHandling()
            # Update
            self.update()
            # Render
            self.render()
            pygame.time.delay(10)

    def eventHandling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isGameRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                   self.isGameRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.previousMousePosition = pygame.mouse.get_pos()
                self.mouseHold = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouseHold = False


    def update(self):
        self.objectRoot.update(0.01)

        if self.mouseHold:
            mousePos = pygame.mouse.get_pos()
            rotation = mousePos[0] - self.previousMousePosition[0]
            self.previousMousePosition = mousePos

            if rotation != 0:
                glRotatef(abs(rotation), 0, rotation, 0)

    def render(self):
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(self.backgroundColor[0], self.backgroundColor[1], self.backgroundColor[2], 1)

        # Draw to buffer
        self.objectRoot.render()

        # Display
        pygame.display.flip()