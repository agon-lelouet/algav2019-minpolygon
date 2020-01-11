from Data import Dataset, download, getrandomfile
from Geometry import Shape, point
from Algorithms import AggregateFiles, GrahamAlgorithm, TriPixelAlgorithm, ToussaintAlgorithm, RitterAlgorithm, CONCATFILE
from os import walk, path
import numpy as np
import matplotlib.pyplot as plt
from random import randint

def runpipeline(index: int) -> tuple:

    AggregateFiles((index+1))

    (tripixelSet, tripixeltime) = TriPixelAlgorithm(CONCATFILE)

    (convexhull, hulltime) = GrahamAlgorithm()

    (minrectangle, rectangletime) = ToussaintAlgorithm(convexhull)

    (boundingcircle, circletime) = RitterAlgorithm()

    return (tripixeltime, convexhull, hulltime, minrectangle, rectangletime, boundingcircle, circletime)

def computequality(shape, hull: Shape):
    return (shape.area() - hull.area()) / hull.area()

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
        print(index)
        (tripixeltime, hull, hulltime, rectangle, rectangletime, circle, circletime) = runpipeline(index)

        tripixeltimetoscale = tripixeltime * (10 ** 4)
        hulltimetoscale = hulltime * (10 ** 4)
        circletimetoscale = circletime * (10 ** 4)

        toussainttime = tripixeltimetoscale + hulltimetoscale + rectangletime
        rittertime = tripixeltimetoscale + circletimetoscale

        toussaintresults[index] = point(index, computequality(rectangle, hull))
        ritterresults[index] = point(index, computequality(circle, hull))
        toussainttimes[index] = point(index, toussainttime)
        rittertimes[index] = point(index, rittertime)

    datasets = (Dataset(toussaintresults), Dataset(ritterresults), Dataset(toussainttimes), Dataset(rittertimes))
    colors = ("red", "blue", "red", "blue", "black")
    labels = ("toussaint", "ritter", "toussaint_times", "ritter_times", "hull_times")
    plots = (efficacity, efficacity, time, time, time)

    for dataset, color, label, plot in zip(datasets, colors, labels, plots):
        dataset.draw(plot, color, label, withlines=True)

    plt.legend(loc=2)

    plt.show()

main()
