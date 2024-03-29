from GameObject import *
import pygame
from PlayGround import *
import configuration as cfg
import numpy as np
import multiprocessing
import random as rd
from MinMaxAlgorithm import MinMax
import time

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

        self.title3dArray = None

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
                if event.button == 1:
                    self.isMouseMoved = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.isMouseUp = True
            elif event.type == pygame.MOUSEMOTION:
                self.isMouseMoved = True

    def update(self, deltaTime: float):
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
        self.title3dArray =  title3dArray
        return self.pickingTitle

    def mouseHover(self):
        if self.title3dArray is None:
            return

        n = cfg.nTitles
        colorIndex = 0
        for i in range(0, n):
            for j in range(0, n):
                for k in range(0, n):
                    if self.title3dArray[i][j][k].isPicked:
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
        self.isStartCalculating = False
        self.findBestMoveProcess = None
        self.bestMoveQueue = multiprocessing.Queue()
        self.calculatingMoveQueue = multiprocessing.Queue()
        self.availableTitle = None

        self.isSelectTitle = False
        self.timeTaken = 0.0
        self.maxTimeWait = cfg.waitingTime
        self.isCalculating = False

        self.maxDepth = maxDepthSearch
        self.depthWeigh = depthWeight
        self.heuristicWeigh = heuristicWeigh
        self.evaluationScore = evaluationScore

        self.bestMove = None
        self.calculatingMove = None

    def reset(self):
        Controller.reset(self)

        self.isStartCalculating = False
        if self.findBestMoveProcess is not None:
            self.findBestMoveProcess.terminate()
        self.findBestMoveProcess = None
        self.bestMoveQueue = multiprocessing.Queue()
        self.calculatingMoveQueue = multiprocessing.Queue()

        self.isSelectTitle = False
        self.timeTaken = 0.0
        self.isCalculating = False

        self.bestMove = None

    def destructor(self):
        if self.findBestMoveProcess is not None:
            self.findBestMoveProcess.terminate()

    def activeTitle(self, title3dArray, gameState):
        if self.findBestMoveProcess is None:
            if  self.bestMove is None:
                self.findBestMoveProcess = multiprocessing.Process(target=findBestMove,
                                                                   args=(title3dArray, gameState, self.maxDepth, self.depthWeigh, self.heuristicWeigh,
                                                                         self.bestMoveQueue, self.calculatingMoveQueue),
                                                                   daemon=True)
                self.findBestMoveProcess.start()
        elif not self.findBestMoveProcess.is_alive():
            self.bestMove = self.bestMoveQueue.get()
            self.findBestMoveProcess = None

        self.isCalculating = self.bestMove is None

        if not self.isStartCalculating and self.isCalculating and not self.isSelectTitle:
            self.isStartCalculating = True
            self.timeTaken = 0.0

        if self.isCalculating:
            try:
                calMove = self.calculatingMoveQueue.get_nowait()
                if calMove:
                    self.calculatingMove = calMove
                    return calMove
            except:
                return self.calculatingMove

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

    def update(self, deltaTime: float):
        super().update(deltaTime)

        self.timeTaken += deltaTime

        if self.timeTaken > self.maxTimeWait and not self.isSelectTitle and self.isStartCalculating:
            self.isSelectTitle = True

def findBestMove(title3dArray, gameState, maxDepth, depthWeigh, heuristicWeigh,
                 queue: multiprocessing.Queue,
                 calculatingQueue: multiprocessing.Queue):
    timeStart = time.time()

    availableTitle = []
    n = cfg.nTitles
    for p in range(0, n):
        for r in range(0, n):
            for c in range(0, n):
                if title3dArray[p][r][c].state == Title.State.default:
                    availableTitle += [[p, r, c]]

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
    for p, r, c in availableTitle:
        title = title3dArray[p][r][c]
        preserveState = copy.copy(title.state)
        title.state = playerTitleState
        moveEvaluation = MinMax(title3dArray, (p, r, c),
                                minTitleState=oponentTitleState,
                                maxTitleState=playerTitleState,
                                isMax=False,
                                maxDepth=maxDepth,
                                depthWeigh=depthWeigh,
                                heuristicWeigh=heuristicWeigh)
        title.state = preserveState

        if moveEvaluation > bestEvaluation:
            bestEvaluation = moveEvaluation
            bestMoves = [[p, r, c]]
            calculatingQueue.put([p, r, c])
        elif moveEvaluation == bestEvaluation:
            calculatingQueue.put([p, r, c])
            bestMoves += [[p, r, c]]

    queue.put(rd.choice(bestMoves))

    timeEnd = time.time()
    totalTime = (timeEnd - timeStart)
    print("Move calculated in ", totalTime, " seconds")