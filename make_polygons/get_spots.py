#!/usr/bin/env python3

""" this module will create a geojson from 
one of doug's color-simplified rasters, 
with a petal polygon and a spot mulipolygon.
Slots for throat, and edge will be created
but left as empty polygon objects.
"""

import argparse, os, json, shapely, geojsonIO
import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry as sg
import shapely.affinity as sa
import shapely.errors
from skimage import measure

def parseDougMatrix(file):
    orig = np.genfromtxt(file, delimiter=',')
    orig = orig.astype(int)
    Ymax=np.max(orig[:,1]).tolist()
    Ymin=np.min(orig[:,1]).tolist()
    Xmax=np.max(orig[:,0]).tolist()
    Xmin=np.min(orig[:,0]).tolist()
    BB = [
        [Xmin,Ymin],
        [Xmax,Ymin],
        [Xmax,Ymax],
        [Xmin,Ymax],
        ]
    petal = np.zeros([Xmax,Ymax])
    spots = np.zeros([Xmax,Ymax])
    for i in orig:
        petal[i[0]-1,i[1]-1] = i[3]
        spots[i[0]-1,i[1]-1] = i[3]
    ## 0 is background color
    ## 2 is petal color
    ## 3 is spot color
    petal = petal.astype(int)
    petal[petal == 0] = 1
    petal[petal == 2] = 0
    petal[petal == 3] = 0
    spots = spots.astype(int)
    spots[spots == 0] = 1
    spots[spots == 2] = 1
    spots[spots == 3] = 0
    return(BB,petal,spots)


## for the actual conversion of raster to polygon:
def digitizePols(mat):
    """pad margins of image and get the contour of the petal shape"""
    ## is the matrix just background color? then return empty polygon
    if (mat == 1).all(): 
            shapelyPoly = sg.Polygon() 
    else:
        petal_marg = np.insert(mat, mat.shape[1], 1, 1)
        petal_marg = np.insert(petal_marg, 0, 1, 1)
        petal_marg = np.insert(petal_marg, mat.shape[0], 1, 0)
        petal_marg = np.insert(petal_marg, 0, 1, 0)
        Pcontours = measure.find_contours(petal_marg, 0)
        if Pcontours:
            #return(Pcontours)
            ## gotta ditch <3 points, they are lines
            polys = [ i for i in Pcontours if len(i) >= 4 ]
            ## make shapely objects
            if len(polys) == 1: 
                shapelyPoly = sg.Polygon(polys[0]) 
            elif len(polys) > 1: 
                lpols = [ sg.Polygon(i) for i in polys ]
                shapelyPoly = sg.MultiPolygon(lpols) 
        elif not Pcontours: shapelyPoly = sg.MultiPolygon() 
    return(shapelyPoly)


def getPetGeoInfo(pet):
    """get centroid and scaling factor needed to standardize petals and spots"""
    area = pet.area
    scalar = area**(-1/2)
    center = pet.centroid
    centerCoor = (center.x, center.y)
    return(scalar, centerCoor)

def stand(pol, scale, cent):
    """standardize a polygon"""
    trans = sa.translate(pol, (-1*cent[0]), (-1*cent[1]))
    scaled = sa.scale(trans, xfact=scale, yfact=scale, origin = (0,0))
    return(scaled)

## clean up small polygons and points
def cleanCollections(geo):
    """sometimes our digitizing of petals creates smatterings of geometries instead
    of a single clean polygon. This attempts to prune down to the main polygon,
    which is usually the object we want."""
    if not geo.is_valid: 
        print('polygon invalid, buffering')
        geo = geo.buffer(0.0)
    if isinstance(geo, sg.collection.BaseMultipartGeometry):
        onlyPolys = [ i for i in geo if type(i) == sg.polygon.Polygon ]
        areas = [ i.area for i in onlyPolys ]
        biggestPoly = [ i for i in onlyPolys if i.area == max(areas) ][0]
    elif isinstance(geo, sg.Polygon):
        biggestPoly = geo
    return(biggestPoly)

def cleanSpots(SpotsMultiPoly):
    """Tries to clean up spot collections, leaving them as a multipolygon"""
    if not SpotsMultiPoly.is_valid: 
        print('polygon invalid, buffering')
        SpotsMultiPoly = SpotsMultiPoly.buffer(0.0)
    if isinstance(SpotsMultiPoly, sg.MultiPolygon):
        SpotsMultiPoly = sg.MultiPolygon([ i.buffer(0.0) for i in SpotsMultiPoly ])
    elif isinstance(SpotsMultiPoly, sg.Polygon):
        SpotsMultiPoly = SpotsMultiPoly.buffer(0)
    return(SpotsMultiPoly)


if __name__ == "__main__":

    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('file', 
                help=("""Name of file that contains CSV versions of 
                         doug's "melted" matrix, the result of 
                         manually choosing color centers from his 
                         matlab color-categorization scripts.
                       """))
    parser.add_argument('--destination', "-d",
                help=("""Folder where you would like this file. Default
                        is same directory."""),
                default=None)

    args = parser.parse_args()

    ### File Names
    meltFullName = os.path.realpath(args.file)
    meltBaseName = os.path.basename(meltFullName)
    meltParentDir = os.path.dirname(meltFullName)
    petalName = os.path.basename(meltParentDir)
    flowerName = os.path.basename(os.path.dirname(meltParentDir))
    gjName = (flowerName + "_"
              + petalName
              + "_polys")
    if args.destination is None: 
        outFileName = ( meltParentDir + "/"
                        + gjName
                        + ".geojson")
    if args.destination is not None: 
        outFileName = ( args.destination  + "/"
                        + gjName
                        + ".geojson")



    ## run through digitizing, standardizing
    os.chdir(meltParentDir)
    print(gjName)
    aa = os.listdir()

    photoBB, petalMat, spotsMat = parseDougMatrix(meltBaseName)
    petPolRaw = digitizePols(petalMat) 
    petPol = cleanCollections(petPolRaw)
    spotPolRaw = digitizePols(spotsMat)
    spotPol = cleanSpots(spotPolRaw)

    scale, cent = getPetGeoInfo(petPol)
    standPet = stand(petPol, scale, cent)
    if isinstance(spotPol, sg.MultiPolygon): 
        standSpot = [ stand(i, scale, cent) for i in spotPol ]
    elif isinstance(spotPol, sg.Polygon): 
        standSpot = [stand(spotPol, scale, cent)]
    standSpots = shapely.geometry.multipolygon.MultiPolygon(standSpot)
    ## deal with the zones elsewhere
    center, edge, throat, spotEstimates = None, None, None, None

    ## outputs ##

    ## define get a dictionary that resembles a geojson feature collection:

    geoDict = geojsonIO.writeGeoJ(standPet, standSpots, 
                                    center, edge, throat, 
                                    spotEstimates, photoBB, scale)

    ## write it out
    with open(outFileName, 'w') as fp:
        json.dump(geoDict, fp)



