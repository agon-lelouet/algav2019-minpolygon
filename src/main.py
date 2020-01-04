import Geometry as geo
import math
import Dataset

Dataset.download()

u = geo.vector(geo.coordinates(1, 1), geo.coordinates(1, 0))

v = geo.vector(geo.coordinates(1, 1), geo.coordinates(0, 1)) 

theta = geo.angleBetweenVectors(u, v)

print("theta", math.degrees(theta))

v.rotateVector(math.radians(-45))

newTheta = geo.angleBetweenVectors(u, v)

print("newTheta", math.degrees(newTheta))

dataset = Dataset.getDataset(1)
print(len(dataset))
xList = Dataset.getXList(dataset)
yList = Dataset.getYList(dataset)
print(xList)
print(yList)