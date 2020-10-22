import numpy as np
from math import *
from OpenGL.GL import *

class Transform:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.scale = np.array([1.0, 1.0, 1.0])
        self.rotation = np.array([0.0, 0.0, 0.0]) # degree


class GLMeshData:
    def __init__(self, vertices, edges, surfaces, verticesColor=None):
        self.vertices = np.array(vertices)
        self.edges = np.array(edges)
        self.surfaces = np.array(surfaces)
        self.verticesColor = verticesColor


# GameObject is a fixed in position object in a scene
# update method is to update logic, state of an object
# render method helps the object to be visible
class GameObject:
    def __init__(self, glObjectData: GLMeshData=None):
        self.transform = Transform()
        self.globalTransform = Transform()
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
            self.globalTransform.scale = self.parent.globalTransform.scale * self.transform.scale
            self.globalTransform.position = (self.parent.globalTransform.position + self.transform.position * self.parent.globalTransform.scale)
            self.globalTransform.rotation = self.parent.globalTransform.rotation + self.transform.rotation

    def updateRotation(self):
        if self.children is None:
            return

        rotMat = rotationMatrix(self.transform.rotation)

        self.globalTransform.position = np.matmul(rotMat, self.globalTransform.position)

        self.updateChildRotation(rotMat)

        for child in self.children:
            child.updateRotation()

    def updateChildRotation(self, rotationMatrix):
            for child in self.children:
                child.globalTransform.position = np.matmul(rotationMatrix, child.globalTransform.position)
                child.updateChildRotation(rotationMatrix)

    def glCalculateTransform(self, vertices):
        vertices = vertices.transpose()
        rotMat = rotationMatrix(self.globalTransform.rotation)
        scaleMat = scaleMatrix(self.globalTransform.scale)
        vertices = np.matmul(scaleMat, vertices)
        vertices = np.matmul(rotMat, vertices)
        vertices = vertices.transpose()
        vertices = vertices + self.globalTransform.position

        return vertices


    def glDraw(self):
        vertices = self.glCalculateTransform(self.meshData.vertices)
        glBegin(GL_QUADS)
        for surface in self.meshData.surfaces:
            for vertex in surface:
                glColor3fv(np.array(self.meshData.verticesColor) / 255)
                glVertex3fv(vertices[vertex])
        glEnd()

    def move(self, direction):
        self.transform.position += np.array(direction)
        for i in range(0, len(self.children)):
            self.children[i].move(direction)


# x, y, z are rotation degree in x, y, z axis respectively
def rotationMatrix(rotation):
    alpha = radians(rotation[2])
    beta = radians(rotation[1])
    yeta = radians(rotation[0])

    yawMat = np.array([[cos(alpha), sin(alpha), 0], [-sin(alpha), cos(alpha), 0], [0, 0, 1]])
    pitchMat = np.array([[cos(beta), 0, -sin(beta)], [0, 1, 0], [sin(beta), 0, cos(beta)]])
    rollMat = np.array([[1, 0, 0], [0, cos(yeta), sin(yeta)], [0, -sin(yeta), cos(yeta)]])
    rotationMat = np.matmul(yawMat, pitchMat, rollMat)

    return rotationMat

def scaleMatrix(scale):
    return np.array([[scale[0], 0, 0,], [0, scale[1], 0], [0, 0, scale[2]]])



