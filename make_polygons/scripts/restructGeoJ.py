#!/usr/bin/env python3

import argparse, json
from makeFlowerPolygons import geojsonIO

parser = argparse.ArgumentParser()
parser.add_argument('geojson')
parser.add_argument('-o', '--outFileName', default=None)
args = parser.parse_args()

if not args.outFileName:
    outFileName=args.geojson
else:
    outFileName=args.outFileName

## reading old format
(petal,spots,center,edge,throat,
    spotEstimates, photoBB,
                scalingFactor) = geojsonIO.parseGeoJson(args.geojson)

geoDict = geojsonIO.writeGeoJ(petal, spots,
                                center, edge, throat,
                                spotEstimates, photoBB, scalingFactor)

with open(outFileName, 'w') as fp:
    json.dump(geoDict, fp)
