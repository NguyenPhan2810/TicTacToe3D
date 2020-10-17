from GameObject import *
import pygame
from PlayGround import *
import configuration as cfg
import numpy as np
from MinMaxAlgorithm import MinMax

class Controller(GameObject):
    def __init__(self):
        GameObject.__init__(self)

    # Decide to the active title
    def selectTitle(self) -> bool:
        return False

    # return a 3d list represents (plane, row, col) to mark active title
    def activeTitle(self, title3dArray, gameState):
        return None

class HumanController(Controller):
    def __init__(self):
        Controller.__init__(self)

        self.isSelectTitle = False
        self.isMouseMoved = False
        self.isMouseUp = False
        self.pickingTitle = None

    def reset(self):
        GameObject.reset(self)
        self.pickingTitle = None

    def event(self, pygameEvents):
        Controller.event(self, pygameEvents)

        self.isMouseUp = False
        n = cfg.nTitles
        for event in pygameEvents:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.isMouseMoved = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.isMouseUp = True
            elif event.type == pygame.MOUSEMOTION:
                self.isMouseMoved = True

    def update(self, deltaTime: float):
        Controller.update(self, deltaTime)

        if self.isMouseMoved:
            self.mouseHover()
        if self.isMouseUp and not self.isMouseMoved:
            self.mouseClick()

    def selectTitle(self) -> bool:
        if self.isSelectTitle:
            self.isSelectTitle = False
            return True
        return False

    def activeTitle(self, title3dArray, gameState):
        return self.pickingTitle

    def mouseHover(self):
        x, y = pygame.mouse.get_pos()
        y = cfg.displaySize[1] - y # This is to match OpenGL and pygame up
        r,g,b = glReadPixels(x, y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
        pixelColor = (r, g, b)

        i = 0
        n = cfg.nTitles
        colorIndex = 0
        for i in range(0, n):
            for j in range(0, n):
                for k in range(0, n):
                    color = cfg.titlesColor[colorIndex]
                    if pixelColor[0] == color[0] and pixelColor[1] == color[1] and pixelColor[2] == color[2]:
                        self.pickingTitle = [i, j, k]
                        break
                    colorIndex += 1
                else: continue
                break
            else: continue
            break
        else:
            self.pickingTitle = None

    def mouseClick(self):
        self.isSelectTitle = True

class MinMaxController(Controller):
    def __init__(self, maxDepthSearch = cfg.maxDepthSearch, depthWeight = cfg.depthWeight, heuristicWeigh = cfg.heuristicWeigh, evaluationScore = cfg.minmaxEvaluationScore):
        GameObject.__init__(self)
        self.isSelectTitle = False
        self.timeTaken = 0.0

        self.maxDepth = maxDepthSearch
        self.depthWeigh = depthWeight
        self.heuristicWeigh = heuristicWeigh
        self.evaluationScore = evaluationScore

    def activeTitle(self, title3dArray, gameState):
        if self.isSelectTitle:
            self.timeTaken = 0.0

        bestMove = None
        bestEvaluation = -math.inf
        n = cfg.nTitles
        from Game import GameState

        playerTitleState = oponentTitleState = Title.State.default
        if gameState == gameState.player1:
            playerTitleState = Title.State.player1
            oponentTitleState = Title.State.player2
        else:
            playerTitleState = Title.State.player2
            oponentTitleState = Title.State.player1

        # Traverse through all possible move
        for p in range(0, n):
            for r in range(0, n):
                for c in range(0, n):
                    title = title3dArray[p][r][c]
                    if  title.state != Title.State.default:
                        continue

                    preserveState = copy.copy(title.state)
                    title.state = playerTitleState
                    moveEvaluation = MinMax(title3dArray, (p, r, c),
                                            minTitleState=oponentTitleState,
                                            maxTitleState=playerTitleState,
                                            isMax=False)
                    title.state = preserveState

                    if moveEvaluation > bestEvaluation:
                        bestEvaluation = moveEvaluation
                        bestMove = (p, r, c)

        return bestMove

    def selectTitle(self) -> bool:
        if self.isSelectTitle:
            self.isSelectTitle = False
            return True
        return False

    def update(self, deltaTime: float):
        Controller.update(self, deltaTime)
        self.timeTaken += deltaTime

        if self.timeTaken > 1.5:
            self.timeTaken = 0.0
            self.isSelectTitle = True
