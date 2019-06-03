import numpy as np


class Mask:
    hexagon = np.array(
        [[0, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 0],
         [1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1],
         [0, 0, 1, 1, 1, 1, 1, 0, 0],
         [0, 0, 0, 0, 1, 0, 0, 0, 0],
         ]
    )
    random=np.where(np.random.rand(9,9)<=0.9,1,0)

    def __init__(self):
        pass
