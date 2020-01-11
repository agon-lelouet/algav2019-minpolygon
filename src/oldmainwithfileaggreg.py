from Data import Dataset, download, getrandomfile
from Geometry import Shape, point
from Algorithms import AggregateFiles, GrahamAlgorithm, TriPixelAlgorithm, ToussaintAlgorithm, RitterAlgorithm, CONCATFILE
from os import walk, path
import numpy as np
import matplotlib.pyplot as plt
from random import randint

def runpipeline(index: int) -> tuple:

    AggregateFiles(index+1)

    tripixelSet = TriPixelAlgorithm()
    pointsnumber = len(tripixelSet.pointslist)

    (convexhull, hulltime) = GrahamAlgorithm()

    (boundingcircle, circletime) = RitterAlgorithm()

    (minrectangle, rectangletime) = ToussaintAlgorithm(convexhull)

    return (pointsnumber, convexhull, hulltime, minrectangle, rectangletime, boundingcircle, circletime)

def computequality(shape: Shape, hull: Shape):
    return shape.area() / hull.area()

def getrandomnumber(max: int):
    return randint(1, max)

def main():
    nb_iter = getrandomnumber(100)
    print(nb_iter)
    download()

    samplesdir = "samples/"
    i = 0

    fig = plt.figure()
    efficacity = fig.add_subplot(2, 1, 1)
    time = fig.add_subplot(2, 1, 2)

    toussaintresults = np.empty(nb_iter, dtype=object)
    ritterresults = np.empty(nb_iter, dtype=object) 
    toussainttimes = np.empty(nb_iter, dtype=object)
    rittertimes = np.empty(nb_iter, dtype=object)
    hulltimes = np.empty(nb_iter, dtype=object)

    for index in range(0, nb_iter):
        (pointsnumber, hull, hulltime, rectangle, rectangletime, circle, circletime) = runpipeline(index)
        print(pointsnumber, computequality(rectangle, hull), computequality(circle, hull), computequality(circle, hull))
        toussaintresults[index] = point(pointsnumber, computequality(rectangle, hull))
        ritterresults[index] = point(pointsnumber, computequality(circle, hull))
        toussainttimes[index] = point(pointsnumber, rectangletime)
        rittertimes[index] = point(pointsnumber, circletime * (10 ** 4))
        hulltimes[index] = point(pointsnumber, hulltime * (10 ** 4))

    datasets = (Dataset(toussaintresults), Dataset(ritterresults), Dataset(toussainttimes), Dataset(rittertimes), Dataset(hulltimes))
    colors = ("red", "blue", "red", "blue", "black")
    labels = ("toussaint", "ritter", "toussaint_times", "ritter_times", "hull_times")
    plots = (efficacity, efficacity, time, time, time)

    for dataset, color, label, plot in zip(datasets, colors, labels, plots):
        dataset.draw(plot, color, label, withlines=True)

    plt.legend(loc=2)

    plt.show()

main()
