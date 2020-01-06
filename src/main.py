from Data import Dataset, download, getrandomfile
from Geometry import Shape
from Algorithms import GrahamAlgorithm, TriPixelAlgorithm, ToussaintAlgorithm
import numpy as np
import matplotlib.pyplot as plt

download()

filename = getrandomfile()

allPointsSet = Dataset()

allPointsSet.from_file(filename)

tripixelSet = TriPixelAlgorithm(filename)


convexhull = Shape(GrahamAlgorithm().pointslist)

minrectangle = ToussaintAlgorithm(convexhull)

dataScatter = (allPointsSet, tripixelSet, convexhull, minrectangle)
colors = ("red", "green", "blue", "yellow")
labels = ("allpoints", "tripixel", "convexhull", "minrectangle")

# Create plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

for data, color, label in zip(dataScatter, colors, labels):
    data.draw(ax, color, label)

ax.plot([ 150, 150 ], [ 200, 200 ])
plt.title('ALGAV 2019')
plt.legend(loc=2)

plt.show()