class Square():
    def verticies(origin = [[0], [0], [0]]):
        vertx =  [
            [1, 1, 0],
            [-1, 1, 0],
            [-1, -1, 0],
            [1, -1, 0]
        ]

        for v in vertx:
            v  += origin

        return vertx

    def edges:
        return (
            (0, 1), (1, 2), (2, 3), (3, 0)
        )

    def surfaces:
        return (
            (0, 1, 2, 3)
        )