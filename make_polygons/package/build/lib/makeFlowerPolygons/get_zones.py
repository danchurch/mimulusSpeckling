#!/usr/bin/env python3

import matplotlib
matplotlib.use('TkAgg')
import argparse, os, json, shapely
import makeFlowerPolygons.geojsonIO as gj
import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry as sg
import shapely.affinity as sa
import shapely.errors
from skimage import measure
from descartes import PolygonPatch

def findCenter(standPol, percent):
    ## generate margin/center
    center = standPol
    rad = 0
    while center.area > percent:
        center = standPol.buffer(rad)
        rad -= .001
    cent = sg.polygon.Polygon(center.exterior.coords)
    return(cent)

def cleanPoly(pol):
    try:
        assert isinstance(pol, sg.Polygon)
        pol = pol.buffer(0)
        return(pol)
    except AssertionError:
        print('not a polygon')
        return


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


## define our zones
def findEdgeThroat(petal, center, simp=0.5):
    #simp=0.5
    ## generate margin/center
    petal = cleanPoly(petal)
    center = cleanPoly(center)
    marg = sg.polygon.Polygon(
            petal.exterior,
            holes = [center.exterior.coords])
    ## break up margin into edge and throat:
    simPol = marg.simplify(simp)
    ## get array of x,y coords separated
    simPolA = np.array(simPol.exterior.xy).transpose()
    ## sort by y coords:
    simPolAsorted = simPolA[simPolA[:,1].argsort()[::-1]]
    leftSide=simPolAsorted[simPolAsorted[:,0] < 0]
    upperleft=leftSide[0,:]
    rightSide=simPolAsorted[simPolAsorted[:,0] > 0]
    upperright=rightSide[0,:]
    simPolB = np.array(simPol.interiors[0].xy).transpose()
    simPolBsorted = simPolB[simPolB[:,1].argsort()[::-1]]
    leftSide=simPolBsorted[simPolBsorted[:,0] < 0]
    lowerleft=leftSide[0,:]
    rightSide=simPolBsorted[simPolBsorted[:,0] > 0]
    lowerright=rightSide[0,:]
    corners = np.stack((upperleft, upperright,lowerright,lowerleft))
    tRapPoly = cleanPoly(sg.polygon.Polygon(corners))
    try:
        tBuff = tRapPoly.buffer(0.1)
        tBuff = cleanPoly(tBuff)
        noTrap = marg.difference(tRapPoly)
        notInTrap = [ i for i in noTrap if i.within(tBuff) ]
        mpNotInTrap = sg.multipolygon.MultiPolygon(notInTrap)
        margInTrap = tRapPoly.intersection(marg)
        throatRaw = margInTrap.union(mpNotInTrap )
        throat = cleanCollections(throatRaw)
        edgeRaw = marg.difference(throat)
        edge = cleanCollections(edgeRaw)
    except:
        print ("Zones failed...")
        edge, throat = None, None
    finally:
        return(edge, throat)

def main(geojson, centerSize, outFileName):
    ## parse the geojson
    (petal,spots,center,
    edge,throat, spotEstimates, 
    photoBB, scalingFactor) = gj.parseGeoJson(geojson)

    center = findCenter(petal, centerSize)
    edge, throat = findEdgeThroat(petal, center, simp=0.5)


    ## write it back out to geojson 
    featC = gj.writeGeoJ(petal,spots,center,
                         edge,throat, spotEstimates,
                         photoBB, scalingFactor)


    with open(outFileName, 'w') as fp:
        json.dump(featC, fp)

###### Throat - underdevelopment ###################################


if __name__ == "__main__":

    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('geojson', 
                help=("""Name of the geojson file to which you want to\
                        assign zones. """))
    parser.add_argument('centerSize', 
                help=("""give the proportion of the middle of the flower \
                       you would like to call Center Zone, from 0.01 \
                       to 0.99."""),
                type=float)
    parser.add_argument('-o', '--out', 
                help=("Name for outfile. If none given, modified in place."),
                type=str,
                default=None)
#    parser.add_argument("-s", "--simp", 
#                help=("""How much simplification to inflict on the petal 
#                       polygons to find zones. A good start might be 0.05
#                       (the default). This is not used right now, as the 
#                        zone calling is under development, only the center 
#                        polygon is stable."""),
#                default=0.05,
#                type=float)

    args = parser.parse_args()
    geojson=args.geojson
    centerSize=args.centerSize
    if args.out is not None:
        outFileName = args.out
    else:
        outFileName = args.geojson

    main(geojson, centerSize, outFileName)


