import Geometry as geo
import math
import numpy as np

u = geo.vector((1, 1), (1, 0))

v = geo.vector((1, 1), (0, 1)) 

theta = geo.angleBetweenVectors(u, v)

print("theta", math.degrees(theta))

v.rotateVector(math.radians(-45))

newTheta = geo.angleBetweenVectors(u, v)

print("newTheta", math.degrees(newTheta))