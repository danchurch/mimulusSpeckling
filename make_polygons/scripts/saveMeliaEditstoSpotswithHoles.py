#!/usr/bin/env python3

import json, argparse, pathlib
import shapely.geometry as sg
import sys
sys.path.append("/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/package/makeFlowerPolygons")
from geojsonIO import parseGeoJson, writeGeoJ

## arguments:
parser = argparse.ArgumentParser()
parser.add_argument('geojson')
parser.add_argument('directory1')
parser.add_argument('directory2')
parser.add_argument('directoryOut')
args = parser.parse_args()
geojson=args.geojson
directory1=pathlib.Path(args.directory1)
directory2=pathlib.Path(args.directory2)
directoryOut=pathlib.Path(args.directoryOut)

## get file and items from each:

(_, newSpots, _, _, _, _, _, _) = parseGeoJson(directory1 / geojson)

(petal, _, center, 
edge, throat, spotEstimates, 
photoBB, scalingFactor) = geoj2=parseGeoJson(directory2 / geojson)

## write out a new geojson:

geoDict=writeGeoJ(petal, newSpots, center, 
                    edge, throat, spotEstimates, 
                    photoBB, scalingFactor)

with open(str(directoryOut / geojson), 'w') as f:
    json.dump(geoDict, f)
