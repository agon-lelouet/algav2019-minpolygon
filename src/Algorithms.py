import Geometry as geo
import numpy as np
import linecache
from Data import Dataset
from subprocess import Popen, PIPE, STDOUT
import os
import time

TRIPIXELDATA = "tempdata/tripixeldata"
GRAHAMDATA = "tempdata/grahamdata"
RITTERDATA = "tempdata/ritterdata"

def TriPixelAlgorithm(filename: str):
    command = "cat {0} | sort -S 80% --parallel=8 -n -s -k1,1 | uniq | executables/tripixel | awk '{{print $2, $1}}' | sort -S 80% --parallel=8 -n -s -k1,1 | executables/tripixel | awk '{{print $2, $1}}' > {1}".format(filename, TRIPIXELDATA)
    process = Popen(command, shell=True)
    process.wait()

    tripixeldataset = Dataset(TRIPIXELDATA)
    return tripixeldataset


def GrahamAlgorithm() -> Dataset:
    command = "cat {0} | executables/graham $(wc -l {0} | awk '{{print $1}}') > {1}".format(TRIPIXELDATA, GRAHAMDATA)
    process = Popen(command, shell=True)
    process.wait()

    time = linecache.getline(GRAHAMDATA, 1)

    grahamdataset = Dataset(GRAHAMDATA, from_line=2)
    return (geo.Shape(grahamdataset.pointslist), time)

def RitterAlgorithm() -> geo.Circle:
    command = "cat {0} | executables/ritter $(wc -l {0} | awk '{{print $1}}') > {1}".format(TRIPIXELDATA, RITTERDATA)
    process = Popen(command, shell=True)
    process.wait()

    time = linecache.getline(RITTERDATA, 1)
    circle = linecache.getline(RITTERDATA, 2)

    rittercircle = geo.Circle(circle)
    
    return (rittercircle, time)

def ToussaintAlgorithm(convexHull: geo.Shape) -> geo.Shape:

    start = time.time()

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

    end = time.time()

    total_time = end - start
    return (minrectangle, total_time)