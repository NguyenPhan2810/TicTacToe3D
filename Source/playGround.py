from  gameObject import *
import GLShapes
import  numpy as np
from math import sin

class PlayGround(GameObject):
    def __init__(self):
        GameObject.__init__(self)

        self.surfacesColor = (
            (0.6, 0.1, 0.2),
            (0.2, 0.7, 0.4),
            (0.8, 0.2, 0.6)
        )

        self.planes = []
        for y in range(-1, 2):
            i = y + 1
            vertx = GLShapes.Square.verticies()
            newPlane = Plane()
            newPlane.changeToColor(self.surfacesColor[i])
            newPlane.move((0, y * 1.5, 0))
            newPlane.transform.scale = 0.3
            newPlane.setParent(self)
            self.planes += [newPlane]

    def update(self, deltaTime):
        GameObject.update(self, deltaTime)

    def getTitleOnClick(self):
        gluUnProject()
        return None

class Title(GameObject):
    def __init__(self,  color = None):
        vertx, edges, faces = GLShapes.Square.data()
        GameObject.__init__(self, GLObjectData(vertx, edges, faces, color))

    def changeToColor(self, color):
        self.meshData.surfacesColor = [color]

class Plane(GameObject):
    def __init__(self, color = None):
        GameObject.__init__(self)
        self.titles = []

        nTitles = 3
        titlePositionOffset = 0.75
        loopRange = range(int(-nTitles/2), int(nTitles/2+1))

        for x in loopRange:
            row = []
            for z in loopRange:
                newTitle = Title(color)
                newTitle.transform.position[0] = self.transform.position[0] + x * (nTitles) * titlePositionOffset
                newTitle.transform.position[2] = self.transform.position[2] + z * (nTitles) * titlePositionOffset
                newTitle.setParent(self)
                row += [newTitle]
            self.titles += [row]

    def changeToColor(self, color):
        for i in range(0, len(self.titles)):
            for j in range(0, len(self.titles[i])):
                self.titles[i][j].changeToColor(color)
