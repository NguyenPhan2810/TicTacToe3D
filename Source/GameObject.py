import numpy as np
from math import *
from OpenGL.GL import *

class Transform:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.scale = 1.0
        self.rotation = np.array([0.0, 0.0, 0.0]) # degree


class GLObjectData:
    def __init__(self, vertices, edges, surfaces, verticesColor=None):
        self.vertices = np.array(vertices)
        self.edges = np.array(edges)
        self.surfaces = np.array(surfaces)
        self.verticesColor = verticesColor


# GameObject is a fixed in position object in a scene
# update method is to update logic, state of an object
# render method helps the object to be visible
class GameObject:
    def __init__(self, glObjectData=None):
        self.transform = Transform()
        self.meshData = glObjectData
        self.children = []
        self.parent = None

        self.globalPosition = np.array([0.0, 0.0, 0.0])
        self.globalScale = 1.0

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
        self.updateTransform()

        for i in range(0, len(self.children)):
            self.children[i].update(deltaTime)

        if self.parent is None:
            self.updateRotation()

    def lateUpdate(self, deltaTime: float):
        for i in range(0, len(self.children)):
            self.children[i].lateUpdate(deltaTime)

    def draw(self):
        if self.meshData is not None:
            self.glDraw()
        for i in range(0, len(self.children)):
            self.children[i].draw()

    def updateTransform(self):
        if self.parent is not None:
            self.globalScale = self.parent.globalScale * self.transform.scale
            self.globalPosition = (self.parent.globalPosition + self.transform.position * self.parent.globalScale)

    def updateRotation(self):
        if self.children is None:
            return

        x, y, z = self.transform.rotation
        rotMat = rotationMatrix(x, y, z)

        self.updateChildRotation(rotMat)

        for child in self.children:
            child.updateRotation()

    def updateChildRotation(self, rotationMatrix):
            for child in self.children:
                child.globalPosition = np.matmul(rotationMatrix, child.globalPosition)
                child.updateChildRotation(rotationMatrix)

    def glCalculateTransform(self, vertex):

        vertex = (vertex * self.globalScale) + self.globalPosition

        return vertex


    def glDraw(self):
        glBegin(GL_QUADS)
        for surface in self.meshData.surfaces:
            for vertex in surface:
                glColor3fv(np.array(self.meshData.verticesColor) / 255)
                glVertex3fv(self.glCalculateTransform(self.meshData.vertices[vertex]))
        glEnd()

    def move(self, direction):
        self.transform.position += np.array(direction)
        for i in range(0, len(self.children)):
            self.children[i].move(direction)


# x, y, z are rotation degree in x, y, z axis respectively
def rotationMatrix(x, y, z):
    alpha = radians(x)
    beta = radians(y)
    yeta = radians(z)

    yawMat = np.array([[cos(alpha), sin(alpha), 0], [-sin(alpha), cos(alpha), 0], [0, 0, 1]])
    pitchMat = np.array([[cos(beta), 0, -sin(beta)], [0, 1, 0], [sin(beta), 0, cos(beta)]])
    rollMat = np.array([[1, 0, 0], [0, cos(yeta), sin(yeta)], [0, -sin(yeta), cos(yeta)]])
    rotationMat = np.matmul(yawMat, pitchMat, rollMat)

    return rotationMat