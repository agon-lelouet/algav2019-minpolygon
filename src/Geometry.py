import numpy as np
import matplotlib.pyplot as plt
from math import degrees

class point:
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
    
    def equals(self, other) -> bool:
        return self.getX() == other.getX() and self.getY() == other.getY()

class vector:
    def __init__(self, orig: point, direct: point):
        self.origin = orig
        self.direction = direct

    def getNorm(self) -> float:
        return np.linalg.norm(self.direction.coordArray)

    def normalise(self):
        """
        sets the norm of this vector to one
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
        result = np.dot(rotationmatrix, coordMatrix)
        result = result.flatten()
        self.direction.coordArray = result

    def normal(self):
        return vector(self.origin, point(-self.direction.getY(), self.direction.getX()))

    def invert(self):
        return self.normal().normal()

    
class Shape:
    def __init__(self, points: np.array):
        self.points = points
        pointslen = len(points)
        self.vectors = np.empty(pointslen, dtype=vector)
        for index, currentpoint in enumerate(points):
            nextPoint = points[(index+1)%pointslen]
            self.vectors[index] = vector(currentpoint, point(nextPoint.getX() - currentpoint.getX(), nextPoint.getY() - currentpoint.getY()))
    
    def area(self) -> float:
        area = 0.0
        for i in range(0, len(self.points)):
            j = (i+1)%len(self.points)
            area+=(self.points[i].getX() * self.points[j].getY())
            area-=(self.points[i].getY() * self.points[j].getX())
        return 0.5*abs(area)

    def areaAsRectangle(self) -> float:
        return self.vectors[0].getNorm() * self.vectors[1].getNorm()

    def draw(self, ax, color, label):
        i = 0
        vectorlistlen = len(self.vectors)
        for vector in self.vectors:
            originX = vector.origin.getX()
            originY = vector.origin.getY()
            ax.plot([ originX, originX + vector.direction.getX() ], [ originY, originY + vector.direction.getY() ], color=color)

class Circle:
    def __init__(self, centerX: float, centerY: float, radius: float):
        self.centerX = centerX
        self.centerY = centerY
        self.radius = radius
    
    def area(self):
        return np.pi * np.square(self.radius)

    def draw(self, ax, color, label):
        i = 0
        circle = plt.Circle((self.centerX, self.centerY), self.radius, color=color, fill=False)
        ax.add_artist(circle)

def angleBetweenVectors(u: vector, v: vector) -> float:
    """
    calculates (in radii) the angle between two vector objects
    """
    normproduct = u.getNorm() * v.getNorm()
    dotproduct = np.dot(u.direction.coordArray, v.direction.coordArray)
    return np.arccos(dotproduct / normproduct)

def get_intersect(aorig, adirect, borig, bdirect):
    if adirect.getX() == 0:
        bslope = bdirect.getY() / bdirect.getX()
        borigy = (borig.getY()) - (bslope * borig.getX())
        ycoord = (bslope*aorig.getX()) + borigy
        return (aorig.getX(), ycoord)
    if adirect.getY() == 0:
        if bdirect.getX() == 0:
            return (borig.getX(), aorig.getY())
        bslope = bdirect.getY() / bdirect.getX()
        borigy = (borig.getY()) - (bslope * borig.getX())
        xcoord = (aorig.getY() - borigy) /bslope
        return (xcoord, aorig.getY())

    if bdirect.getX() == 0:
        aslope = adirect.getY() / adirect.getX()
        aorigy = (aorig.getY()) - (aslope * aorig.getX())
        ycoord = (aslope*borig.getX()) + aorigy
        return (borig.getX(), ycoord)
    if bdirect.getY() == 0:
        if adirect.getX() == 0:
            return (aorig.getX(), borig.getY())
        aslope = adirect.getY() / adirect.getX()
        aorigy = (aorig.getY()) - (aslope * aorig.getX())
        xcoord = (borig.getY() - aorigy) /aslope
        return (xcoord, borig.getY())

    aslope = adirect.getY() / adirect.getX()
    aorigy = (aorig.getY()) - (aslope * aorig.getX())

    bslope = bdirect.getY() / bdirect.getX()
    borigy = (borig.getY()) - (bslope * borig.getX())

    xcoord = (borigy - aorigy) / (aslope - bslope)

    ycoord = (aslope*xcoord) + aorigy

    return (xcoord, ycoord)


def computeshapefromvectors(vectors: np.array) -> Shape:
    vectorslen = len(vectors)
    shape = np.empty(vectorslen, dtype=point)
    for index, vectorcur in enumerate(vectors):
        nextvec = vectors[(index+1)%vectorslen]
        aorig = vectorcur.origin
        adirect = vectorcur.direction
        borig = nextvec.origin
        bdirect = nextvec.direction
        x, y = get_intersect(aorig, adirect, borig, bdirect)
        shape[index] = point(x, y)
    
    for index, pointcur in enumerate(shape):
        pointnext = shape[(index+1)%4]
        xdirectNext= pointnext.getX() - pointcur.getX()
        ydirectNext= pointnext.getY() - pointcur.getY()
        pointnextnext = shape[(index+2)%4]
        xdirectNextNext= pointnextnext.getX() - pointnext.getX()
        ydirectNextNext= pointnextnext.getY() - pointnext.getY()
        #print("print", degrees(angleBetweenVectors(vector(pointcur, point(xdirectNext, ydirectNext)), vector(pointnext, point(xdirectNextNext, ydirectNextNext)))))
        # to assert that all angles are 90 deg
    return Shape(shape)



