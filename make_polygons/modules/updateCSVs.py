#!/usr/bin/env python3

import os, argparse
import numpy as np
from get_spots import parseDougMatrix

## args
parser = argparse.ArgumentParser()
parser.add_argument('meltedDir',
            help=("""Name of the melted matrix from Doug to which you want 
                    save as two CSVs (petal and spots). """))
args = parser.parse_args()

matfile = args.meltedDir 

##matfile="/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/polygons/P247F1/right/P247F1_right_melted.csv"

## parse melted dir, make petal and spot matrices
petal,spots = parseDougMatrix(matfile)

## can we shave this down to the edges of the petals?
petalRows = np.any(petal!=1, axis=1)

newPetal = petal[petalRows,:]
newSpots = spots[petalRows,:]
## use petal outline as boundary

## name stuff
meltName = os.path.basename(matfile)
meltDir = os.path.dirname(matfile)
petalName = meltName.replace("melted","petal")
outPetalName = meltDir + "/" + petalName
spotsName = meltName.replace("melted","spots")
outSpotsName = meltDir + "/" + spotsName

## save out
np.savetxt(outPetalName, newPetal, delimiter = ',')
np.savetxt(outSpotsName, newSpots, delimiter = ',')

