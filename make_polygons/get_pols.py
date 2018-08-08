#!/usr/bin/env python3

import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage import data, io, filters, measure

## instantiate the argparser
parser = argparse.ArgumentParser()

## argument:
parser.add_argument('file', 
            help="Name of the .csv file from matlab that contains grayscale information about a petal.")

args = parser.parse_args()

## get our image in...
aa  = np.genfromtxt(args.file, delimiter = ",")

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

imageName = args.file[:-4] ## no file extension

for n, contour in enumerate(contours):
    polyname = imageName + "_poly" + str(n) + ".csv"
    np.savetxt(fname=polyname, X=contour.astype(int), delimiter=',')

