import Geometry as geo
import numpy as np
import linecache
from Data import Dataset, NB_FILES, ALL_FILES
from subprocess import Popen
from random import sample
import os
import time

CONCATFILE = "tempdata/concatfile"
TRIPIXELDATA = "tempdata/tripixeldata"
GRAHAMDATA = "tempdata/grahamdata"
RITTERDATA = "tempdata/ritterdata"
TIMEDATA = "tempdata/timedata"

def AggregateFiles(setsize: int):
    random_files = sample(ALL_FILES, setsize)
    seen = set()
    unique = not any(i in seen or seen.add(i) for i in random_files)
    command = "cat "
    for file in random_files:
        command+=file + " "
    command += " > " + CONCATFILE
    process = Popen(command, shell=True)
    process.wait()

def TriPixelAlgorithm(filename):
    commands = [
        "cat {0} | sort -S 80% --parallel=8 -n | uniq | executables/tripixel | tail -n -1 > {1}".format(CONCATFILE, TIMEDATA),
        "cat {0} | sort -S 80% --parallel=8 -n | uniq | executables/tripixel | head -n -1 | awk '{{print $2, $1}}' | sort -S 80% --parallel=8 -n | executables/tripixel | tail -n -1 >> {1}".format(CONCATFILE, TIMEDATA),
        "cat {0} | sort -S 80% --parallel=8 -n | uniq | executables/tripixel | head -n -1 | awk '{{print $2, $1}}' | sort -S 80% --parallel=8 -n | executables/tripixel | awk '{{print $2, $1}}' | head -n -1 > {1}".format(filename, TRIPIXELDATA)
    ]
    for command in commands:
        process = Popen(command, shell=True)
        (stdout, stderr) = process.communicate()

    linecache.clearcache()
    time1 = float(linecache.getline(TIMEDATA, 1))
    time2 = float(linecache.getline(TIMEDATA, 2))
    totaltime = time1 + time2
    tripixeldataset = Dataset(np.empty(1))
    tripixeldataset.from_file(TRIPIXELDATA, from_line=2)
    return ( tripixeldataset, totaltime)


def GrahamAlgorithm() -> Dataset:
    command = "cat {0} | executables/graham $(wc -l {0} | awk '{{print $1}}') > {1}".format(TRIPIXELDATA, GRAHAMDATA)
    process = Popen(command, shell=True)
    process.wait()
    linecache.clearcache()
    time = float(linecache.getline(GRAHAMDATA, 1))

    grahamdataset = Dataset(np.empty(1))
    grahamdataset.from_file(GRAHAMDATA, from_line=2)

    return (geo.Shape(grahamdataset.pointslist), time)

def RitterAlgorithm() -> geo.Circle:
    command = "cat {0} | executables/ritter $(wc -l {0} | awk '{{print $1}}') > {1}".format(TRIPIXELDATA, RITTERDATA)
    process = Popen(command, shell=True)
    process.wait()

    linecache.clearcache()
    time = float(linecache.getline(RITTERDATA, 2))
    circle = linecache.getline(RITTERDATA, 1)

    x, y, radius = tuple(circle.split(" "))

    rittercircle = geo.Circle(float(x), float(y), float(radius))
    
    return (rittercircle, time)

