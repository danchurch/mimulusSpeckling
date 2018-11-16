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

## parse melted dir, make petal and spot matrices
petal,spots = parseDougMatrix(matfile)

## name stuff
meltName = os.path.basename(matfile)
meltDir = os.path.dirname(matfile)
petalName = meltName.replace("melted","petal")
outPetalName = meltDir + "/" + petalName
spotsName = meltName.replace("melted","spots")
outSpotsName = meltDir + "/" + spotsName

## save out
np.savetxt(outPetalName, petal, delimiter = ',')
np.savetxt(outSpotsName, spots, delimiter = ',')


