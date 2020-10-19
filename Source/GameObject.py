import numpy as np
from OpenGL.GL import *

class Transform:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.globalPosition = np.array([0.0, 0.0, 0.0])
        self.scale = 1.0
        self.globalScale = 1.0


class GLObjectData:
    def __init__(self, vertices, edges, surfaces, verticesColor=None):
        self.vertices = np.array(vertices)
        self.edges = np.array(edges)
        self.surfaces = np.array(surfaces)
        self.verticesColor = verticesColor

    def draw(self, transform: Transform):
        if self.verticesColor is None:
            return

        glBegin(GL_QUADS)
        for surface in self.surfaces:
            for vertex in surface:
                glColor3fv(np.array(self.verticesColor) / 255)
                glVertex3fv((self.vertices[vertex] * transform.globalScale) + transform.globalPosition)
        glEnd()


# GameObject is a fixed in position object in a scene
# update method is to update logic, state of an object
# render method helps the object to be visible
class GameObject:
    def __init__(self, glObjectData=None):
        self.transform = Transform()
        self.meshData = glObjectData
        self.children = []
        self.parent = None

    def setParent(self, parent):
        self.parent = parent
        self.parent.addChild(self)

    def addChild(self, child):
        self.children += [child]

    def reset(self):
        for i in range(0, len(self.children)):
            self.children[i].reset()

    def event(self, pygameEvents):
        for i in range(0, len(self.children)):
            self.children[i].event(pygameEvents)

    def update(self, deltaTime: float):
        if self.parent is not None:
            self.transform.globalScale = self.parent.transform.globalScale * self.transform.scale
            self.transform.globalPosition = (self.parent.transform.globalPosition + self.transform.position * self.parent.transform.globalScale)

        for i in range(0, len(self.children)):
            self.children[i].update(deltaTime)

    def lateUpdate(self, deltaTime: float):
        for i in range(0, len(self.children)):
            self.children[i].lateUpdate(deltaTime)

    def draw(self):
        if self.meshData is not None:
            self.meshData.draw(self.transform)
        for i in range(0, len(self.children)):
            self.children[i].draw()

    def move(self, direction):
        self.transform.position += np.array(direction)
        for i in range(0, len(self.children)):
            self.children[i].move(direction)