def ToussaintAlgorithm(convexHull: geo.Shape) -> geo.Shape:

    start = time.perf_counter_ns()

    iindex = 0
    jindex = 0
    kindex = 0
    lindex = 0

    for i, vector in enumerate(convexHull.vectors):
        if (vector.origin.getX() < convexHull.vectors[iindex].origin.getX()):
            iindex = i

        if (vector.origin.getY() < convexHull.vectors[jindex].origin.getY()):
            lindex = i
        
        if (vector.origin.getX() > convexHull.vectors[kindex].origin.getX()):
            kindex = i
        
        if (vector.origin.getY() > convexHull.vectors[lindex].origin.getY()):
            jindex = i

    iindex0 = iindex
    jindex0 = jindex
    kindex0 = kindex
    lindex0 = lindex

    support_i = geo.vector(convexHull.vectors[iindex].origin, geo.point(0,1))
    support_j = geo.vector(convexHull.vectors[jindex].origin, geo.point(1,0))
    support_k = geo.vector(convexHull.vectors[kindex].origin, geo.point(0,-1))
    support_l = geo.vector(convexHull.vectors[lindex].origin, geo.point(-1,0))

    hullscanned = False
    iStepped = False
    jStepped = False
    kStepped = False
    lStepped = False

    count = 0

    minrectangle = geo.computeshapefromvectors([ support_i, support_j, support_k, support_l ])
    areamin = float("inf")

    convexhulllen = len(convexHull.vectors)

    while not hullscanned:

        indexanglemin = 0
        anglemin = 0

        anglei = geo.angleBetweenVectors(support_i, convexHull.vectors[iindex])
        anglej = geo.angleBetweenVectors(support_j, convexHull.vectors[jindex])

        if(anglei < anglej):
            anglemin = -anglei
            indexanglemin = iindex
        else:
            anglemin = -anglej
            indexanglemin = jindex

        anglek = geo.angleBetweenVectors(support_k, convexHull.vectors[kindex])
        if(anglek < anglemin):
            anglemin = -anglek
            indexanglemin = kindex

        anglel = geo.angleBetweenVectors(support_l, convexHull.vectors[lindex])
        if(anglel < anglemin):
            anglemin = -anglel
            indexanglemin = lindex
    

        if indexanglemin == iindex:
            support_i = geo.vector(convexHull.vectors[iindex].origin, convexHull.vectors[iindex].direction)
            support_j = geo.vector(support_j.origin, support_i.normal().invert().direction)
            support_k = geo.vector(support_k.origin, support_i.invert().direction)
            support_l = geo.vector(support_l.origin, support_j.invert().direction)

            iindex = (iindex+1)%convexhulllen
            support_i.origin = convexHull.points[iindex]
            iStepped = True

        elif indexanglemin == jindex:
            support_j = geo.vector(convexHull.vectors[jindex].origin, convexHull.vectors[jindex].direction)
            support_k = geo.vector(support_k.origin, support_j.normal().invert().direction)
            support_l = geo.vector(support_l.origin, support_j.invert().direction)
            support_i = geo.vector(support_i.origin, support_k.invert().direction)

            jindex = (jindex+1)%convexhulllen
            support_j.origin = convexHull.points[jindex]
            jStepped = True

        elif indexanglemin == kindex:
            support_k = geo.vector(convexHull.vectors[kindex].origin, convexHull.vectors[kindex].direction)
            support_l = geo.vector(support_l.origin, support_k.normal().invert().direction)
            support_i = geo.vector(support_i.origin, support_k.invert().direction)
            support_j = geo.vector(support_j.origin, support_l.invert().direction)
            kindex = (kindex+1)%convexhulllen
            support_k.origin = convexHull.points[kindex]
            kStepped = True

        else:
            support_l = geo.vector(convexHull.vectors[lindex].orig, convexHull.vectors[lindex].direction)
            support_i = geo.vector(support_i.origin, support_l.normal().invert().direction)
            support_j = geo.vector(support_j.origin, support_l.invert().direction)
            support_k = geo.vector(support_k.origin, support_i.invert().direction)

            lindex = (lindex+1)%convexhulllen
            support_l.origin = convexHull.points[lindex]
            lStepped = True

        rectangle = geo.computeshapefromvectors([ support_i, support_j, support_k, support_l ])

        if rectangle.area() < areamin:
            minrectangle = geo.computeshapefromvectors([ support_i, support_j, support_k, support_l ])
            minarea = minrectangle.area()
        
        if (iStepped and iindex == iindex0 or jStepped and jindex == jindex0 or
            kStepped and kindex == kindex0 or lStepped and lindex == lindex0):
            count = count + 1

        hullscanned = (count >= 4)

    end = time.perf_counter_ns()

    total_time = (end - start) / (10 ** 9)
    return (minrectangle, total_time)