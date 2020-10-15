import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class GLObjectData:
    def __init__(self, verticies, edges, surfaces, surfacesColor = None):
        self.verticies = np.array(verticies)
        self.edges = np.array(edges)
        self.surfaces = np.array(surfaces)
        self.surfacesColor = surfacesColor

    def render(self, position):
        glBegin(GL_QUADS)
        colorIndex = 0
        for surface in self.surfaces:
            if self.surfacesColor is not None:
                glColor3fv(self.surfacesColor[colorIndex])
                colorIndex += 1
            for vertex in surface:
                glVertex3fv(self.verticies[vertex] + np.array(position))
        glEnd()

# GameObject is a fixed in position object in a scene
# update method is to update logic, state of an object
# render method helps the object to be visible
class GameObject:
    def __init__(self, meshData = GLObjectData((()),(()),(()))):
        self.position =  np.array([0.0, 0.0, 0.0])
        self.meshData = meshData
    def update(self, deltaTime):
        pass
    def render(self):
        self.meshData.render(self.position)
        pass