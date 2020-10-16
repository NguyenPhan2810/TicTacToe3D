from GameObject import *
import pygame
from PlayGround import *
import configuration as cfg
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
        self.activePlane = self.activeRow = self.activeCol = 1

    def event(self, pygameEvents):
        Controller.event(self, pygameEvents)

        n = cfg.nTitles
        for event in pygameEvents:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f: self.isSelectTitle = True
                elif event.key == pygame.K_a: self.activeRow = max(0, self.activeRow - 1)
                elif event.key == pygame.K_d: self.activeRow = min(n - 1, self.activeRow + 1)
                elif event.key == pygame.K_w: self.activeCol = max(0, self.activeCol - 1)
                elif event.key == pygame.K_s: self.activeCol = min(n - 1, self.activeCol + 1)
                elif event.key == pygame.K_SPACE: self.activePlane = min(n - 1, self.activePlane + 1)
                elif event.key == pygame.K_LCTRL: self.activePlane = max(0, self.activePlane - 1)

    def update(self, deltaTime: float):
        Controller.update(self, deltaTime)

    def selectTitle(self) -> bool:
        if self.isSelectTitle:
            self.isSelectTitle = False
            return True
        return False

    def activeTitle(self, title3dArray, gameState):
        return (self.activePlane, self.activeRow, self.activeCol)

class MinMaxController(Controller):
    def __init__(self):
        GameObject.__init__(self)

    def activeTitle(self, title3dArray, gameState):
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
                    moveEvaluation = MinMax(title3dArray, (p, r, c), oponentTitleState, playerTitleState)
                    title.state = preserveState

                    if moveEvaluation > bestEvaluation:
                        bestEvaluation = moveEvaluation
                        bestMove = (p, r, c)

        return bestMove

    def selectTitle(self) -> bool:
        return True