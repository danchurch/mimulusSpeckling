#!/usr/bin/env python3

import json, argparse
import pandas as pd
import matplotlib.pyplot as plt
import shapely.geometry as sg
from makeFlowerPolygons.geojsonIO import parseGeoJson

## arguments
parser = argparse.ArgumentParser()

parser.add_argument('geojson',
            help=("""Name of the geojson file from which to 
                extract spotEstimates."""))
parser.add_argument('out',
            help=("Name for outfile."))

args = parser.parse_args()

if args.out is not None:
    outFileName = args.out
else:
    outFileName = args.geojson

## for dev:
#geoj=('/home/daniel/Documents/cooley_lab/'
#            'mimulusSpeckling/make_polygons/'
#            'toy/P773F1_left_polys.geojson')

## get our circles:

_,_,_,_,_,aa,_,_ = parseGeoJson(argparse.geojson)

## we need a dataframe of x,y,area

## get info
xx = [ i.centroid.x for i in aa ]
yy = [ i.centroid.y for i in aa ]
areas = [ i.area for i in aa ]

## make dataframe
da = np.array([xx,yy,areas])
dat = np.transpose(da)
df = pd.DataFrame(dat, columns=['x','y','area'])

## export as csv:
df.to_csv(args.out, index=False)
