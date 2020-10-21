import pygame

# Colors
titlesColor = [[124,128, 231]] * 9 + [[190,128, 231]] * 9 + [[128,128, 180]] * 9

for i in range(0, len(titlesColor)):
    titlesColor[i] = [titlesColor[i][0], titlesColor[i][1] + i, titlesColor[i][2]]
    i += 1

backgroundColor = (51, 51, 51)
activeTitleColor = (5, 2, 3)
player1Color = (0, 0, 0)
player2Color = (255, 255, 255)

# Playground
nTitles = 3
titleWiggleAmount = 0.05
titleWiggleFrequency = 20
terminalTitleColorChangeFreq = 5
terminalTitleColorChangeAmount = 80
titlePositionOffset = -0.4
planeSpacingMultiplier = 1.6
playGroundScale = 0.33
mouseRotationSensitivity = 0.3

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
heuristicMaxWeigh = 1.1
heuristicMinWeigh = 1
heuristicWeigh = 2
maxDepthSearch  = 2
depthWeight = 10
minmaxEvaluationScore = 10000
alphabetaPrunning = True

# MinMaxController
timeProportionRandomMove = 0.5
waitingTime = 2.0
waitingRandomTimeInterval = 0.5

# Main menu
mainmenuTextColor = (255, 255, 255)
mainmenuTextColorHovered = (235, 124, 165)
mainmenuTextColorClicked = (255, 144, 205)