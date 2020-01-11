from Data import Dataset, download, getrandomfile, NB_FILES
from Geometry import Shape
from Algorithms import GrahamAlgorithm, TriPixelAlgorithm, ToussaintAlgorithm, RitterAlgorithm
from os import walk, path
import numpy as np
import matplotlib.pyplot as plt
from random import randint

def plotmelikeonofyourfrenchgirls():
    dataScatter = (allPointsSet, tripixelSet, convexhull, minrectangle)
    colors = ("red", "green", "blue", "yellow")
    labels = ("allpoints", "tripixel", "convexhull", "minrectangle")

    # Create plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for data, color, label in zip(dataScatter, colors, labels):
        data.draw(ax, color, label)

def runpipeline(path: str) -> list:

    allPointsSet = Dataset(path)

    tripixelSet = TriPixelAlgorithm(path)
    pointsnumber = len(tripixelSet.pointslist)

    (convexhull, hulltime) = GrahamAlgorithm()

    (boundingcircle, circletime) = RitterAlgorithm()

    (minrectangle, rectangletime) = ToussaintAlgorithm(convexhull)

    return (convexhull, hulltime, minrectangle, rectangletime, boundingcircle, circletime)

def computequality(shape: Shape, hull: Shape):
    return shape.area() / hull.area()

def getrandomnumber(max: int):
    return randint(1, max)

def main():

    nb_iter = getrandomnumber(50)
    download()

    samplesdir = "samples/"
    i = 0

    fig = plt.figure()
    efficacity = fig.add_subplot(2, 1, 1)
    time = fig.add_subplot(2, 1, 2)

    toussaintresults = np.zeros(nb_iter, dtype=float)
    ritterresults = np.zeros(nb_iter, dtype=float) 
    toussainttimes = np.zeros(nb_iter, dtype=float)
    rittertimes = np.zeros(nb_iter, dtype=float)
    hulltimes = np.zeros(nb_iter, dtype=float)

    for root, dirs, files in walk(samplesdir):
        for index, filename in enumerate(files):
            if (index == nb_iter):
                break
            print("runpipeline", path.join(samplesdir, filename), index)
            (hull, hulltime, rectangle, rectangletime, circle, circletime) = runpipeline(path.join(samplesdir, filename))
            toussaintresults[index] = computequality(rectangle, hull)
            ritterresults[index] = computequality(circle, hull)
            toussainttimes[index] = rectangletime
            rittertimes[index] = circletime
            hulltimes[index] = hulltime

    datasets = (toussaintresults, ritterresults, toussainttimes, rittertimes, hulltimes)
    colors = ("red", "blue", "red", "blue", "black")
    labels = ("toussaint", "ritter", "toussaint_times", "ritter_times", "hull_times")
    plots = (efficacity, efficacity, time, time, time)

    for dataset, color, label, plot in zip(datasets, colors, labels, plots):
        plot.scatter([ f for f in range(0, nb_iter) ], dataset, alpha=0.8, c=color, edgecolors='none', s=30, label=label)
        for index, point in enumerate(dataset):
            plot.plot([index, index + 1], [ point, dataset[index+1] ], color=color, ls="solid")
            if (index == nb_iter - 2):
                break

    # efficacity.scatter([ f for f in range(0, nb_iter) ], ritterresults, alpha=0.8, c="blue", edgecolors='none', s=30)
    # times.scatter([ f for f in range(0, nb_iter) ], toussainttimes, alpha=0.8, c="red", edgecolors='none', s=30)
    # times.scatter([ f for f in range(0, nb_iter) ], rittertimes, alpha=0.8, c="blue", edgecolors='none', s=30)
    # times.scatter([ f for f in range(0, nb_iter) ], rittertimes, alpha=0.8, c="blue", edgecolors='none', s=30)

    # for index, (toussaint, ritter, toussainttime, rittertime) in enumerate(zip(toussaintresults, ritterresults, toussainttimes, rittertimes)):

    #     efficacity.plot([index, index + 1], [ ritter, ritterresults[index+1] ], "b-")
    #     times.plot([index, index + 1], [ toussainttime, toussainttimes[index+1] ], "r-")
    #     times.plot([index, index + 1], [ rittertime, rittertimes[index+1] ], "b-")
    #     if (index == nb_iter - 2):
    #         break

    plt.legend(loc=2)

    plt.show()

main()
