import numpy as np

class GLShape():
    verticies = []
    edges = []
    surfaces = []

class Square(GLShape):
    verticies = np.array([
            [1.0, 0.0, 1.0],
            [-1.0, 0.0, 1.0],
            [-1.0, 0.0, -1.0],
            [1.0, 0.0, -1.0]
        ])

    edges = np.array([
            (0, 1), (1, 2), (2, 3), (3, 0)
        ])

    surfaces = np.array([
            (0, 1, 2, 3)
        ])

class Cube(GLShape):
    verticies = np.array([
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
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7)
    ])

    def __init__(self):
        self.surfacesColor = []
