import PlayGround
import configuration as cfg
import copy
import math

# Reference: https://www3.ntu.edu.sg/home/ehchua/programming/java/JavaGame_TicTacToe_AI.html#:~:text=In%20Tic%2DTac%2DToe%2C,two%20empty%20cells)%20for%20computer.
def Heuristic(title3dArray, minTitleState, maxTitleState):
    score = 0
    arr = title3dArray
    n = cfg.nTitles

    totalMaxCount = totalMinCount = totalNoneCount = 0

    # Check plane
    for r in range(0, n):
        for c in range(0, n):
            maxCount = minCount = noneCount = 0
            for p in range(0, n):
                if arr[p][r][c].state == maxTitleState: maxCount += 1
                elif arr[p][r][c].state == minTitleState: minCount += 1
                else: noneCount += 1
            totalMaxCount += maxCount * maxCount
            totalMinCount += minCount * minCount
            totalNoneCount += noneCount * noneCount

    # Check row
    for p in range(0, n):
        for c in range(0, n):
            maxCount = minCount = noneCount = 0
            for r in range(0, n):
                if arr[p][r][c].state == maxTitleState: maxCount += 1
                elif arr[p][r][c].state == minTitleState: minCount += 1
                else: noneCount += 1
            totalMaxCount += maxCount * maxCount
            totalMinCount += minCount * minCount
            totalNoneCount += noneCount * noneCount

    # Check col
    for p in range(0, n):
        for r in range(0, n):
            maxCount = minCount = noneCount = 0
            for c in range(0, n):
                if arr[p][r][c].state == maxTitleState: maxCount += 1
                elif arr[p][r][c].state == minTitleState: minCount += 1
                else: noneCount += 1
            totalMaxCount += maxCount * maxCount
            totalMinCount += minCount * minCount
            totalNoneCount += noneCount * noneCount

    # Check diagonal
    for p in range(0, n):
        maxCount = minCount = noneCount = 0
        for i in range(0, n):
            if arr[p][i][i].state == maxTitleState: maxCount += 1
            elif arr[p][i][i].state == minTitleState: minCount += 1
            else: noneCount += 1
        totalMaxCount += maxCount * maxCount
        totalMinCount += minCount * minCount
        totalNoneCount += noneCount * noneCount

    # Check anti-diagonal
    for p in range(0, n):
        maxCount = minCount = noneCount = 0
        for i in range(0, n):
            if arr[p][i][n - 1 - i].state == maxTitleState: maxCount += 1
            elif arr[p][i][n - 1 - i].state == minTitleState: minCount += 1
            else: noneCount += 1
        totalMaxCount += maxCount * maxCount
        totalMinCount += minCount * minCount
        totalNoneCount += noneCount * noneCount

    # Check multiplane row
    for c in range(0, n):
        maxCount = minCount = noneCount = 0
        for i in range(0, n):
            if arr[i][i][c].state == maxTitleState: maxCount += 1
            elif arr[i][i][c].state == minTitleState: minCount += 1
            else: noneCount += 1
        totalMaxCount += maxCount * maxCount
        totalMinCount += minCount * minCount
        totalNoneCount += noneCount * noneCount

    # Check multiplane anti-row
    for c in range(0, n):
        maxCount = minCount = noneCount = 0
        for i in range(0, n):
            if arr[n - 1 - i][i][c].state == maxTitleState: maxCount += 1
            elif arr[n - 1 - i][i][c].state == minTitleState: minCount += 1
            else: noneCount += 1
        totalMaxCount += maxCount * maxCount
        totalMinCount += minCount * minCount
        totalNoneCount += noneCount * noneCount

    # Check multiplane col
    for r in range(0, n):
        maxCount = minCount = noneCount = 0
        for i in range(0, n):
            if arr[i][r][i].state == maxTitleState: maxCount += 1
            elif arr[i][r][i].state == minTitleState: minCount += 1
            else: noneCount += 1
        totalMaxCount += maxCount * maxCount
        totalMinCount += minCount * minCount
        totalNoneCount += noneCount * noneCount

    # Check multiplane anti-col
    for r in range(0, n):
        maxCount = minCount = noneCount = 0
        for i in range(0, n):
            if arr[n - 1 - i][r][i].state == maxTitleState: maxCount += 1
            elif arr[n - 1 - i][r][i].state == minTitleState: minCount += 1
            else: noneCount += 1
        totalMaxCount += maxCount * maxCount
        totalMinCount += minCount * minCount
        totalNoneCount += noneCount * noneCount

    # Check multiplane diagonal
    maxCount = minCount = noneCount = 0
    for i in range(0, n):
        if arr[i][i][i].state == maxTitleState: maxCount += 1
        elif arr[i][i][i].state == minTitleState: minCount += 1
        else: noneCount += 1
    totalMaxCount += maxCount * maxCount
    totalMinCount += minCount * minCount
    totalNoneCount += noneCount * noneCount

    maxCount = minCount = noneCount = 0
    for i in range(0, n):
        if arr[n - 1 - i][i][i].state == maxTitleState: maxCount += 1
        elif arr[n - 1 - i][i][i].state == minTitleState: minCount += 1
        else: noneCount += 1
    totalMaxCount += maxCount * maxCount
    totalMinCount += minCount * minCount
    totalNoneCount += noneCount * noneCount

    # Check multiplane anti-diagonal
    maxCount = minCount = noneCount = 0
    for i in range(0, n):
        if arr[i][i][n - 1 - i].state == maxTitleState: maxCount += 1
        elif arr[i][i][n - 1 - i].state == minTitleState: minCount += 1
        else: noneCount += 1
    totalMaxCount += maxCount * maxCount
    totalMinCount += minCount * minCount
    totalNoneCount += noneCount * noneCount

    maxCount = minCount = noneCount = 0
    for i in range(0, n):
        if arr[n - 1 - i][i][n - 1 - i].state == maxTitleState: maxCount += 1
        elif arr[n - 1 - i][i][n - 1 - i].state == minTitleState: minCount += 1
        else: noneCount += 1
    totalMaxCount += maxCount * maxCount
    totalMinCount += minCount * minCount
    totalNoneCount += noneCount * noneCount

    # maxCount and minCount squared means the more titles in a row the weigher the score is
    # minus totalNoneCount means the less None Title the weigher the score is
    # 2 * totalMinCount because 2 minTitle in a row is the most dangerous
    score = (totalMaxCount * cfg.heuristicMaxWeigh + totalMinCount * cfg.heuristicMinWeigh - totalNoneCount)

    return score


