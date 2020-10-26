import PlayGround
import configuration as cfg
import copy
import math

# Reference: https://www3.ntu.edu.sg/home/ehchua/programming/java/JavaGame_TicTacToe_AI.html#:~:text=In%20Tic%2DTac%2DToe%2C,two%20empty%20cells)%20for%20computer.
def Heuristic(title3dArray, scoreState):
    score = 0
    weigh = cfg.heuristicWeigh
    priorityWeigh = cfg.heuristicPriorityWeigh
    arr = title3dArray
    n = cfg.nTitles

    # Check plane
    for r in range(0, n):
        for c in range(0, n):
            maxCount = noneCount = 0
            for p in range(0, n):
                if arr[p][r][c].state == scoreState: maxCount += 1
                elif arr[p][r][c].state == PlayGround.Title.State.default: noneCount += 1
            if maxCount + noneCount == n:
                if noneCount < 2: score += priorityWeigh
                else: score += weigh * maxCount

    # Check row
    for p in range(0, n):
        for c in range(0, n):
            maxCount = noneCount = 0
            for r in range(0, n):
                if arr[p][r][c].state == scoreState: maxCount += 1
                elif arr[p][r][c].state == PlayGround.Title.State.default: noneCount += 1
            if maxCount + noneCount == n:
                if noneCount < 2: score += priorityWeigh
                else: score += weigh * maxCount

    # Check col
    for p in range(0, n):
        for r in range(0, n):
            maxCount = noneCount = 0
            for c in range(0, n):
                if arr[p][r][c].state == scoreState: maxCount += 1
                elif arr[p][r][c].state == PlayGround.Title.State.default: noneCount += 1
            if maxCount + noneCount == n:
                if noneCount < 2: score += priorityWeigh
                else: score += weigh * maxCount

    # Check diagonal
    for p in range(0, n):
        maxCount = noneCount = 0
        for i in range(0, n):
            if arr[p][i][i].state == scoreState: maxCount += 1
            elif arr[p][i][i].state == PlayGround.Title.State.default: noneCount += 1
        if maxCount + noneCount == n:
            if noneCount < 2: score += priorityWeigh
            else: score += weigh * maxCount

    # Check anti-diagonal
    for p in range(0, n):
        maxCount = noneCount = 0
        for i in range(0, n):
            if arr[p][i][n - 1 - i].state == scoreState: maxCount += 1
            elif arr[p][i][n - 1 - i].state == PlayGround.Title.State.default: noneCount += 1
        if maxCount + noneCount == n:
            if noneCount < 2: score += priorityWeigh
            else: score += weigh * maxCount

    # Check multiplane row
    for c in range(0, n):
        maxCount = noneCount = 0
        for i in range(0, n):
            if arr[i][i][c].state == scoreState: maxCount += 1
            elif arr[i][i][c].state == PlayGround.Title.State.default: noneCount += 1
        if maxCount + noneCount == n:
            if noneCount < 2: score += priorityWeigh
            else: score += weigh * maxCount

    # Check multiplane anti-row
    for c in range(0, n):
        maxCount = noneCount = 0
        for i in range(0, n):
            if arr[n - 1 - i][i][c].state == scoreState: maxCount += 1
            elif arr[n - 1 - i][i][c].state == PlayGround.Title.State.default: noneCount += 1
        if maxCount + noneCount == n:
            if noneCount < 2: score += priorityWeigh
            else: score += weigh * maxCount

    # Check multiplane col
    for r in range(0, n):
        maxCount = noneCount = 0
        for i in range(0, n):
            if arr[i][r][i].state == scoreState: maxCount += 1
            elif arr[i][r][i].state == PlayGround.Title.State.default: noneCount += 1
        if maxCount + noneCount == n:
            if noneCount < 2: score += priorityWeigh
            else: score += weigh * maxCount

    # Check multiplane anti-col
    for r in range(0, n):
        maxCount = noneCount = 0
        for i in range(0, n):
            if arr[n - 1 - i][r][i].state == scoreState: maxCount += 1
            elif arr[n - 1 - i][r][i].state == PlayGround.Title.State.default: noneCount += 1
        if maxCount + noneCount == n:
            if noneCount < 2: score += priorityWeigh
            else: score += weigh * maxCount

    # Check multiplane diagonal
    maxCount = noneCount = 0
    for i in range(0, n):
        if arr[i][i][i].state == scoreState: maxCount += 1
        elif arr[i][i][i].state == PlayGround.Title.State.default: noneCount += 1
    if maxCount + noneCount == n:
        if noneCount < 2: score += priorityWeigh
        else: score += weigh * maxCount

    maxCount = noneCount = 0
    for i in range(0, n):
        if arr[n - 1 - i][i][i].state == scoreState: maxCount += 1
        elif arr[n - 1 - i][i][i].state == PlayGround.Title.State.default: noneCount += 1
    if maxCount + noneCount == n:
        if noneCount < 2: score += priorityWeigh
        else: score += weigh * maxCount

    # Check multiplane anti-diagonal
    maxCount = noneCount = 0
    for i in range(0, n):
        if arr[i][i][n - 1 - i].state == scoreState: maxCount += 1
        elif arr[i][i][n - 1 - i].state == PlayGround.Title.State.default: noneCount += 1
        if maxCount + noneCount == n:
            if noneCount < 2: score += priorityWeigh
            else: score += weigh * maxCount

    maxCount = noneCount = 0
    for i in range(0, n):
        if arr[n - 1 - i][i][n - 1 - i].state == scoreState: maxCount += 1
        elif arr[n - 1 - i][i][n - 1 - i].state == PlayGround.Title.State.default: noneCount += 1
    if maxCount + noneCount == n:
        if noneCount < 2: score += priorityWeigh
        else: score += weigh * maxCount

    return score


# Reference https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/
# Reference https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
# Optimization technique used: Alpha-beta pruning, max depth restriction, heuristic function
def MinMax(title3dArray, newestMove, minTitleState, maxTitleState, depth = 0, isMax = False, alpha = -math.inf, beta = math.inf,
           maxDepth = cfg.maxDepthSearch, depthWeigh = cfg.depthWeight, heuristicWeigh = cfg.heuristicWeigh):
    # Evaluation
    if PlayGround.terminalCheck(title3dArray, newestMove) is not None: # Somebody won
        return (cfg.minmaxEvaluationScore - depth * depthWeigh) * (-1 if isMax else 1)

    if depth >= maxDepth:
        return Heuristic(title3dArray, maxTitleState) - Heuristic(title3dArray, minTitleState)

    score = 0
    n = cfg.nTitles
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
                    if beta <= alpha and cfg.alphabetaPruning:
                        break
                else: continue
                break
            else: continue
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
                    if beta <= alpha and cfg.alphabetaPruning:
                        break
                else: continue
                break
            else: continue
            break
        score += best

    return score if movecount > 0 else 0