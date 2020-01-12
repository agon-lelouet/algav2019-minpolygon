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

    return (tripixelSet, tripixeltime, convexhull, hulltime, minrectangle, rectangletime, boundingcircle, circletime)

def computequality(shapearea, hullarea):
    return (shapearea - hullarea) / hullarea

def getrandomnumber(max: int):
    return randint(1, max)

def main():
    nb_iter = getrandomnumber(10)
    print(nb_iter)
    download()

    samplesdir = "samples/"
    i = 0

    fig = plt.figure()
    efficacity = fig.add_subplot(2, 2, 1)
    time = fig.add_subplot(2, 2, 2)

    # plot1 = fig.add_subplot(2,2,3)
    # plot2 = fig.add_subplot(2,2,4)
    # toplot = (randint(0, nb_iter), randint(0, nb_iter))
    # plots = (plot1, plot2)
    # toplotindex = 0

    toussaintresults = np.empty(nb_iter, dtype=object)
    ritterresults = np.empty(nb_iter, dtype=object) 
    toussainttimes = np.empty(nb_iter, dtype=object)
    rittertimes = np.empty(nb_iter, dtype=object)
    for index in range(0, nb_iter):
        (tripixelSet, tripixeltime, hull, hulltime, rectangle, rectangletime, circle, circletime) = runpipeline(index)

        rectanglearea = rectangle.area()
        hullarea = hull.area()
        circlearea = circle.area()

        tripixeltimetoscale = tripixeltime * (10 ** 4)
        hulltimetoscale = hulltime * (10 ** 4)
        circletimetoscale = circletime * (10 ** 4)

        toussainttime = tripixeltimetoscale + hulltimetoscale + rectangletime
        rittertime = tripixeltimetoscale + circletimetoscale

        toussaintresults[index] = point(index, computequality(rectanglearea, hullarea))
        ritterresults[index] = point(index, computequality(circlearea, hullarea))
        toussainttimes[index] = point(index, toussainttime)
        rittertimes[index] = point(index, rittertime)

        # if index in toplot:
        #     print("ici")
        #     hull.draw(plots[toplotindex], "black", "graham")
        #     rectangle.draw(plots[toplotindex], "red", "toussaint")
        #     circle.draw(plots[toplotindex], "blue", "ritter")
        #     toplotindex = toplotindex+1


    datasets = (Dataset(toussaintresults), Dataset(ritterresults), Dataset(toussainttimes), Dataset(rittertimes))
    colors = ("red", "blue", "red", "blue")
    labels = ("toussaint", "ritter", "toussaint_times", "ritter_times")
    plots = (efficacity, efficacity, time, time)

    for dataset, color, label, plot in zip(datasets, colors, labels, plots):
        dataset.draw(plot, color, label, withlines=True)

    efficacity.legend(loc=2)
    time.legend(loc=2)

    plt.show()

main()
