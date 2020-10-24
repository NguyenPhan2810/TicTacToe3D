import pygame

# Playground
nTitles = 4 # must be > 1

titleXThickness = 0.1
titleOThickness = 0.2
titleOSegments = 6

titleWiggleAmount = 0.00
titleWiggleFrequency = 4
titleScaleAmount = 0.02
titleScaleFrequency = 20
titleSelectedScaleMultiplier = 1.1

terminalTitleColorChangeFreq = 5
terminalTitleColorChangeAmount = 70

playGroundScale = [1, 1, 1]
mouseRotationSensitivity = 0.3
titlesPadding = 1

# Display
displaySize = (800, 800)
displayAspectRatio = displaySize[0] / displaySize[1]
FOV = 30
nearClippingPlane = 0.1
farClippingPlane = 50.0
cameraZOffset = -7
cameraXRotate = 22
timePerFrame = 1 / 24

# Min-Max alg
heuristicMaxWeigh = 1.1
heuristicMinWeigh = 1
heuristicWeigh = 50
heuristicPriorityWeigh = 500
maxDepthSearch  = 1
depthWeight = 1
minmaxEvaluationScore = 10000
alphabetaPrunning = True

# MinMaxController
timeProportionRandomMove = 0.8
waitingTime = 5
waitingRandomTimeInterval = 0.5

# Main menu
mainmenuTextColor = (255, 255, 255)
mainmenuTextColorHovered = (235, 124, 165)
mainmenuTextColorClicked = (255, 144, 205)



# Colors
import random as rd
colorSpace = [
    [120, 178, 210],
    [150, 220, 100],
    [110, 150, 100],
    [140, 210, 240],
    [210, 130, 190],
    [200, 200, 200],
]
if nTitles > len(colorSpace):
    colorSpace *= nTitles // len(colorSpace)
planeColor = rd.sample(colorSpace, nTitles)

backgroundColor = (51, 51, 51)
activeTitleColor = (5, 2, 3)
inactiveTitleColor = (100, 100, 100)
player1Color = (255, 90, 90)
player2Color = (100, 90, 255)