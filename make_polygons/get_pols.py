#!/usr/bin/env python3

import argparse, os, pickle
import numpy as np
import matplotlib.pyplot as plt
import shapely.geometry as sg
import shapely.affinity as sa
from skimage import measure

def digitizePols(file):
    ## pad margins of image and get the contour of the petal shape
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
    aa = sg.asPolygon(pet)
    area = aa.area
    scalar = area**(-1/2)
    center = aa.centroid
    centerCoor = (center.x, center.y)
    return(scalar, centerCoor)

def stand(pol, scale, cent):
    aa = sg.asPolygon(pol)
    trans = sa.translate(aa, (-1*cent[0]), (-1*cent[1]))
    scaled = sa.scale(trans, xfact=scale, yfact=scale, origin = (0,0))
    return(scaled)

def findZones(standPol, percent, simp=0.05):
    center = standPol
    rad = 0
    while center.area > percent:
        center = standPol.buffer(rad)
        rad -= .001

    marg = sg.polygon.Polygon(
            standPol.exterior,
            holes = [center.exterior.coords])
    simPol = marg.simplify(simp)
    simPolA = np.array(simPol.exterior.xy).transpose()
    simPolA[:,0].argsort()
    simPolAsorted = simPolA[simPolA[:,1].argsort()[::-1]]
    outCorners = simPolAsorted[0:2]
    simPolB = np.array(simPol.interiors[0].xy).transpose()
    simPolB[:,0].argsort()
    simPolBsorted = simPolB[simPolB[:,1].argsort()[::-1]]
    inCorners = simPolBsorted[0:2,]
    inCorners = np.flipud(inCorners)
    tRap = np.concatenate((outCorners,inCorners))
    tRapPoly = sg.polygon.Polygon(tRap)
    tBuff = tRapPoly.buffer(0.1)
    noTrap = marg.difference(tRapPoly)
    notInTrap = [ i for i in noTrap if i.within(tBuff) ]
    mpNotInTrap = sg.multipolygon.MultiPolygon(notInTrap)
    margInTrap = tRapPoly.intersection(marg)
    throat = margInTrap.union(mpNotInTrap )
    edge = marg.difference(throat)
    return(center, edge, throat)


if __name__ == "__main__":


    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', 
                help=("Name of folder that contains two files:"
                      " that contains grayscale petal outlint and spot "
                        "information in the form of CSVs."))
    parser.add_argument('centerSize', 
                help=("give the proportion of the middle of the flower"
                      " you would like to call Center Zone, from 0.01"
                      " to 0.99."),
                type=float)
    parser.add_argument('destination', 
                help=("Folder where you would like this file."))


    args = parser.parse_args()


    os.chdir(args.folder)
    aa = os.listdir()
    for i in aa:
        if "petal" in i:
            petPol = digitizePols(i)[0] 
        elif "spots" in i:
            spotPol = digitizePols(i)
    scale, cent = getPetGeoInfo(petPol)
    standPet = stand(petPol, scale, cent)
    standSpot = [ stand(i, scale, cent) for i in spotPol ]
    center, edge, throat = findZones(standPet, args.centerSize, 0.07)
    
    polys = {
        'standPet': standPet,
        'standSpot': standSpot,
        'center': center,
        'edge': edge,
        'throat': throat
                }
   
    here = os.getcwd()
    petalName = os.path.basename(here)
    flowerName = os.path.basename(os.path.dirname(here)) 
    outFileName = ( args.destination + "/" 
                    + flowerName + "_" 
                    + petalName 
                    + "_polys.p")

    output = open(outFileName, "wb")



#####################

