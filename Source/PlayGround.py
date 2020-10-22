from GameObject import *
import GLShapes
import enum
import configuration as cfg
from pygame import time
import math
import copy
import numpy as np

class Title(GameObject):
    class State(enum.Enum):
        default = 0
        player1 = 1
        player2 = 2

    def __init__(self, color=None):
        vertx, edges, faces = GLShapes.Square.data()
        GameObject.__init__(self, GLObjectData(vertx, edges, faces, color))
        self.state = Title.State(0)
        self.color = color

    def changeToColor(self, color=None):
        if color is not None:
            self.meshData.verticesColor = [color]
            self.color = color

class Plane(GameObject):
    def __init__(self, color=None):
        GameObject.__init__(self)
        self.titles = []
        n = cfg.nTitles
        loopRange = np.arange(-1, 1.01, 2.0 / (n - 1)) # Get the titles center to 0
        for x in loopRange:
            row = []
            for z in loopRange:
                newTitle = Title(color)
                newTitle.transform.position[0] = self.transform.position[0] + x
                newTitle.transform.position[2] = self.transform.position[2] + z
                newTitle.transform.scale = 1 / (n + cfg.titlesPadding)
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

        self.terminalTitlesColor = None
        self.terminalTitles = None
        self.totalTime = 0.0

        self.planes = []
        self.transform.scale = cfg.playGroundScale

        n = cfg.nTitles
        for y in np.arange(-0.5, 0.51, 1.0 / (n - 1)):  # Make planes center to 0
            i = y + 1
            vertx = GLShapes.Square.verticies()
            newPlane = Plane()
            newPlane.move((0, y * cfg.planeSpacingMultiplier, 0))
            newPlane.setParent(self)
            self.planes += [newPlane]

        self.selectionCount = 0
        self.activeTitleIndex = None
        self.activeTitlePreservedTransform = None

        self.title3dArray = []
        for i in range(0, n):
            self.title3dArray += [self.planes[i].titles]

        # Setup color
        self.resetColor()

        self.setActiveTitle()

    def reset(self):
        GameObject.reset(self)

        self.totalTime = 0.0
        self.terminalTitles = None
        self.resetColor()

        for i in range(0, cfg.nTitles):
            for j in range(0, cfg.nTitles):
                for k in range(0, cfg.nTitles):
                    self.title3dArray[i][j][k].state = Title.State.default

    def resetColor(self):
        index = 0
        for i in range(0, cfg.nTitles):
            for j in range(0, cfg.nTitles):
                for k in range(0, cfg.nTitles):
                    title = self.title3dArray[i][j][k]
                    title.changeToColor(cfg.titlesColor[index])
                    index += 1

    def lateUpdate(self, deltaTime):
        GameObject.lateUpdate(self, deltaTime)
        self.totalTime += deltaTime

        if self.activeTitleIndex is not None:
            title = self.title3dArray[self.activeTitleIndex[0]][self.activeTitleIndex[1]][self.activeTitleIndex[2]]
            oldTransform = self.activeTitlePreservedTransform

            dx = cfg.titleWiggleAmount * math.cos(self.totalTime * cfg.titleWiggleFrequency)
            dz = cfg.titleWiggleAmount * math.sin(self.totalTime * cfg.titleWiggleFrequency)
            ds = cfg.titleScaleAmount * math.sin(self.totalTime * cfg.titleScaleFrequency)
            newX = oldTransform.position[0] + dx
            newZ = oldTransform.position[2] + dz
            newS = oldTransform.scale + ds
            title.transform.position[0] = newX
            title.transform.position[2] = newZ
            title.transform.scale = newS

        if self.terminalTitles is not None:
            for index in self.terminalTitles:
                title = self.title3dArray[index[0]][index[1]][index[2]]
                if self.terminalTitlesColor is None:
                    self.terminalTitlesColor = title.color
                r, g, b = self.terminalTitlesColor
                change = math.sin(self.totalTime * cfg.terminalTitleColorChangeFreq) * cfg.terminalTitleColorChangeAmount
                r += change
                g += change
                b += change
                title.changeToColor((r, g, b))

    def setActiveTitle(self, plane=None, row=None, col=None):
        index = self.activeTitleIndex

        # Prevent recall the function multiple times
        if index is not None and plane is not None and row is not None and col is not None:
            if index[0] == plane and index[1] == row and index[2] == col:
                return

        # Kind of reset if no coordinates are provided
        if index is not None:
            oldTitle = self.title3dArray[index[0]][index[1]][index[2]]
            oldTitle.transform = self.activeTitlePreservedTransform
            self.activeTitlePreservedTransform = None
            self.activeTitleIndex = None

        if plane is None or row is None or col is None:
            self.totalTime = 0.0
            return

        # If no players has taken the title yet then choose it
        newTitle = self.title3dArray[plane][row][col]
        if newTitle.state == Title.State.default:
            self.activeTitleIndex = [plane, row, col]
            self.activeTitlePreservedTransform = copy.deepcopy(newTitle.transform)

    # Return True if selection succeeded false if doesn't
    # Return End game result if there is end game
    def selectTitle(self, state: Title.State):
        if self.activeTitleIndex is None:
            return False

        title = self.title3dArray[self.activeTitleIndex[0]][self.activeTitleIndex[1]][self.activeTitleIndex[2]]
        if title.state == Title.State.default:
            title.state = state
            self.selectionCount += 1

            color = cfg.player1Color if state == Title.State.player1 else cfg.player2Color
            title.changeToColor(color)

            result = self.endgameCheck()
            self.setActiveTitle()
            if result is not None:
                return result
            return True
        return False

    # Return None means nothing
    # Return Title.State.Default means draw
    # Return Title.State.PlayerX means PlayerX wins
    def endgameCheck(self):
        plane = self.activeTitleIndex[0]
        row = self.activeTitleIndex[1]
        col = self.activeTitleIndex[2]
        newestSelection = (plane, row, col)
        title3dArray = self.title3dArray

        self.terminalTitles = terminalCheck(title3dArray, newestSelection)
        if self.terminalTitles is not None:
            return title3dArray[plane][row][col].state
        elif self.selectionCount == math.pow(cfg.nTitles, 3):
            return Title.State.default
        else:
            return None

