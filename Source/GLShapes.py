import numpy as np
import copy
import math
import configuration as cfg

class GLShape():
    # Params:
    # colors receive 1d array has 3 value RGB for 1 color only
    def __init__(self, vertices, edges, surfaces, color):
        self.vertices = np.array(vertices)
        self.edges = np.array(edges)
        self.surfaces = np.array(surfaces)

        if color is None:
            color = [[128] * 3]
        self.surfaceColors = None # Surfaces color
        self.setColor(color)

    def setColor(self, color):
        self.surfaceColors = np.array([copy.deepcopy(color) for i in range(len(self.surfaces))])

class Cube(GLShape):
    vertices = [
        [1, 1, 1],
        [-1, 1, 1],
        [-1, 1, -1],
        [1, 1, -1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, -1, -1],
        [1, -1, -1],
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    surfaces = [
        (0, 3, 2, 1),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7)
    ]
    def __init__(self, surfaceColor = None):

        GLShape.__init__(self, Cube.vertices, Cube.edges, Cube.surfaces, surfaceColor)

class XShape(GLShape):
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 0),
        (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23),
        (23, 12),
        (0, 12), (1, 13), (2, 14), (3, 15), (4, 16), (5, 17), (6, 18), (7, 19), (8, 20), (9, 21), (10, 22), (11, 23)]
    surfaces = [
        (0, 9, 6, 3), (0, 3, 2, 1), (3, 6, 5, 4), (6, 9, 8, 7), (9, 0, 11, 10),
        (12, 21, 18, 15), (12, 15, 14, 13), (15, 18, 17, 16), (18, 21, 20, 19), (21, 12, 23, 22),
        (0, 1, 13, 12), (1, 2, 14, 13), (2, 3, 15, 14), (3, 4, 16, 15), (4, 5, 17, 16),
        (5, 6, 18, 17), (6, 7, 19, 18), (7, 8, 20, 19), (8, 9, 21, 20), (9, 10, 22, 21),
        (10, 11, 23, 22), (11, 0, 12, 23)
    ]
    def __init__(self, surfaceColor = None, thickness = cfg.titleXThickness):
        vertices = [
            [thickness, -1, thickness],
            [thickness, -1, 1],
            [-thickness, -1, 1],
            [-thickness, -1, thickness],
            [-1, -1, thickness],
            [-1, -1, -thickness],
            [-thickness, -1, -thickness],
            [-thickness, -1, -1],
            [thickness, -1, -1],
            [thickness, -1, -thickness],
            [1, -1, -thickness],
            [1, -1, thickness],

            [thickness, 1, thickness],
            [thickness, 1, 1],
            [-thickness, 1, 1],
            [-thickness, 1, thickness],
            [-1, 1, thickness],
            [-1, 1, -thickness],
            [-thickness, 1, -thickness],
            [-thickness, 1, -1],
            [thickness, 1, -1],
            [thickness, 1, -thickness],
            [1, 1, -thickness],
            [1, 1, thickness]
        ]

        cos45 = math.cos(math.radians(45))
        sin45 = math.sin(math.radians(45))
        for vertex in vertices:
            x = vertex[0]
            z = vertex[2]
            vertex[0] = x * cos45 - z * sin45
            vertex[2] = x * sin45 + z * cos45

        GLShape.__init__(self, vertices, XShape.edges, XShape.surfaces, surfaceColor)

class OShape(GLShape):
    def __init__(self, surfaceColor=None, nSegments=cfg.titleOSegments, thickness = cfg.titleOThickness):
        vertices = []
        vertices += self.generateCircleVertices(nSegments, 1, 1 - thickness)
        vertices += self.generateCircleVertices(nSegments, 1, 1)
        vertices += self.generateCircleVertices(nSegments, -1, 1)
        vertices += self.generateCircleVertices(nSegments, -1, 1 - thickness)

        edges = []
        for ring in range(0, 4):
            edges += [[i, i + 1] for i in range(nSegments * ring, nSegments * (ring + 1) - 1)]
            edges += [[nSegments * (ring + 1) - 1, nSegments * ring]]
        for segment in range(nSegments):
            edges += [[nSegments * i + segment, nSegments * (i + 1) + segment] for i in range(3)]
            edges += [[nSegments * 3 + segment, segment]]


        surfaces = []
        for segment in range(nSegments):
            vIndex = [segment + nSegments * i for i in range(4)]
            if vIndex[0] < nSegments - 1:
                surfaces += [[vIndex[i], vIndex[i] + 1, vIndex[i + 1] + 1, vIndex[i + 1]] for i in range(3)]
                surfaces += [[vIndex[3], vIndex[3] + 1, vIndex[0] + 1, vIndex[0]]]
            else:
                surfaces += [
                    [vIndex[0], 0, nSegments, vIndex[1]],
                    [vIndex[1], nSegments, 2 * nSegments, vIndex[2]],
                    [vIndex[2], 2 * nSegments, 3 * nSegments, vIndex[3]],
                    [vIndex[3], 3 * nSegments, 0, vIndex[0]]
                ]


        super().__init__(vertices, edges, surfaces, surfaceColor)


    def generateCircleVertices(self, nSegments, y, radius):
        segments = []

        pi = math.pi
        r = radius

        dTheta = 2 * pi / nSegments
        lastTheta =  dTheta * (nSegments - 1)
        x_prev = r * math.sin(lastTheta)
        z_prev = r * math.cos(lastTheta)
        theta = 0.0
        for segment in range(nSegments):
            x = r * math.cos(theta)
            z = r * math.sin(theta)

            segments += [[x, y, z]]

            theta += dTheta
            x_prev = x
            z_prev = z

        return segments

