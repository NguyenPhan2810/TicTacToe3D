import numpy as np

class Square():
    def data():
        return Square.verticies(), Square.edges(), Square.surfaces()

    def verticies():
        vertx =  [
            [1, 0, 1],
            [-1, 0, 1],
            [-1, 0, -1],
            [1, 0, -1]
        ]

        return vertx

    def edges():
        return  np.array([
            (0, 1), (1, 2), (2, 3), (3, 0)
        ])

    def surfaces():
        return np.array([
            [0, 1, 2, 3]
        ])