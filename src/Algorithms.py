import Geometry as geo
import numpy as np
from Data import Dataset
from subprocess import Popen, PIPE, STDOUT
import os

def GrahamAlgorithm(dataset: Dataset) -> Dataset:
    executable = os.path.abspath(os.path.join(os.getcwd(), "executables/graham"))
    process = Popen([ executable, str(len(dataset.pointslist)) ], stdin=PIPE, stdout=PIPE, stderr=STDOUT)

    dataset.to_stdin(process)

    grahamStdout = process.communicate()[0]
    process.stdin.close()

    grahamdataset = Dataset()
    grahamdataset.from_stdout(grahamStdout)
    return grahamdataset


def ToussaintAlgorithm(convexHull: list) -> list:
    #here too
    return []
