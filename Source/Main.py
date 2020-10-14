import pygame
import numpy
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialization
verticies = (
    (-1, -1,-1),
    (1, -1,  -1),
    (1, -1, 1),
    (-1, -1, 1),
    (-1, 0, -1),
    (1, 0, -1),
    (1, 0, 1),
    (-1, 0, 1),
    (-1, 1, -1),
    (1,  1,  -1),
    (1, 1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (8, 9),
    (9, 10),
    (10, 11),
    (11, 8)
)

surfaces = (
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (8, 9, 10, 11)
)

colors = [(r, g, b) for r in (0, 1) for g in (0, 1) for b in (0, 1)]

def Cube():
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = -5
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

def main():
    pygame.init()
    displaySize = (600, 600)
    mouseOrigin = numpy.array((int(displaySize[0] / 2), int(displaySize[1] / 2)))
    displayAspectRatio = displaySize[0]/displaySize[1]
    pygame.display.set_mode(displaySize, DOUBLEBUF|OPENGL)
    pygame.mouse.set_pos(mouseOrigin)
    pygame.mouse.set_visible(False)

    gluPerspective(60, displayAspectRatio, 0.1, 50.0)
   

    # Main loop
    isGameRunning = True
    while isGameRunning:
        velocity = numpy.array([0.0,  0.0, 0.0])

        # Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isGameRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    velocity[0] = -1
                if event.key == pygame.K_d:
                    velocity[0] = 1
                if event.key == pygame.K_w:
                    velocity[1] = 1
                if event.key == pygame.K_s:
                    velocity[1] = -1
                if event.key == pygame.K_ESCAPE:
                    isGameRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    velocity[2] = 1  if event.button == 4 else -1

        # Logic
        deltaMousePos = numpy.array(pygame.mouse.get_pos()) - mouseOrigin
        pygame.mouse.set_pos(mouseOrigin)
        glRotatef(1, deltaMousePos[1],  deltaMousePos[0],  0)

        velocity *= 0.1
        glTranslatef(velocity[0], velocity[1], velocity[2])

        # Render
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.delay(10)
    quit()

main()














