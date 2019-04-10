#!/usr/bin/env python3

import json, argparse, pathlib
import shapely.geometry as sg
import sys
sys.path.append("/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/package/makeFlowerPolygons")
from geojsonIO import parseGeoJson, writeGeoJ

## arguments:
parser = argparse.ArgumentParser()
parser.add_argument('geojson')
parser.add_argument('spotsDir')
parser.add_argument('otherFeaturesDir')
parser.add_argument('directoryOut')

args = parser.parse_args()
geojson=args.geojson
spotsDir=pathlib.Path(args.spotsDir)
otherFeaturesDir=pathlib.Path(args.otherFeaturesDir)
directoryOut=pathlib.Path(args.directoryOut)

## get file and items from each:

(_, newSpots, _, _, _, _, _, _) = parseGeoJson(spotsDir / geojson)

(petal, _, center, 
edge, throat, spotEstimates, 
photoBB, scalingFactor) = geoj2=parseGeoJson(otherFeaturesDir / geojson)

## write out a new geojson:

geoDict=writeGeoJ(petal, newSpots, center, 
                    edge, throat, spotEstimates, 
                    photoBB, scalingFactor)

with open(str(directoryOut / geojson), 'w') as f:
    json.dump(geoDict, f)
