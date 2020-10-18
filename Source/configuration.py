titlesColor = [[124,128, 231]] * 9 + [[190,128, 231]] * 9 + [[128,128, 180]] * 9

for i in range(0, len(titlesColor)):
    titlesColor[i] = [titlesColor[i][0], titlesColor[i][1] + i, titlesColor[i][2]]
    i += 1

backgroundColor = (51, 51, 51)
activeTitleColor = (5, 2, 3)
player1Color = (0, 0, 0)
player2Color = (255, 255, 255)

nTitles = 3
titleWiggleAmount = 0.05
titleWiggleFrequency = 20
titlePositionOffset = -0.4
planeSpacingMultiplier = 2.4
playGroundScale = 0.3
heuristicMaxWeigh = 1.1
heuristicMinWeigh = 1

displaySize = (1000, 1000)
displayAspectRatio = displaySize[0] / displaySize[1]
FOV = 30
nearClippingPlane = 0.1
farClippingPlane = 50.0
cameraZOffset = -7
cameraXRotate = 22
timePerFrame = 1 / 120

# Min-Max alg
maxDepthSearch  = 1
depthWeight = 10
heuristicWeigh = 2
minmaxEvaluationScore = 10000

# MinMaxController
timeProportionRandomMove = 0.7