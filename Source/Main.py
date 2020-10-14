import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialization
verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1 ,1 ,1),
    (-1, -1, 1)
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
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (3, 0, 4, 7)
)

colors = [(r, g, b) for r in (0, 1) for g in (0, 1) for b in (0,1)]

def Cube():
    glBegin(GL_QUADS)
    x = -8
    for surface in surfaces:
        for vertex in surface:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

def main():
    pygame.init()
    displaySize = (600, 600)
    displayAspectRatio = displaySize[0]/displaySize[1]
    pygame.display.set_mode(displaySize, DOUBLEBUF|OPENGL)

    gluPerspective(60, displayAspectRatio, 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5.0)
    glRotatef(20, 0, 0, 0)

    # Main loop
    isGameQuit = True
    while isGameQuit:
        # Event
        for event in pygame.event.get():
            if event == pygame.QUIT:
                isGameQuit = False

        # Logic
        glRotatef(1, 3, 1, 1)

        # Render
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.delay(10)


main()














