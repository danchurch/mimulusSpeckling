#!/usr/bin/env python3

"""this is a one-shot module for retroactively 
getting bounding boxes into geojsons that don't 
have them. In the future, this will be done as
part of the digitizing pipeline."""

import json
import argparse
import geojsonIO
import numpy as np

def getBB(file):
    orig = np.genfromtxt(file, delimiter=',')
    orig = orig.astype(int)
    Ymax=max(orig[:,1])
    Ymin=min(orig[:,1])
    Xmax=max(orig[:,0])
    Xmin=min(orig[:,0])
    BB = np.array([
        [Xmin,Ymin],
        [Xmax,Ymin],
        [Xmax,Ymax],
        [Xmin,Ymax],
        ]).tolist()
    return(BB)


def addPhotoBB(geojson, csv):
    petal,spots,center,edge,throat, spotEstimates, photoBB = geojsonIO.parseGeoJson(geojson)
    photoBB = getBB(csv)
    newGeo = geojsonIO.writeGeoJ(petal, spots, center, edge, throat, spotEstimates, photoBB)
    with open(geojson, 'w') as fp:
        json.dump(newGeo, fp)

if __name__ == "__main__":

    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('geojson',
                help=("""Name of the geojson file to which you want to\
                        add a photo bounding box. """))
    parser.add_argument('csv',
                help=("""the csv for the petal of interest, from Doug's pipeline."""),
                type=str)

    args = parser.parse_args()

    addPhotoBB(args.geojson, args.csv)
