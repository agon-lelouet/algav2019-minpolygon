import os
import zipfile
import ssl
import wget
import csv
import numpy as np
from Geometry import coordinates
from random import randint

#: Index of the last file after cleaning
NB_FILES = 1663
ALL_FILES = ['samples/test-%s.points' % i for i in range(NB_FILES)]

def download() -> bool:
    """Download the dataset from internet if it doesn't exist.
    Returns:
        bool: True if it had to be downloaded.
    """
    if os.path.isdir('samples') and len(ALL_FILES) > 0:
        _clean_files()
        return False
    url = 'http://www-apr.lip6.fr/~buixuan/files/algav2019/Varoumas_benchmark.zip'
    ssl._create_default_https_context = ssl._create_unverified_context
    filename = wget.download(url)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall()
    os.unlink(filename)
    _clean_files()
    return True

def _clean_files() -> None:
    """Well ok it's quite dirty, but the first file is corrupted
    and it is easier to start counting from 0.
    """
    try:
        os.rename('samples/test-%s.points' %
                  (NB_FILES + 1), 'samples/test-0.points')
        os.replace('samples/test-%s.points' %
                   (NB_FILES), 'samples/test-1.points')
    except FileNotFoundError:
        pass

def getFromFile(filename: str) -> list:
    """Given a filename, parses the file as a list of points
    Args:
        filename (str): The name of the file to parse
    Returns:
        (list): the constructed set of points 
    """
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=" ")
        return np.array([ coordinates(float(row[0]), float(row[1])) for row in reader ])

def getDataset(size: int) -> list:
    """Given a number of files, parse the samples folder to construct a dataset of points
        Args:
        size (int): The number of files to parse
    Returns:
        (list): the constructed set of points 
    """
    if size == 0 or size > NB_FILES:
        print("dataset s3.ize can't be 0")
        size = 1
    alreadyChosen = []
    toreturn = []
    
    # dirty, mais pas de do...while en python
    while True:
        if len(alreadyChosen) == size:
            break
        
        i = randint(0, NB_FILES)
        if i in alreadyChosen:
            continue
        alreadyChosen.append(i)
        filename = file = 'samples/test-%s.points' % (i)
        templist = getFromFile(filename)
        toreturn = toreturn + templist
    return toreturn

def getXList(pointsSet: list):
    """Gets all the x coordinates from the point set
        Args:
        pointSet (list): The point set to parse
    Returns:
        (list): the list of x coordinates
    """
    return np.array([ point.getX() for point in pointsSet ])

def getYList(pointsSet: list):
    """Gets all the y coordinates from the point set
        Args:
        pointSet (list): The point set to parse
    Returns:
        (list): the list of y coordinates
    """
    return np.array([ point.getY() for point in pointsSet ])


def getMinPoint(pointdataset: list, xoryset: list) -> coordinates:
    """Gets the minimum point with the min x or y from the point data set
        use in conjuction with getXList or getYList
        Args:
        pointSet (list): The point set to parse
        xoryset (list): The list of x or y points to use as a reference
    Returns:
        (coordinates): the min x or y point from this set 
    """
    return pointdataset[np.argmin(xoryset)]

def getMaxPoint(pointdataset: list, xoryset: list) -> coordinates:
    """Gets the max point with the min x or y from the point data set
        use in conjuction with getXList or getYList
        Args:
        pointSet (list): The point set to parse
        xoryset (list): The list of x or y points to use as a reference
    Returns:
        (coordinates): the max x or y point from this set 
    """
    return pointdataset[np.argmax(xoryset)]
