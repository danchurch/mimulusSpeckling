#!/usr/bin/env python3

import argparse, os, json, shapely
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

def parseGeoJson(geojson):
    with open(geojson) as gjf:
        aa = json.load(gjf)
        listP = (aa['features'])
        try:
            petalGJ = [ i for i in listP if i['properties']['id'] == 'Petal' ][0]['geometry']
            petal = sg.shape(petalGJ)
        except:
            petal = sg.polygon.Polygon()
        try:
            spotsGJ = [ i for i in listP if i['properties']['id'] == 'Spots' ][0]['geometry']
            spots= sg.shape(spotsGJ)
        except:
            spots = sg.polygon.Polygon()
        try:
            centerGJ = [ i for i in listP if i['properties']['id'] == 'Center' ][0]['geometry']
            center = sg.shape(centerGJ)
        except:
            center = sg.polygon.Polygon()
        try:
            edgeGJ = [ i for i in listP if i['properties']['id'] == 'Edge' ][0]['geometry']
            edge = sg.shape(edgeGJ)
        except:
            edge = sg.polygon.Polygon()
        try:
            throatGJ = [ i for i in listP if i['properties']['id'] == 'Throat' ][0]['geometry']
            throat = sg.shape(throatGJ)
        except:
            throat = sg.polygon.Polygon()
    return(petal,spots,center,edge,throat)



####### Throat - underdevelopment ###################################
#def redrawThroat(marg, standPet):
#    def onclick(event):
#        print('Point at x=%d y=%d' %(event.x, event.y))
#        xc, yc = event.xdata, event.ydata
#        global points
#        points.append([xc,yc])
#
#    print('Okay, click the four points pf the throat.')
#    print("Start with one corner and click counterclockwise.")
#    points=[]
#    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)
#    plt.gcf().canvas.mpl_disconnect(cid)
#    print('made it here')
#    print(cid)
#    polA = sg.polygon.Polygon(points)
#    return(polA)
#
#
#
#    """ often the zone-finding algorithm failes, so we need to help it """
#
#
### define our zones
#def findZones(standPol, percent, simp=0.05):
#
#    ## generate margin/center
#    center = standPol
#    rad = 0
#    while center.area > percent:
#        center = standPol.buffer(rad)
#        rad -= .001
#    marg = sg.polygon.Polygon(
#            standPol.exterior,
#            holes = [center.exterior.coords])
#
#    ## break up margin into edge and throat:
#    simPol = marg.simplify(simp)
#    simPolA = np.array(simPol.exterior.xy).transpose()
#    simPolAsorted = simPolA[simPolA[:,1].argsort()[::-1]]
#    outCorners = simPolAsorted[0:2]
#    simPolB = np.array(simPol.interiors[0].xy).transpose()
#    simPolBsorted = simPolB[simPolB[:,1].argsort()[::-1]]
#    inCorners = simPolBsorted[0:2,]
#    inCorners = np.flipud(inCorners)
#    tRap = np.concatenate((outCorners,inCorners))
#    tRapPoly = sg.polygon.Polygon(tRap)
#
#    ## polygon calculations start here, risky:
#    try:
#        tBuff = tRapPoly.buffer(0.1)
#        noTrap = marg.difference(tRapPoly)
#        notInTrap = [ i for i in noTrap if i.within(tBuff) ]
#        mpNotInTrap = sg.multipolygon.MultiPolygon(notInTrap)
#        margInTrap = tRapPoly.intersection(marg)
#        throatRaw = margInTrap.union(mpNotInTrap )
#        throat = cleanCollections(throatRaw)
#        edgeRaw = marg.difference(throat)
#        edge = cleanCollections(edgeRaw)
#   ## bring up a plot of the zones:
#   plt.ion()
#   plotOne(standPet)
#   addOne(standSpots)
#   addOne(edge, col='white', a=0.5)
#   addOne(throat, col='purple', a=0.5)
#   ## ask user if the digitization worked:
#   sanCheck=input('Is this throat polygon OK?')
#        assert (sanCheck in ['y','Y','yes']), "Not a good polygon? Time to redraw."
#    except AssertionError as err:
#        print(err)
#       ## time to get interactive
#   if sanCheck not in ['y','Y','yes']:
#           polA=redrawThroat(marg,standPet)
#           addOne(polA, col='orange', a=1)
#    finally:
#        plt.close()
#        return(center, edge, throat)
#    except:
#        print ("Zones failed...")
#        center, edge, throat = None, None, None
#    finally:
#        return(center, edge, throat)
####### Throat - underdevelopment ###################################


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

    if args.out is not None:
        outFileName = args.out
    else:
        outFileName = args.geojson

    ## parse the geojson
    petal,spots,center,edge,throat = parseGeoJson(args.geojson)

    print(args.geojson)
#    center, edge, throat = findZones(standPet, args.centerSize, args.simp)
    edge, throat = None, None  
    center = findCenter(petal, args.centerSize)

    ## outputs 

    ## write it back out to geojson (need to write a function for this...)
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

    ## write it out
    with open(outFileName, 'w') as fp:
        json.dump(featC, fp)

#####################

