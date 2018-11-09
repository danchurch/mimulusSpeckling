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

def parseDougMatrix(file):
    """Get numpy arrays that can be used as images
    from Doug's weird melted matrix that results
    when you manually correct his color centers """
    orig = np.genfromtxt(file, delimiter=',')
    orig = orig.astype(int)
    Ymax=np.max(orig[:,1])
    Xmax=np.max(orig[:,0])
    petal = np.zeros([Xmax,Ymax])
    spots = np.zeros([Xmax,Ymax])
    for i in orig:
        petal[i[0]-1,i[1]-1] = i[3]
        #petal[i[1]-1,i[0]-1] = i[3]
        #spots[i[1]-1,i[0]-1] = i[3]
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
    return(petal,spots)




## for the actual conversion of raster to polygon:
def digitizePols(mat):
    """pad margins of image and get the contour of the petal shape"""
    petal_marg = np.insert(mat, mat.shape[1], 1, 1)
    petal_marg = np.insert(petal_marg, 0, 1, 1)
    petal_marg = np.insert(petal_marg, mat.shape[0], 1, 0)
    petal_marg = np.insert(petal_marg, 0, 1, 0)
    Pcontours = measure.find_contours(petal_marg, 0)
    #return(Pcontours)
    ## gotta ditch <3 points, they are lines
    polys = [ i for i in Pcontours if len(i) >= 4 ]
    ## make shapely objects
    try:
        assert len(polys) > 0
        if len(polys) == 1: 
            shapelyPoly = sg.Polygon(polys[0]) 
        elif len(polys) > 1: 
            lpols = [ sg.Polygon(i) for i in polys ]
            shapelyPoly = sg.MultiPolygon(lpols) 
        return(shapelyPoly)
    except AssertionError as err:
        print("No polygons returned. " + str(err))
        return()


## debugging
#exL="/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/polygons/P247F1/left/P247F1_left_melted.csv"
#petal, spots = parseDougMatrix(exL)
#
#exR="/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/polygons/P247F1/right/P247F1_right_melted.csv"
#petal, spots = parseDougMatrix(exR)
#
#aa = digitizePols(petal)
#bb = digitizePols(spots)
#
#plt.ion()
#
#plt.close('all')
#
#fig, ax = plt.subplots(1,1)
#ax.imshow(petal, cmap='gray')
#
#
#fig, axes = plt.subplots(nrows=1,ncols=2, sharey=True)
#axes[0].imshow(petal, cmap='gray')
#axes[1].imshow(spots, cmap='gray')
#
#os.chdir('/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons')
#import FlowerPetal
#
#fl = FlowerPetal.FlowerPetal()
#
#fl.plotOne(aa)
#fl.addOne(bb)

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


def writeGeoJ(petal, spots, center, edge, throat):
    """Function for putting polygons into a dictionary that can be written out \
    to json format, = geojson."""
    featC = {
            "type" : "FeatureCollection",
            "features" : [],
            }

    ## fill it with features
    partNames = ['Petal', 'Spots', 'Center', 'Edge', 'Throat']
    ## each geometry needs a feature wrapper
    for i,part in enumerate([petal, spots, center, edge, throat]):
        try:
            gj_i = sg.mapping(part)
        except (NameError, AttributeError):
            gj_i = {"type": "Polygon", "coordinates": []}
        finally:
            feature_i = {"type": "Feature",
                  "geometry": gj_i,
                  "properties": {"id":(partNames[i])}}
            featC['features'].append(feature_i)
    return(featC)

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

    petalMat, spotsMat = parseDougMatrix(meltBaseName)
    petPolRaw = digitizePols(petalMat) 
    petPol = cleanCollections(petPolRaw)
    spotPol = digitizePols(spotsMat)

    scale, cent = getPetGeoInfo(petPol)
    standPet = stand(petPol, scale, cent)
    if isinstance(spotPol, sg.MultiPolygon): 
        standSpot = [ stand(i, scale, cent) for i in spotPol ]
    elif isinstance(spotPol, sg.Polygon): 
        standSpot = [stand(spotPol, scale, cent)]
    standSpots = shapely.geometry.multipolygon.MultiPolygon(standSpot)
    ## deal with the zones elsewhere
    center, edge, throat = None, None, None

    ## outputs ##

    ## define get a dictionary that resembles a geojson feature collection:

    geoDict = writeGeoJ(standPet, standSpots, center, edge, throat)

    ## write it out
    with open(outFileName, 'w') as fp:
        json.dump(geoDict, fp)

## buffer out silf-intersections when digitizing


