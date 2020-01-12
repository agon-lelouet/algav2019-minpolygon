import os
import zipfile
import ssl
import wget
import csv
import numpy as np
from random import randint
from Geometry import point

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

def getrandomfile():
        i = randint(0, NB_FILES)
        return 'samples/test-%s.points' % (i)


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

class Dataset:
    def __init__(self, pointslist: np.array):
        self.pointslist = pointslist

    def from_file(self, filename: str, from_line=1):
        """Given a filename, parses the file as a list of points
        Args:
            filename (str): The name of the file to parse
        Returns:
            (list): the constructed set of points 
        """
        with open(filename, "r") as f:
            reader = csv.reader(f, delimiter=" ")
            for i in range(1, from_line):
                next(f)
            self.pointslist = np.array([ point(float(row[0]), float(row[1])) for row in reader ])

    def draw(self, plot, color, label, withlines=False):
        plot.scatter(self.getXList(), self.getYList(), alpha=0.8, c=color, edgecolors='none', s=30, label=label)
        if withlines:
            plot.plot(self.getXList(), self.getYList(), color=color, ls="solid")

    def toString(self):
        for point in self.pointslist:
            print(point.tointstring())

    def getXList(self) -> np.array:
        """Gets all the x coordinates from the point set
            Args:
            pointSet (list): The point set to parse
        Returns:
            (list): the list of x coordinates
        """
        return np.array([ point.getX() for point in self.pointslist ])

    def getYList(self) -> np.array:
        """Gets all the y coordinates from the point set
            Args:
            pointSet (list): The point set to parse
        Returns:
            (list): the list of y coordinates
        """
        return np.array([ point.getY() for point in self.pointslist ])


    def getMinPoint(self, xoryset: list) -> point:
        """Gets the minimum point with the min x or y from the point data set
            use in conjuction with getXList or getYList
            Args:
            pointSet (list): The point set to parse
            xoryset (list): The list of x or y points to use as a reference
        Returns:
            (point): the min x or y point from this set 
        """
        return self.pointslist[np.argmin(xoryset)]

    def getMaxPoint(self, xoryset: list) -> point:
        """Gets the max point with the min x or y from the point data set
            use in conjuction with getXList or getYList
            Args:
            pointSet (list): The point set to parse
            xoryset (list): The list of x or y points to use as a reference
        Returns:
            (point): the max x or y point from this set 
        """
        return self.pointslist[np.argmax(xoryset)]
