import numpy as np

class coordinates:
    def __init__(self, xCoord, yCoord):
        self.coordArray = np.array([xCoord, yCoord], dtype=float)

    def getX(self) -> float:
        return self.coordArray[0]

    def getY(self) -> float:
        return self.coordArray[1]

    def setX(self, xCoord):
        print("xCoord", xCoord)
        self.coordArray[0] = xCoord

    def setY(self, yCoord):
        print("yCoord", yCoord)
        self.coordArray[1] = yCoord

class vector:
    def __init__(self, orig: coordinates, direct: coordinates):
        self.origin = orig
        self.direction = direct
        self.normalise()

    def getNorm(self) -> float:
        sqx = np.power(self.direction.getX(), 2)
        sqy = np.power(self.direction.getY(), 2)
        sum = sqx + sqy
        return np.sqrt(sum)

    def normalise(self):
        norm = self.getNorm()
        normedX = self.direction.getX() / norm
        normedY = self.direction.getY() / norm
        self.direction[0] = normedX
        self.direction[1] = normedY
        self.norm = self.getNorm()

    def rotateVector(self, theta: float):
        rotationmatrix = np.array([ [ np.cos(theta), -np.sin(theta) ], [ np.sin(theta), np.cos(theta) ] ], dtype=float)
        self.direction = np.dot(rotationmatrix, self.direction.reshape((2, 1)))

def angleBetweenVectors(u: vector, v: vector) -> float:
    scalarProduct = np.dot(u.direction, v.direction)
    return np.arccos(scalarProduct)

