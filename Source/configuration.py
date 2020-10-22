import pygame

# Playground
nTitles = 4
titleWiggleAmount = 0.01
titleWiggleFrequency = 20
titleScaleAmount = 0.06
titleScaleFrequency = 5
terminalTitleColorChangeFreq = 5
terminalTitleColorChangeAmount = 150
planeSpacingMultiplier = 1.3
playGroundScale = 0.8
mouseRotationSensitivity = 0.3
titlesPadding = -0.3

# Colors
titlesColor = [[124,128, 231]] * nTitles* nTitles\
              + [[190,128, 231]] * nTitles* nTitles\
              + [[128,128, 180]] * nTitles * nTitles\
              + [[121,113, 199]] * nTitles* nTitles\
              + [[234, 136, 219]] * nTitles* nTitles

for i in range(0, len(titlesColor)):
    titlesColor[i] = [titlesColor[i][0], titlesColor[i][1] + i, titlesColor[i][2]]
    i += 1

backgroundColor = (51, 51, 51)
activeTitleColor = (5, 2, 3)
player1Color = (0, 0, 0)
player2Color = (255, 255, 255)

# Display
displaySize = (800, 800)
displayAspectRatio = displaySize[0] / displaySize[1]
FOV = 30
nearClippingPlane = 0.1
farClippingPlane = 50.0
cameraZOffset = -7
cameraXRotate = 22
timePerFrame = 1 / 120

# Min-Max alg
heuristicMaxWeigh = 1.2
heuristicMinWeigh = 1
heuristicWeigh = 2
maxDepthSearch  = 2
depthWeight = 10
minmaxEvaluationScore = 10000
alphabetaPrunning = True

# MinMaxController
timeProportionRandomMove = 0.5
waitingTime = 0
waitingRandomTimeInterval = 0.5

# Main menu
mainmenuTextColor = (255, 255, 255)
mainmenuTextColorHovered = (235, 124, 165)
mainmenuTextColorClicked = (255, 144, 205)