#! /usr/bin/env python3
import os, json, argparse
from get_spots import writeGeoJ
from get_zones import parseGeoJson 

## deal with arguments
parser = argparse.ArgumentParser()
parser.add_argument('geojson',
            help=("""Name of the geojson file to which you want to\
                    assign zones. """))
parser.add_argument('outFileName',
            help=("""Name of the geojson file to which you want to\
                    assign zones. """))

args = parser.parse_args()

petal,spots,center,edge,throat = parseGeoJson(args.geojson)

## now remove the throat and edge polygons (center should be fine?)

throat, edge = None, None 

aa = writeGeoJ(petal, spots, center, edge, throat)

with open(args.outFileName, 'w') as fp:
    json.dump(aa, fp)
