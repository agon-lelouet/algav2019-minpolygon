import numpy as np

class coordinates:
    def __init__(self, xCoord, yCoord):
        self.coordArray = np.array([xCoord, yCoord], dtype=float)

    def getX(self) -> float:
        return self.coordArray[0]

    def getY(self) -> float:
        return self.coordArray[1]

    def setX(self, xCoord):
        self.coordArray[0] = xCoord

    def setY(self, yCoord):
        self.coordArray[1] = yCoord
    
    def tofloatstring(self):
        return "{0} {1} \n".format(self.getX(), self.getY())

    def tointstring(self):
        return "{0} {1} \n".format(int(self.getX()), int(self.getY()))

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
        """
        sets the norm of this vector to one, done at object initialization, required for proper 
        computing of angle between two vectors
        """
        norm = self.getNorm()
        normedX = self.direction.getX() / norm
        normedY = self.direction.getY() / norm
        self.direction.setX(normedX)
        self.direction.setY(normedY)
        self.norm = self.getNorm()

    def rotateVector(self, theta: float):
        """
        rotates the vector of the specified angle (in radii, still)
        """
        coordMatrix = np.reshape(self.direction.coordArray, (2, 1))
        rotationmatrix = np.array([ [ np.cos(theta), -np.sin(theta) ], [ np.sin(theta), np.cos(theta) ] ], dtype=float)
        self.direction.coordArray = np.dot(rotationmatrix, coordMatrix)

def angleBetweenVectors(u: vector, v: vector) -> float:
    """
    calculates (in radii) the angle between two vector objects
    """
    scalarProduct = np.dot(u.direction.coordArray, v.direction.coordArray)
    return np.arccos(scalarProduct)

