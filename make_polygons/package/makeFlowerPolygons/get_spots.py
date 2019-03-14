#!/usr/bin/env python3

""" this module will create a geojson from 
one of doug's color-simplified rasters, 
with a petal polygon and a spot mulipolygon.
Slots for throat, and edge will be created
but left as empty polygon objects.
"""

import matplotlib
matplotlib.use('TkAgg')
import argparse, os, json, shapely
import numpy as np
import matplotlib.pyplot as plt
import shapely.validation as sv
import shapely.geometry as sg
import shapely.affinity as sa
import shapely.errors
from skimage import measure
## while developing:
#import sys
#sys.path.append("/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/package/")


from makeFlowerPolygons import geojsonIO

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

################# shapely object cleaning ##################################

def testAndFixPoly(pol,gjName=None,objtype=None):
    """
    an attempt to fix invalid polygons.
    Multipolygons are not accepted here.
    """
    if pol.is_valid and not pol.is_empty:
        return(pol)
        ## try buffering.
    elif  pol.is_empty:
        print("{} {} is empty!".format(gjName,objtype))
        return(pol)
        ## try buffering.
    elif not pol.is_valid:
        print("{} {} is invalid! Opening bag of tricks".format(gjName,objtype))
    try:
        print("Trying buffering")
        newPoly=pol.buffer(0.0)
        ## sometimes this creates multiplte polygons...
        if isinstance(newPoly, sg.collection.BaseMultipartGeometry):
            print("multiple polygons detected where there should only be one")
            newPoly=getBiggest(newPoly)
        assert(newPoly.is_valid)
        assert(newPoly.is_empty is False)
        print("Buffering complete. {} {} seems better.".format(gjName,objtype))
        return(newPoly)
    except AssertionError:
        print("Buffering doesn't help.")
    try:
        print("Trying simplification.")
        newPoly=pol.simplify(0.0)
        ## not sure, but this may also create new polygons. To be safe:
        if isinstance(newPoly, sg.collection.BaseMultipartGeometry):
            print("multiple polygons detected where there should only be one")
            newPoly=getBiggest(newPoly)
        assert(newPoly.is_valid)
        assert(newPoly.is_empty is False)
        print("Simplification complete. {} {} seems better.".format(gjName,objtype))
        return(newPoly)
    except AssertionError:
        print("Simplifying polygon doesn't help either. Returning original.")
        if not newPoly.is_valid:
            print("Careful. {} {} object is invalid because:".format(gjName,objtype))
            print(sv.explain_validity(pol))
        if newPoly.is_empty:
            print("Careful. {} {} object is empty!")
        return(pol)

def getBiggest(multipol):
    onlyPolys = [ i for i in multipol if type(i) == sg.polygon.Polygon ]
    areas = [ i.area for i in onlyPolys ]
    biggestPoly = [ i for i in onlyPolys if i.area == max(areas) ][0]
    return(biggestPoly)

## clean up small polygons and points
def cleanPetal(geo, gjName=None):
    """sometimes our digitizing of petals creates smatterings of geometries instead
    of a single clean polygon. This attempts to prune down to the main polygon,
    which is usually the object we want."""
    objtype="petal"
    if isinstance(geo, sg.collection.BaseMultipartGeometry):
        biggestPoly = getBiggest(geo)
    elif isinstance(geo, sg.Polygon):
        biggestPoly = geo
    try:
        newGeo = testAndFixPoly(biggestPoly, gjName, objtype)
    except TypeError:
        print("Are you sure this petal object?")
        return(Geo)
    return(newGeo)

def cleanIndividualSpotPolys(SpotsMultiPoly, gjName=None):
    """Tries to clean up spots collections, leaving them as a multipolygon.
        Note that cleaning the spots individually does not necessarily
        mean that the outputted multipolygon is valid. After spots and
        holes have been called from these polygons, the resulting multipolygon
        also often has to be buffered again, as a single object, in the 
        function 'cleanFinalSpotsMultpoly()'.
    """
    objtype="spots"
    if isinstance(SpotsMultiPoly, sg.Polygon):
        cleanPoly = testAndFixPoly(SpotsMultiPoly, gjName, objtype)
        cleanMultPoly = sg.MultiPolygon([cleanPoly])
    elif isinstance(SpotsMultiPoly, sg.MultiPolygon):
        polyList= [testAndFixPoly(i, gjName, objtype) for i in SpotsMultiPoly]
        cleanMultPoly = sg.MultiPolygon(polyList)
    else:
        raise TypeError('Are you sure you have a [multi]polygon?')
    return(cleanMultPoly)


def cleanFinalSpotsMultpoly(SpotsMultiPoly):
    if not SpotsMultiPoly.is_valid:
        print('Buffering spot multipolygon.')
        cleanMultPoly = SpotsMultiPoly.buffer(0)
        return(cleanMultPoly)
    elif SpotsMultiPoly.is_valid:
        print('This spot multipolygon seems okay without buffering.')
        return(SpotsMultiPoly)

