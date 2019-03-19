#! /usr/bin/env python3 

import argparse, json
import shapely.validation as sv
from makeFlowerPolygons import geojsonIO
from makeFlowerPolygons.geojsonIO import parseGeoJson, writeGeoJ

## arguments:
parser = argparse.ArgumentParser()
parser.add_argument('geojson')
parser.add_argument('-l', '--log', default=None)
args = parser.parse_args()

## for dev:
#geojson="/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/polygons/plate3/P810F2/right/P810F2_right_polys.geojson"
#log="geojson_validity_log.txt"

geojson=args.geojson
if not args.log:
    log="geojson_validity_log.txt"
else:
    log=args.log

aa = parseGeoJson(geojson)

## check validity:
print(sv.explain_validity(aa[1]))
