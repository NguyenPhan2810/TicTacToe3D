from  gameObject import *
import GLShapes
import enum
import configuration as cfg
from pygame import time
from math import sin

class Title(GameObject):
    class State(enum.Enum):
        default = 0
        player1 = 1
        player2 = 2

    def __init__(self,  color = None):
        vertx, edges, faces = GLShapes.Square.data()
        GameObject.__init__(self, GLObjectData(vertx, edges, faces, color))
        self.state = Title.State(0)
        self.color = color

    def changeToColor(self, color = None):
        if color is not None:
            self.meshData.surfacesColor = [color]
            self.color = color

    def changeToState(self,  state: State):
        self.state = state
        color = None
        if state == Title.State.player1: color = cfg.player1Color
        elif state == Title.State.player2: color = cfg.player2Color
        self.changeToColor(color)


class Plane(GameObject):
    def __init__(self, color = None):
        GameObject.__init__(self)
        self.titles = []

        loopRange = range(int(-cfg.nTitles/2), int(cfg.nTitles/2+1))

        for x in loopRange:
            row = []
            for z in loopRange:
                newTitle = Title(color)
                newTitle.transform.position[0] = self.transform.position[0] + x * (cfg.nTitles + cfg.titlePositionOffset)
                newTitle.transform.position[2] = self.transform.position[2] + z * (cfg.nTitles + cfg.titlePositionOffset)
                newTitle.setParent(self)
                row += [newTitle]
            self.titles += [row]

    def changeToColor(self, color):
        for i in range(0, len(self.titles)):
            for j in range(0, len(self.titles[i])):
                self.titles[i][j].changeToColor(color)


class PlayGround(GameObject):
    def __init__(self):
        GameObject.__init__(self)

        self.planes = []
        for y in range(-1, 2):
            i = y + 1
            vertx = GLShapes.Square.verticies()
            newPlane = Plane()
            newPlane.changeToColor(cfg.surfacesColor[i])
            newPlane.move((0, y * cfg.planeSpacingMultipler, 0))
            newPlane.transform.scale = cfg.playGroundScale
            newPlane.setParent(self)
            self.planes += [newPlane]

        self.activePlane = 1
        self.activeRow = 1
        self.activeCol = 1
        self.setActiveTitle()

    def setActiveTitle(self, plane = None, row = None, col = None):
        if plane is None:
            plane = self.activePlane
        if row is None:
            row = self.activePlane
        if col is None:
            col = self.activePlane

        title = self.planes[self.activePlane].titles[self.activeRow][self.activeCol]
        color = None
        if title.state == Title.State.player1: color = cfg.player1Color
        elif title.state == Title.State.player2: color = cfg.player2Color
        else: color = cfg.surfacesColor[self.activePlane]

        title.changeToColor(color)
        self.activePlane = plane
        self.activeRow = row
        self.activeCol = col

    def selectTitle(self, state: Title.State):
        title = self.planes[self.activePlane].titles[self.activeRow][self.activeCol]
        if title.state == Title.State.default:
            title.changeToState(state)
            return True
        return False

    def update(self, deltaTime):
        GameObject.update(self, deltaTime)

        title = self.planes[self.activePlane].titles[self.activeRow][self.activeCol]
        color = np.array((0.5, 0.5, 0.5)) + sin(time.get_ticks() / 1000 * cfg.titleBlinkFreq) / 8
        title.changeToColor(color)

    def getTitleOnClick(self):
        gluUnProject()
        return None