# Reference https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/
# Reference https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
# Optimization technique used: Alpha-beta pruning, max depth restriction, heuristic function
def MinMax(title3dArray, newestMove, minTitleState, maxTitleState, depth = 0, isMax = False, alpha = -math.inf, beta = math.inf,
           maxDepth = cfg.maxDepthSearch, depthWeigh = cfg.depthWeight, heuristicWeigh = cfg.heuristicWeigh):
    score = 0
    n = cfg.nTitles

    # Evaluation
    if PlayGround.terminalCheck(title3dArray, newestMove) == True: # Somebody won
        score = cfg.minmaxEvaluationScore - depth * depthWeigh
        if title3dArray[newestMove[0]][newestMove[1]][newestMove[2]].state == maxTitleState:
            return  score
        else:
            return -score

    if depth >= maxDepth:
        return Heuristic(title3dArray, minTitleState, maxTitleState) * heuristicWeigh

    movecount = 0
    if isMax:
        best = -math.inf
        for p in range(0, n):
            for r in range(0, n):
                for c in range(0, n):
                    title = title3dArray[p][r][c]
                    if title.state != PlayGround.Title.State.default:
                        continue

                    # make a move
                    movecount += 1
                    preserveState = copy.copy(title.state)
                    title.state = maxTitleState

                    # recursively calculate evaluation and take the highest one
                    best = max(best, MinMax(title3dArray, (p, r, c), minTitleState, maxTitleState, depth + 1, not isMax, alpha, beta,
                                            maxDepth, depthWeigh, heuristicWeigh))
                    alpha = max(alpha, best)

                    # undo the move
                    title.state = preserveState

                    # Alpha beta pruning
                    if beta <= alpha:
                        break
        score += best
    else:
        best = math.inf
        for p in range(0, n):
            for r in range(0, n):
                for c in range(0, n):
                    title = title3dArray[p][r][c]
                    if title.state != PlayGround.Title.State.default:
                        continue

                    # make a move
                    movecount += 1
                    preserveState = copy.copy(title.state)
                    title.state = minTitleState

                    # recursively calculate evaluation and take the lowest one
                    best = min(best, MinMax(title3dArray, (p, r, c), minTitleState, maxTitleState, depth + 1, not isMax, alpha, beta,
                                            maxDepth, depthWeigh, heuristicWeigh))
                    beta = min(beta, best)

                    # undo the move
                    title.state = preserveState

                    # Alpha beta pruning
                    if beta <= alpha:
                        break
        score += best
    return score if movecount > 0 else 0