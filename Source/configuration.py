import pygame

# Playground
nTitles = 4 # must be > 1

titleXThickness = 0.1
titleOThickness = 0.2
titleOSegments = 6

activeTitleColorPulseRate = 20
activeTitleColorPulseAmount = 100
selectedTitleScaleMultiplier = 1.5

terminalTitleColorChangeFreq = 5
terminalTitleColorChangeAmount = 70

playGroundZoomAmount = 1.2
playGroundMaxRotationX = 70
mouseRotationSensitivity = 0.3
titlesPadding = 2

# Display
displaySize = (800, 800)
displayAspectRatio = displaySize[0] / displaySize[1]
FOV = 30
nearClippingPlane = 0.1
farClippingPlane = 50.0
cameraZOffset = -7
cameraXRotate = 22
timePerFrame = 1 / 60

# Min-Max alg
heuristicWeigh = 5
heuristicPriorityWeigh = 100
maxDepthSearch  = 1
depthWeight = 1
minmaxEvaluationScore = 10000
alphabetaPruning = True

# MinMaxController
waitingTime = 3

# Main menu
mainmenuTextColor = (255, 255, 255)
mainmenuTextColorHovered = (235, 124, 165)
mainmenuTextColorClicked = (255, 144, 205)
guideScrollAmount = 40
guideImageFilename = "Resources/Images/guide.png"

# Colors
import random as rd
colorSpace = [
    [150, 220, 100],
    [110, 150, 100],
    [189, 179, 120],
    [128, 180, 140],
    [120, 190, 190],
    [120, 220, 180],
]
if nTitles > len(colorSpace):
    colorSpace *= nTitles // len(colorSpace)
planeColor = rd.sample(colorSpace, nTitles)

backgroundColor = (51, 51, 51)
activeTitleColor = (255, 255, 255)
inactiveTitleColor = (100, 100, 100)
player1Color = (255, 90, 90)
player2Color = (100, 90, 255)