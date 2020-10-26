import pygame

# Playground
nTitles = 4 # must be > 1

titleXThickness = 0.1
titleOThickness = 0.2
titleOSegments = 6

activeTitleColorPulseRate = 20
activeTitleColorPulseAmount = 100
selectedTitleScaleMultiplier = 1.1

terminalTitleColorChangeFreq = 5
terminalTitleColorChangeAmount = 70

playGroundZoomAmount = 1.2
playGroundMaxRotationX = 70
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
timePerFrame = 1 / 30

# Min-Max alg
heuristicMaxWeigh = 1
heuristicMinWeigh = 1
heuristicWeigh = 5
heuristicPriorityWeigh = 100
maxDepthSearch  = 1
depthWeight = 1
minmaxEvaluationScore = 1000
alphabetaPruning = True

# MinMaxController
waitingTime = 4

# Main menu
mainmenuTextColor = (255, 255, 255)
mainmenuTextColorHovered = (235, 124, 165)
mainmenuTextColorClicked = (255, 144, 205)
guideScrollAmount = 40
guideImageFilename = "Resources/Images/guide.png"

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
activeTitleColor = (255, 255, 255)
inactiveTitleColor = (100, 100, 100)
player1Color = (255, 90, 90)
player2Color = (100, 90, 255)