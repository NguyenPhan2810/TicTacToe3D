from  gameObject import *
import GLShapes
class PlayGround(GameObject):
    def __init__(self):
        verticies =

        edges = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (8, 9),
            (9, 10),
            (10, 11),
            (11, 8)
        )

        surfaces = (
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (8, 9, 10, 11)
        )

        surfacesColor = (
            (0.6, 0.1, 0.2),
            (0.2, 0.7, 0.4),
            (0.8, 0.2, 0.6)
        )

        GameObject.__init__(self, GLObjectData(verticies, edges, surfaces, surfacesColor))
