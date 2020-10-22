import pygame

# Playground
nTitles = 4
titleWiggleAmount = 0.02
titleWiggleFrequency = 20
titleScaleAmount = 0.02
titleScaleFrequency = 5
terminalTitleColorChangeFreq = 5
terminalTitleColorChangeAmount = 150
playGroundScale = [0.8, 1, 0.8]
mouseRotationSensitivity = 0.3
titlesPadding = 1

# Colors
titlesColor = [[124,128, 231]] * nTitles* nTitles\
              + [[190,128, 231]] * nTitles* nTitles\
              + [[128,128, 180]] * nTitles * nTitles\
              + [[121,113, 199]] * nTitles* nTitles\
              + [[234, 136, 219]] * nTitles* nTitles

j = 0
for i in range(0, len(titlesColor)):
    titlesColor[i] = [titlesColor[i][0], titlesColor[i][1] + j, titlesColor[i][2]]
    j += 1
    if j == nTitles * nTitles:
        j = 0

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
heuristicMaxWeigh = 1
heuristicMinWeigh = 2
heuristicWeigh = 5
maxDepthSearch  = 2
depthWeight = 10
minmaxEvaluationScore = 10000
alphabetaPrunning = True

# MinMaxController
timeProportionRandomMove = 0.5
waitingTime = 2
waitingRandomTimeInterval = 0.5

# Main menu
mainmenuTextColor = (255, 255, 255)
mainmenuTextColorHovered = (235, 124, 165)
mainmenuTextColorClicked = (255, 144, 205)