################# shapely object cleaning ##################################
################## holes in spots #########################

class SpotHole():
    def __init__(self,
                poly=None,
                level=None,
                parentPoly=None,
                holez=None):
        self.poly=poly
        self.level=level
        self.isSpot=None
        self.isHole=None
        self.parentPoly=parentPoly
        if holez is None:
            holez=[]
        self.holez=[]

    def callSpotOrHole(self):
        if self.level is not None and self.level % 2 == 0:
            self.isSpot=True
            self.isHole=False
        elif self.level is not None and self.level % 2 == 1:
            self.isSpot=False
            self.isHole=True
        return

    def makeHolesInPoly(self):
        listHoleCoords=[]
        outsideCoords=list(self.poly.exterior.coords)
        if self.holez:
            for i in self.holez:
                listHoleCoords.append(list(i.exterior.coords))
        finalDonut=sg.Polygon(outsideCoords, listHoleCoords)
        self.poly=finalDonut

def findBiggest(l):
    aa = [ i.area for i in l ]
    try:
        bb = max(aa)
        bigspot = [ i for i in l if i.area == bb ][0]
    except (ValueError, IndexError):
        bigspot = None
    return bigspot

def dig2bottom(startPol=None,l=[],level=0,parentSpotHole=None):
    if l:
        bottom=SpotHole()
        bottom.poly=startPol
        if parentSpotHole:
            bottom.parentPoly = parentSpotHole.poly
        bottom.level = level
        nextl = [ i for i in l if not i.equals(bottom.poly) and i.within(bottom.poly) ]
        nextPoly = findBiggest(nextl)
        level+=1
        nextSpotHole=dig2bottom(nextPoly,nextl,level,bottom)
        return(nextSpotHole)
    elif not l:
        bottom = parentSpotHole
        bottom.callSpotOrHole()
        return(bottom)

def tickOff(l, pol):
    newl = [ i for i in l if i is not pol.poly ]
    return(newl)

def organizeSpots(multipol):
    #import pdb; pdb.set_trace()
    todo = list(multipol)
    spotList=[]

    while todo:
        done = []
        ## find biggest polygon
        big = findBiggest(todo)
        ## make a SpotHole object for it:
        bigSpot=SpotHole(
                        poly=big,
                        level=0,
                        parentPoly=None,
                        holez=[])

        bigSpot.callSpotOrHole()
        todo = tickOff(todo, bigSpot)
        done.append(bigSpot)
        ## find out what polygons are in it:
        subTodo = [ i for i in todo if bigSpot.poly.contains(i) ]
        ## start classifying these polygons:
        while subTodo:
            bottom = dig2bottom(startPol=big,l=subTodo,level=0,parentSpotHole=None)
            ## knock off this bottom polygon
            todo = tickOff(todo, bottom)
            subTodo = tickOff(subTodo, bottom)
            ## add to done:
            done.append(bottom)

        for nu,hs in enumerate(done):
            if hs.isHole:
                parent, = [ j for j in done if j.poly is hs.parentPoly ]
                parent.holez.append(hs.poly)

        for i in done:
            if i.isSpot: i.makeHolesInPoly()
        localSpotz = [ i.poly for i in done if i.isSpot ]
        spotList.extend(localSpotz)

    spots=sg.MultiPolygon(spotList)
    return(spots)

################## holes in spots #########################

################ main ##########################################


def main(pdir, gjName, meltName, outFileName):
    ## run through digitizing, standardizing
    os.chdir(pdir)
    print(gjName)
    aa = os.listdir()

    _, petalMat, spotsMat = parseDougMatrix(meltName)
    petPolRaw = digitizePols(petalMat) 
    petPol = cleanPetal(petPolRaw, gjName)
    photoBB = list(petPol.bounds)
    spotPolRaw = digitizePols(spotsMat)
    spotPol = cleanIndividualSpotPolys(spotPolRaw, gjName)

    scale, cent = getPetGeoInfo(petPol)
    standPet = stand(petPol, scale, cent)
    if isinstance(spotPol, sg.MultiPolygon): 
        standSpot = [ stand(i, scale, cent) for i in spotPol ]
    elif isinstance(spotPol, sg.Polygon): 
        standSpot = [stand(spotPol, scale, cent)]
    standSpots = shapely.geometry.multipolygon.MultiPolygon(standSpot)
    spotsWithHoles = organizeSpots(standSpots)
    finalSpotsMultiPoly=cleanFinalSpotsMultpoly(spotsWithHoles)
    ## deal with the zones elsewhere
    center, edge, throat, spotEstimates = None, None, None, None
    ## write it out
    geoDict = geojsonIO.writeGeoJ(standPet, finalSpotsMultiPoly, 
                                    center, edge, throat, 
                                    spotEstimates, photoBB, scale)


    with open(outFileName, 'w') as fp:
        json.dump(geoDict, fp)
    return

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

    main(meltParentDir, gjName, meltBaseName, outFileName)