# titleArray must be 1d array unwrapped from 3d titles
# Return None if terminal condition meet

def terminalCheck(title3dArray, newestMoveIndex):
    arr = title3dArray
    p = newestMoveIndex[0]
    r = newestMoveIndex[1]
    c = newestMoveIndex[2]
    n = cfg.nTitles
    state = arr[p][r][c].state

    # Check plane
    terminalTitles = []
    for i in range(0, n):
        if arr[i][r][c].state != state:
            break
        terminalTitles += [[i, r, c]]
    else:
        return terminalTitles

    # Check row
    terminalTitles = []
    for i in range(0, n):
        if arr[p][i][c].state != state:
            break
        terminalTitles += [[p, i, c]]
    else:
        return terminalTitles

    # Check col
    terminalTitles = []
    for i in range(0, n):
        if arr[p][r][i].state != state:
            break
        terminalTitles += [[p, r, i]]
    else:
        return terminalTitles

    # Check diagonal
    if r == c:
        terminalTitles = []
        for i in range(0, n):
            if arr[p][i][i].state != state:
                break
            terminalTitles += [[p, i, i]]
        else:
            return terminalTitles

    # Check anti-diagonal
    if r + c == n - 1:
        terminalTitles = []
        for i in range(0, n):
            if arr[p][i][n - 1 - i].state != state:
                break
            terminalTitles += [[p, i, n - 1 - i]]
        else:
            return terminalTitles

    # Check multiplane row
    if p == r:
        terminalTitles = []
        for i in range(0, n):
            if arr[i][i][c].state != state:
                break
            terminalTitles += [[i, i, c]]
        else:
            return terminalTitles

    # Check multiplane anti-row
    if p + r == n - 1:
        terminalTitles = []
        for i in range(0, n):
            if arr[n - 1 - i][i][c].state != state:
                break
            terminalTitles += [[n - 1 - i, i, c]]
        else:
            return terminalTitles

    # Check multiplane col
    if p == c:
        terminalTitles = []
        for i in range(0, n):
            if arr[i][r][i].state != state:
                break
            terminalTitles += [[i, r, i]]
        else:
            return terminalTitles

    # Check multiplane anti-col
    if p + c == n - 1:
        terminalTitles = []
        for i in range(0, n):
            if arr[n - 1 - i][r][i].state != state:
                break
            terminalTitles += [[n - 1 - i, r, i]]
        else:
            return terminalTitles

    # Check multiplane diagonal
    if r == c:
        terminalTitles = []
        for i in range(0, n):
            if arr[i][i][i].state != state:
                break
            terminalTitles += [[i, i, i]]
        else:
            return terminalTitles

        terminalTitles = []
        for i in range(0, n):
            if arr[n - 1 - i][i][i].state != state:
                break
            terminalTitles += [[n - 1 - i, i, i]]
        else:
            return terminalTitles

    # Check multiplane anti-diagonal
    if r + c == n - 1:
        terminalTitles = []
        for i in range(0, n):
            if arr[p][i][n - 1 - i].state != state:
                break
            terminalTitles += [[p, i, n - 1 - i]]
        else:
            return terminalTitles

        terminalTitles = []
        for i in range(0, n):
            if arr[n - 1 - i][i][n - 1 - i].state != state:
                break
            terminalTitles += [[n - 1 - i, i, n - 1 - i]]
        else:
            return terminalTitles

    return None
