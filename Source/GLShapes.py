import numpy as np

class GLShape():
    def __init__(self, vertices, edges, surfaces, colors):
        if colors is None:
            colors = [[128] * 3] * len(surfaces)

        self.vertices = vertices
        self.edges = edges
        self.surfaces = surfaces
        self.colors = colors # Surfaces color


class Cube(GLShape):
    vertices = np.array([
        [1, 1, 1],
        [-1, 1, 1],
        [-1, 1, -1],
        [1, 1, -1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, -1, -1],
        [1, -1, -1],
    ])
    edges = np.array([
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ])
    surfaces = np.array([
        (0, 3, 2, 1),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7)
    ])
    def __init__(self, surfaceColor = None):

        GLShape.__init__(self, Cube.vertices, Cube.edges, Cube.surfaces, surfaceColor)

class PlusShape(GLShape):
    edges = np.array([
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 0),
        (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23),
        (23, 12),
        (0, 12), (1, 13), (2, 14), (3, 15), (4, 16), (5, 17), (6, 18), (7, 19), (8, 20), (9, 21), (10, 22), (11, 23)
    ])
    surfaces = np.array([
        (0, 9, 6, 3), (0, 3, 2, 1), (3, 6, 5, 4), (6, 9, 8, 7), (9, 0, 11, 10),
        (12, 21, 18, 15), (12, 15, 14, 13), (15, 18, 17, 16), (18, 21, 20, 19), (21, 12, 23, 22),
        (0, 1, 13, 12), (1, 2, 14, 13), (2, 3, 15, 14), (3, 4, 16, 15), (4, 5, 17, 16),
        (5, 6, 18, 17), (6, 7, 19, 18), (7, 8, 20, 19), (8, 9, 21, 20), (9, 10, 22, 21),
        (10, 11, 23, 22), (11, 0, 12, 23)
    ])
    def __init__(self, surfaceColor = None, lengthProportion = 0.2):
        vertices = np.array([
            [lengthProportion, -1, lengthProportion],
            [lengthProportion, -1, 1],
            [-lengthProportion, -1, 1],
            [-lengthProportion, -1, lengthProportion],
            [-1, -1, lengthProportion],
            [-1, -1, -lengthProportion],
            [-lengthProportion, -1, -lengthProportion],
            [-lengthProportion, -1, -1],
            [lengthProportion, -1, -1],
            [lengthProportion, -1, -lengthProportion],
            [1, -1, -lengthProportion],
            [1, -1, lengthProportion],

            [lengthProportion, 1, lengthProportion],
            [lengthProportion, 1, 1],
            [-lengthProportion, 1, 1],
            [-lengthProportion, 1, lengthProportion],
            [-1, 1, lengthProportion],
            [-1, 1, -lengthProportion],
            [-lengthProportion, 1, -lengthProportion],
            [-lengthProportion, 1, -1],
            [lengthProportion, 1, -1],
            [lengthProportion, 1, -lengthProportion],
            [1, 1, -lengthProportion],
            [1, 1, lengthProportion]
        ])

        GLShape.__init__(self, vertices, PlusShape.edges, PlusShape.surfaces, surfaceColor)

class OShape(GLShape):
    def __init__(self, surfaceColor = None):
        pass
