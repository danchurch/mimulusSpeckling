#!/usr/bin/env python3

""" this module will create a geojson from 
one of doug's color-simplified rasters, 
with a petal polygon and a spot mulipolygon.
Slots for throat, and edge will be created
but left as empty polygon objects.
"""

import argparse, os, json, shapely
import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry as sg
import shapely.affinity as sa
import shapely.errors
from skimage import measure

## for the actual conversion of raster to polygon:
def digitizePols(file):
    """pad margins of image and get the contour of the petal shape"""
    petal = np.genfromtxt (file, delimiter=",")
    petal_marg = np.insert(petal, petal.shape[1], 1, 1)
    petal_marg = np.insert(petal_marg, 0, 1, 1)
    petal_marg = np.insert(petal_marg, petal.shape[0], 1, 0)
    petal_marg = np.insert(petal_marg, 0, 1, 0)
    Pcontours = measure.find_contours(petal_marg, 0)
    ## gotta ditch <3 points, they are lines
    polys = [ i for i in Pcontours if len(i) > 3 ]
    return(polys)

def getPetGeoInfo(pet):
    """get centroid and scaling factor needed to standardize petals and spots"""
    aa = sg.asPolygon(pet)
    area = aa.area
    scalar = area**(-1/2)
    center = aa.centroid
    centerCoor = (center.x, center.y)
    return(scalar, centerCoor)

def stand(pol, scale, cent):
    """standardize a polygon"""
    aa = sg.asPolygon(pol)
    trans = sa.translate(aa, (-1*cent[0]), (-1*cent[1]))
    scaled = sa.scale(trans, xfact=scale, yfact=scale, origin = (0,0))
    return(scaled)

## clean up small polygons and points
def cleanCollections(geo):
    """sometimes our digitizing creates smatterings of geometries instead\
    of a single clean polygon. This attempts to prune down to the main polygon,\
    which is usually the object we want."""
    if type(geo) is not sg.polygon.Polygon:
        if type(geo) is sg.collection.GeometryCollection:
            onlyPolys = [ i for i in geo if type(i) == sg.polygon.Polygon ]
        else:
            onlyPolys = geo
        areas = [ i.area for i in onlyPolys ]
        biggestPoly = [ i for i in onlyPolys if i.area == max(areas) ][0]
        return(biggestPoly)
    elif type(geo) is sg.polygon.Polygon:
        return(geo)



if __name__ == "__main__":

    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', 
                help=("Name of folder that contains two files:"
                      " that contains grayscale petal outlint and spot "
                        "information in the form of CSVs."))
    parser.add_argument('destination', 
                help=("Folder where you would like this file."))
    args = parser.parse_args()

    ## organize name
    os.chdir(args.folder)
    here = os.getcwd()
    petalName = os.path.basename(here)
    flowerName = os.path.basename(os.path.dirname(here))
    gjName = (flowerName + "_"
              + petalName
              + "_polys")
    outFileName = ( args.destination + "/"
                    + flowerName + "_"
                    + petalName
                    + "_polys.geojson")

    ## run through digitizing, standardizing, zone calling pipeline
    print(gjName)
    aa = os.listdir()
    for i in aa:
        if "petal" in i:
            petPol = digitizePols(i)[0] 
        elif "spots" in i:
            spotPol = digitizePols(i)
    scale, cent = getPetGeoInfo(petPol)
    standPet = stand(petPol, scale, cent)
    standSpot = [ stand(i, scale, cent) for i in spotPol ]
    standSpots = shapely.geometry.multipolygon.MultiPolygon(standSpot)
    center, edge, throat = None, None, None

    ## outputs ##

    ## define get a dictionary that resembles a geojson feature collection:
    featC = {
            "type" : "FeatureCollection",
            "features" : [],
            }

    ## fill it with features
    partNames = ['Petal', 'Spots', 'Center', 'Edge', 'Throat']
    ## each geometry needs a feature wrapper
    for i,part in enumerate([standPet, standSpots, center, edge, throat]):
        try:
            gj_i = sg.mapping(part)
        except (NameError, AttributeError):
            gj_i = {"type": "Polygon", "coordinates": []}
        finally:
            feature_i = {"type": "Feature",
                  "geometry": gj_i,
                  "properties": {"id":(partNames[i])}}
            featC['features'].append(feature_i)

    ## write it out
    with open(outFileName, 'w') as fp:
        json.dump(featC, fp)


