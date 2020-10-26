import numpy as np
from math import *
from OpenGL.GL import *
import GLShapes
import copy

class Transform:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.scale = np.array([1.0, 1.0, 1.0])
        self.rotation = np.array([0.0, 0.0, 0.0]) # degree

# GameObject is a fixed in position object in a scene
# update method is to update logic, state of an object
# render method helps the object to be visible
class GameObject:
    id = 0
    def __init__(self):
        self.transform = Transform()
        self.globalTransform = Transform()
        self.prevGlobalTransform = Transform()
        self.meshData = None
        self.transformedVerticesArray = None

        self.children = []
        self.parent = None

        self.isPicked = False # If this object is picked by the mouse or not
        self.isPickable = False
        self.id = GameObject.id
        GameObject.id += 1

    def setParent(self, parent):
        self.parent = parent
        self.parent.addChild(self)

    def addChild(self, child):
        self.children += [child]

    def reset(self):
        for i in range(0, len(self.children)):
            self.children[i].reset()

    def constructor(self):
        for i in range(0, len(self.children)):
            self.children[i].constructor()

    def destructor(self):
        for i in range(0, len(self.children)):
            self.children[i].destructor()

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
        for child in self.children:
            child.lateUpdate(deltaTime)

        if self.meshData is not None and self.prevGlobalTransform != self.globalTransform:
           self.glPreprocessVertices()

    def draw(self):
        if self.meshData is not None:
            self.glDraw()
        for i in range(0, len(self.children)):
            self.children[i].draw()

    def glDraw(self):
        if self.transformedVerticesArray is None:
            return

        vertexRange = range(4)
        colorArray = self.meshData.surfaceColors / 255

        glBegin(GL_QUADS)
        index = 0
        for surface in range(len(self.meshData.surfaces)):
            glColor3fv(colorArray[surface])
            for vertex in vertexRange:
                glVertex3f(*self.transformedVerticesArray[index])
                index += 1
        glEnd()

    def drawPicking(self):
        if self.meshData is not None and self.isPickable:
            self.glDrawPicking()
        for i in range(0, len(self.children)):
            self.children[i].drawPicking()

    def glDrawPicking(self):
        if self.transformedVerticesArray is None:
            return

        glBegin(GL_QUADS)
        glColor3fv(np.array(self.idToColor()) / 255)
        for vertex in range(len(self.transformedVerticesArray)):
            glVertex3f(*self.transformedVerticesArray[vertex])
        glEnd()

    # Return true if this object or children picked
    def updatePicking(self, pickedColor):
        if self.idToColor() == pickedColor and self.isPickable:
            self.isPicked = True
            return True
        else:
            self.isPicked = False
            for child in self.children:
                if child.updatePicking(pickedColor):
                    return True
            else:
                return False

    def updateTransform(self):
        self.prevGlobalTransform = copy.deepcopy(self.globalTransform)
        if self.parent is None:
            self.globalTransform = self.transform
        else:
            self.globalTransform.scale = self.parent.globalTransform.scale * self.transform.scale
            self.globalTransform.position = (self.parent.globalTransform.position + self.transform.position * self.parent.globalTransform.scale)
            self.globalTransform.rotation = self.parent.globalTransform.rotation + self.transform.rotation

    def updateRotation(self):
        rotMat = rotationMatrix(self.globalTransform.rotation)
        self.globalTransform.position = np.matmul(rotMat, self.globalTransform.position)

        for child in self.children:
            child.updateRotation()

    def glPreprocessVertices(self):
        vertices = self.meshData.vertices
        vertices = vertices.transpose()
        rotMat = rotationMatrix(self.globalTransform.rotation)
        scaleMat = scaleMatrix(self.globalTransform.scale)
        vertices = np.matmul(scaleMat, vertices)
        vertices = np.matmul(rotMat, vertices)
        vertices = vertices.transpose()
        vertices = vertices + self.globalTransform.position

        vertexArray = []
        for surface in self.meshData.surfaces:
            for vertex in surface:
                vertexArray += [vertices[vertex]]

        self.transformedVerticesArray = vertexArray

    def idToColor(self):
        r = (self.id & 0x0000ff) >> 0
        g = (self.id & 0x00ff00) >> 8
        b = (self.id & 0xff0000) >> 16
        return (r, g, b)

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
    rotationMat = np.matmul(yawMat, pitchMat)
    rotationMat = np.matmul(rotationMat, rollMat)

    return rotationMat

def scaleMatrix(scale):
    return np.array([[scale[0], 0, 0,], [0, scale[1], 0], [0, 0, scale[2]]])



