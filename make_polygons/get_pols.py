#!/usr/bin/env python3

import argparse, os
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, io, filters, measure

## instantiate the argparser
parser = argparse.ArgumentParser()
## deal with arguments:
parser.add_argument('file', 
            help="Name of the .csv file from matlab that contains grayscale information about a petal.")
args = parser.parse_args()

## get our image in...
aa  = np.genfromtxt(args.file, delimiter = ",")

## set up our directory for saving files

## name of raster image (a petal or a spots grayscale matrix from matlab)
imageName = args.file[:-4] ## no file extension
#imageName = argsfile[:-4] ## no file extension

## current directory
cwd = os.getcwd()
## name of folder, based on image
fullFolderName = cwd + "/" + imageName
## make a new directory for the CSVs
## we will make at the end of all this:
os.makedirs(fullFolderName, exist_ok=True)

aR = aa.shape[0] ## number of rows
aC = aa.shape[1] ## number of cols

## add one pixel of white to rows:
aa_marg = np.insert(aa, aR, 1, 0)
aa_marg = np.insert(aa_marg, 0, 1, 0)
## and columns:
aa_marg = np.insert(aa_marg, aC, 1, 1)
aa_marg = np.insert(aa_marg, 0, 1, 1)

## find the contours:
contours = measure.find_contours(aa_marg, 0)

## save them out:

for n, contour in enumerate(contours):
    polyname = fullFolderName + "/" + imageName + "_poly" + str(n) + ".csv"
    np.savetxt(fname=polyname, X=contour.astype(int), delimiter=',')


