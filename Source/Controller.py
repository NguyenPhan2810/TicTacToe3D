from GameObject import *
import pygame
from PlayGround import *
import configuration as cfg
import numpy as np
import threading
import random as rd
from MinMaxAlgorithm import MinMax

class Controller(GameObject):
    def __init__(self):
        GameObject.__init__(self)

    def reset(self):
        GameObject.reset(self)

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
        Controller.reset(self)
        self.isSelectTitle = False
        self.isMouseMoved = False
        self.isMouseUp = False
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
                        print(i, j, k)
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
        self.isStartCalculating = False
        self.findBestMoveThread = None
        self.availableTitle = None

        self.isSelectTitle = False
        self.timeTaken = 0.0
        self.maxTimeWait = cfg.waitingTime
        self.isCalculating = False
        self.randomTimeWait = 0
        self.maxRandomTimeInterval = cfg.waitingRandomTimeInterval

        self.maxDepth = maxDepthSearch
        self.depthWeigh = depthWeight
        self.heuristicWeigh = heuristicWeigh
        self.evaluationScore = evaluationScore

        self.bestMove = None
        self.currentRandomMove = None

    def reset(self):
        Controller.reset(self)

        self.isStartCalculating = False
        self.findBestMoveThread = None
        self.availableTitle = None

        self.isSelectTitle = False
        self.timeTaken = 0.0
        self.isCalculating = False
        self.randomTimeWait = 0

        self.bestMove = None
        self.currentRandomMove = None


    def activeTitle(self, title3dArray, gameState):
        if self.availableTitle is None:
            self.prepareAvailableMove(title3dArray)

        if self.findBestMoveThread is None:
            self.findBestMoveThread = threading.Thread(target=self.findBestMove,
                                                       args=(title3dArray, gameState),
                                                       daemon=True)
            self.findBestMoveThread.start()
        elif not self.findBestMoveThread.is_alive():
            self.findBestMoveThread = None

        self.isCalculating = self.bestMove is None

        if not self.isStartCalculating and self.isCalculating and not self.isSelectTitle:
            self.isStartCalculating = True
            self.timeTaken = 0.0

        if self.timeTaken < self.maxTimeWait * cfg.timeProportionRandomMove or self.isCalculating:
            self.getRandomMove()
            return self.currentRandomMove

        return self.bestMove

    def selectTitle(self) -> bool:
        if self.isSelectTitle and not self.isCalculating:
            self.isSelectTitle = False
            self.bestMove = None
            self.isCalculating = False
            self.availableTitle = None
            self.timeTaken = 0.0
            self.isStartCalculating = False
            return True
        return False

    def findBestMove(self, title3dArray, gameState):
        if self.bestMove is not None:
            return

        bestEvaluation = -math.inf
        n = cfg.nTitles

        playerTitleState = oponentTitleState = Title.State.default
        if gameState == gameState.player1:
            playerTitleState = Title.State.player1
            oponentTitleState = Title.State.player2
        else:
            playerTitleState = Title.State.player2
            oponentTitleState = Title.State.player1

        # Traverse through all possible move
        bestMoves = []
        for p, r, c in self.availableTitle:
            title = title3dArray[p][r][c]
            preserveState = copy.copy(title.state)
            title.state = playerTitleState
            moveEvaluation = MinMax(title3dArray, (p, r, c),
                                    minTitleState=oponentTitleState,
                                    maxTitleState=playerTitleState,
                                    isMax=False,
                                    maxDepth=self.maxDepth,
                                    depthWeigh=self.depthWeigh,
                                    heuristicWeigh=self.heuristicWeigh)
            title.state = preserveState

            if moveEvaluation > bestEvaluation:
                bestEvaluation = moveEvaluation
                bestMoves = [[p, r, c]]
            elif moveEvaluation == bestEvaluation:
                bestMoves += [[p, r, c]]

        self.bestMove = rd.choice(bestMoves)

    def prepareAvailableMove(self, title3dArray):
        self.availableTitle = []
        n = cfg.nTitles
        for p in range(0, n):
            for r in range(0, n):
                for c in range(0, n):
                    title = title3dArray[p][r][c]
                    if title.state != Title.State.default:
                        continue

                    self.availableTitle += [[p, r, c]]

    def getRandomMove(self):
        if self.randomTimeWait < self.maxRandomTimeInterval:
            return self.currentRandomMove

        self.randomTimeWait = 0
        self.currentRandomMove = rd.choice(self.availableTitle)

    def update(self, deltaTime: float):
        Controller.update(self, deltaTime)

        self.timeTaken += deltaTime
        self.randomTimeWait += deltaTime

        if self.timeTaken > self.maxTimeWait and not self.isSelectTitle and self.isStartCalculating:
            self.isSelectTitle = True

