# coding=utf-8
__author__ = 'david'
import  sys

allFeaturesFile = sys.argv[1]
numberOfFeatures = int(sys.argv[2])
reducedFile = "reduced-" + str(numberOfFeatures) + "-" + allFeaturesFile

inFile = open(allFeaturesFile, "r")
outFile = open(reducedFile, "w")

for line in inFile:
    f = line.split()
    outFile.write(" ".join(f[:numberOfFeatures]) + "\n")

inFile.close()
outFile.close()
