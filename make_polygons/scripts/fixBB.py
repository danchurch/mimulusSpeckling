#!/usr/bin/env python3
import argparse, json 
from makeFlowerPolygons import geojsonIO
#from makeFlowerPolygons.get_spots import parseDougMatrix, digitizePols, cleanPetal

## while working without internet, for updating packages
import sys
sys.path.append("/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/package/makeFlowerPolygons")
from get_spots import parseDougMatrix, digitizePols, cleanPetal



## deal with args:
parser = argparse.ArgumentParser()
parser.add_argument('geojson')
parser.add_argument('csv')
parser.add_argument('-o', '--outFileName', default=None)
args = parser.parse_args()

if not args.outFileName:
    outFileName=args.geojson
else:
    outFileName=args.outFileName

## script

(petal,spots,center,edge,throat,
    spotEstimates, photoBB,
                scalingFactor) = geojsonIO.parseGeoJson(args.geojson)
 
_, petalCSV, _ = parseDougMatrix(args.csv)
rawPetal = digitizePols(petalCSV)
clePetal = cleanPetal(rawPetal)
## get our new photoBB
photoBB = list(clePetal.bounds)

## write it out
geoDict = geojsonIO.writeGeoJ(petal, spots,
                                center, edge, throat,
                                spotEstimates, photoBB, scalingFactor)

with open(outFileName, 'w') as fp:
    json.dump(geoDict, fp)
