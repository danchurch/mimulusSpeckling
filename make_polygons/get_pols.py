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


## name of folder, based on image
cwd = os.getcwd()
fullFolderName = cwd + "/" + os.path.basename(imageName)
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
    polyname = fullFolderName + "/" + os.path.basename(imageName) + "_poly" + str(n) + ".csv"
    np.savetxt(fname=polyname, X=contour.astype(int), delimiter=',')


%%%%%%%%%%%%%%%%%%%%


%% okay, the problems with the polygon digitization need to be fixed, one 
%% way or another. 

%% The problems are:

%% 1) doug's color simplification sometimes caused cracks or leaks of photo 
%% background color into the images. The digitization process followed these
%% creaks and this broke up the petal polygons.

%% 2) Holes in petal-spots are interpreted as additional spots, not as petal

%% 3) Some petals were interpreted as entirely spot, usually when there were
%% no significant spots at all on the petal.

%% the second I can fix by tweaking our digitization algorithm. 1 and 3 are 
%% problems deeper in the image analysis, from Doug's color simplication 
%% process. I think. But #3 is a mystery to me. 


%% of course, Arielle would like an edge statistic, too...

%% let's look at #3 a little bit.

%% some examples
P428F1  
P428F2  
P430F2

%% let's bring up the structures:

wd = '/Users/danthomas/Documents/speckling/make_polygons/';
objDir="/Users/danthomas/Documents/speckling/make_polygons/matObjW_pol/";
dougDir = "/Users/danthomas/Documents/speckling/dougRaster/Rotated_and_Cropped/";
fname = 'P428F2';

load(objDir + fname + ".mat")

petal = Petals.Polys.right.petal(1);

spots = Petals.Polys.right.spots;

hold off;
plot(petal)
hold on;
plot(spots(1))
%%

hold off;
plot(spots(1))

hold off;
plot(spots(2))
