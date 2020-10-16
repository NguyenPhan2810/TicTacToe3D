from GameObject import *
import GLShapes
import enum
import configuration as cfg
from pygame import time
import math

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
            self.meshData.surfacesColor = [color]
            self.color = color


class Plane(GameObject):
    def __init__(self, color=None):
        GameObject.__init__(self)
        self.titles = []

        loopRange = range(int(-cfg.nTitles / 2), int(cfg.nTitles / 2 + 1))

        for x in loopRange:
            row = []
            for z in loopRange:
                newTitle = Title(color)
                newTitle.transform.position[0] = self.transform.position[0] + x * (
                            cfg.nTitles + cfg.titlePositionOffset)
                newTitle.transform.position[2] = self.transform.position[2] + z * (
                            cfg.nTitles + cfg.titlePositionOffset)
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

        self.selectionCount = 0
        self.activePlane = 1
        self.activeRow = 1
        self.activeCol = 1

        self.title3dArray = []
        for i in range(0, cfg.nTitles):
            self.title3dArray += [self.planes[i].titles]

        self.setActiveTitle()

    def update(self, deltaTime):
        GameObject.update(self, deltaTime)

        title = self.planes[self.activePlane].titles[self.activeRow][self.activeCol]
        color = np.array((0.5, 0.5, 0.5)) + math.sin(time.get_ticks() / 1000 * cfg.titleBlinkFreq) / 8
        title.changeToColor(color)

    def setActiveTitle(self, plane=None, row=None, col=None):
        if plane is None:
            plane = self.activePlane
        if row is None:
            row = self.activePlane
        if col is None:
            col = self.activePlane

        title = self.planes[self.activePlane].titles[self.activeRow][self.activeCol]
        color = None
        if title.state == Title.State.player1:
            color = cfg.player1Color
        elif title.state == Title.State.player2:
            color = cfg.player2Color
        else:
            color = cfg.surfacesColor[self.activePlane]

        title.changeToColor(color)
        self.activePlane = plane
        self.activeRow = row
        self.activeCol = col

    # Return True if selection succeeded false if doesn't
    # Return End game result if there is end game
    def selectTitle(self, state: Title.State):
        title = self.planes[self.activePlane].titles[self.activeRow][self.activeCol]
        if title.state == Title.State.default:
            title.state = state
            self.selectionCount += 1

            color = cfg.player1Color if state == Title.State.player1 else cfg.player2Color
            title.changeToColor(color)

            result = self.endgameCheck()
            if result is not None:
                return result
            return True
        return False

    # Return None means nothing
    # Return Title.State.Default means draw
    # Return Title.State.PlayerX means PlayerX wins
    def endgameCheck(self):
        plane = self.activePlane
        row = self.activeRow
        col = self.activeCol
        newestSelection = (plane, row, col)
        title3dArray = self.title3dArray

        if terminalCheck(title3dArray, newestSelection):
            return title3dArray[plane][row][col].state
        elif self.selectionCount == math.pow(cfg.nTitles, 3):
            return Title.State.default
        else:
            return None

# titleArray must be 1d array unwrapped from 3d titles
def terminalCheck(title3dArray, newestMoveIndex) -> bool:
    arr = title3dArray
    p = newestMoveIndex[0]
    r = newestMoveIndex[1]
    c = newestMoveIndex[2]
    n = cfg.nTitles
    state = arr[p][r][c].state

    # Check plane
    for i in range(0, n):
        if arr[i][r][c].state != state:
            break
    else:
        return True

    # Check row
    for i in range(0, n):
        if arr[p][i][c].state != state:
            break
    else:
        return True

    # Check col
    for i in range(0, n):
        if arr[p][r][i].state != state:
            break
    else:
        return True

    # Check diagonal
    if r == c:
        for i in range(0, n):
            if arr[p][i][i].state != state:
                break
        else:
            return True

    # Check anti-diagonal
    if r + c == n - 1:
        for i in range(0, n):
            if arr[p][i][n - 1 - i].state != state:
                break
        else:
            return True

    # Check multiplane row
    if p == r:
        for i in range(0, n):
            if arr[i][i][c].state != state:
                break
        else:
            return True

    # Check multiplane anti-row
    if p + r == n - 1:
        for i in range(0, n):
            if arr[n - 1 - i][i][c].state != state:
                break
        else:
            return True

    # Check multiplane col
    if p == c:
        for i in range(0, n):
            if arr[i][r][i].state != state:
                break
        else:
            return True

    # Check multiplane anti-col
    if p + c == n - 1:
        for i in range(0, n):
            if arr[n - 1 - i][r][i].state != state:
                break
        else:
            return True

    # Check multiplane diagonal
    if r == c:
        for i in range(0, n):
            if arr[i][i][i].state != state:
                break
        else:
            return True

        for i in range(0, n):
            if arr[n - 1 - i][i][i].state != state:
                break
        else:
            return True

    # Check multiplane anti-diagonal
    if r + c == n - 1:
        for i in range(0, n):
            if arr[p][i][n - 1 - i].state != state:
                break
        else:
            return True

        for i in range(0, n):
            if arr[n - 1 - i][i][n - 1 - i].state != state:
                break
        else:
            return True

    return False
