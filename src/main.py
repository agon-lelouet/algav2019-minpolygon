import Data
from Algorithms import GrahamAlgorithm

Data.download()

dataset = Data.Dataset()
dataset.from_file()

GrahamAlgorithm(dataset)
