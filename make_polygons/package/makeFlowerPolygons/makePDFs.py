#!/usr/bin/env python3

import matplotlib
matplotlib.use('TkAgg')
import os, json, pathlib, argparse
import numpy as np
from makeFlowerPolygons import geojsonIO 
from makeFlowerPolygons.get_spots import parseDougMatrix 
import shapely.geometry as sg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from descartes import PolygonPatch

def plotNoZone(petalPoly, spotsPoly, x, y):
    alp=1.0
    l=2
    ax1 = plt.subplot2grid((4, 3), (x, y), colspan=1)
    ax1.set_aspect('equal')
    ax1.set_xlim(min(petalPoly.exterior.xy[0]), max(petalPoly.exterior.xy[0]))
    ax1.set_ylim(min(petalPoly.exterior.xy[1]), max(petalPoly.exterior.xy[1]))
    ax1.add_patch(PolygonPatch(petalPoly,
                  fc='yellow', ec='black',
                  linewidth=l, alpha=alp))
    ## if spots aren't empty.... 
    try:
        ax1.add_patch(PolygonPatch(spotsPoly,
                      fc='red', ec='black',
                      linewidth=l, alpha=alp))
    except: 
        ax1.set_xlabel('No spots detected')

def plotYesZone (petalPoly, spotsPoly, centerPoly, edgePoly, throatPoly, x ,y):
    alp=0.3
    l=2
    ax1 = plt.subplot2grid((4, 3), (x, y), colspan=1)
    ax1.set_xlim(min(petalPoly.exterior.xy[0]), max(petalPoly.exterior.xy[0]))
    ax1.set_ylim(min(petalPoly.exterior.xy[1]), max(petalPoly.exterior.xy[1]))
    ax1.set_aspect('equal')
    ax1.add_patch(PolygonPatch(petalPoly,
                  fc='yellow', ec='black',
                  linewidth=l, alpha=1.0))
    try:
        ax1.add_patch(PolygonPatch(spotsPoly,
                      fc='red', ec='black',
                      linewidth=l, alpha=1.0))
    except: 
        ax1.set_xlabel('No spots detected')
    try:
        ax1.add_patch(PolygonPatch(centerPoly,
                      fc='white', ec='black',
                      linewidth=l, alpha=alp))
    except: 
        ax1.set_xlabel('No center detected')
    try:
        ax1.add_patch(PolygonPatch(edgePoly,
                      fc='white', ec='black',
                      linewidth=l, alpha=alp))
        ax1.add_patch(PolygonPatch(throatPoly,
                      fc='white', ec='black',
                      linewidth=l, alpha=alp))
    except:
        ax1.set_xlabel('throat and edges failed')


def plotRow1(jpgs, flower):
    """ our first row is a plot using one of these jpegs:"""
    pJpgs = pathlib.Path(jpgs)
    jpg = [ i for i in os.listdir(pJpgs) if flower in i and ".JPG" in i][0]
    fJpg = pJpgs / jpg 
    ax1 = plt.subplot2grid((4,3), (0,0), colspan=3)
    img=mpimg.imread(fJpg)
    ax1.imshow(img)
    plt.gcf().suptitle(flower, fontsize=12)

def plotRow2(wd, flower):
    """ our second row is doug's pixel info, peeled apart"""
    pWD=pathlib.Path(wd)
    counter = 0 ## for keeping track of the 6 plots, second row
    try:
        assert flower in list(os.walk(pWD))[0][1], "Is this flower in your working directory?"
        flowerHome = pWD / flower
        for n,j in enumerate(['left','mid','right']):
            meltcsv = [ i for i in os.listdir(flowerHome / j) if "melted.csv" in i][0]
            meltCSV = flowerHome / j / meltcsv
            photoBB, petalMat, spotsMat = parseDougMatrix(meltCSV)
            bb = list(zip(*photoBB))
            lowerLeft = [ min(i)-2 for i in bb ]
            upperRight = [ max(i)+2 for i in bb ]
            ## plot these two rasters, petal outline and spots
            petalOutline = petalMat[lowerLeft[0]:upperRight[0],lowerLeft[1]:upperRight[1]]
            spotsOutline = spotsMat[lowerLeft[0]:upperRight[0],lowerLeft[1]:upperRight[1]]
            #return(photoBB, lowerLeft, upperRight,petalMat, spotsMat,petalOutline, spotsOutline)
            ax = plt.subplot2grid((4,6), (1, counter))
            ax.imshow(petalOutline, cmap='gray')
            counter += 1
            ax = plt.subplot2grid((4,6), (1, counter))
            ax.imshow(spotsOutline, cmap='gray')
            counter += 1
    except AssertionError as err:
        print (err)


def plotRow3(wd, flower):
    ## row 3 plot petal and spot geojsons if we have them. 
    pWD = pathlib.Path(wd, flower)
    for n,petal in enumerate(['left','mid','right']):
        geoJ = [ i for i in os.listdir(pWD / petal) if "geojson" in i ][0]
        (petalPoly,spotsPoly,
                _,_,_,_,_,_) = geojsonIO.parseGeoJson(pWD / petal / geoJ)
        try:
            plotNoZone(petalPoly, spotsPoly, 2, n)
        except: 
            ax=plt.subplot2grid((4,3),(2,n)) ## blank

def plotRow4(wd, flower):
    pWD = pathlib.Path(wd, flower)
    for n,petal in enumerate(['left','mid','right']):
        geoJ = [ i for i in os.listdir(pWD / petal) if "geojson" in i ][0]
        (petalPoly,spotsPoly,
         centerPoly,edgePoly,throatPoly,
                      _,_,_) = geojsonIO.parseGeoJson(pWD / petal / geoJ)
        try:
            plotYesZone (petalPoly,spotsPoly,centerPoly,edgePoly,throatPoly,3,n)
        except: 
            ax=plt.subplot2grid((4,3),(3,n)) ## blank


def main(flower, wd, jpgs, outDir):
    plotRow1(jpgs, flower)
    plotRow2(wd, flower)
    plotRow3(wd, flower)
    plotRow4(wd, flower)
    outPDF=str(pathlib.Path(outDir + "/" + flower + ".pdf"))
    plt.savefig(outPDF)

if __name__ == "__main__":

    ## arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument('flowerName',
                help=("""Give the name of the flower. In our project, this
                        is generally in form of "P---F-" """),
                default=None)
    parser.add_argument('workingDirectory',
                help=("""Give the location of the folder containing 
                         the various flower directories. 
                       """))
    parser.add_argument('jpgDirectory',
                help=("""Give the location of the cropped and rotated JPG files
                        of the flower."""),
                default=None)
    parser.add_argument('--outputDirectory','-o',
                help=("""Give the name of the directory where you would like to 
                        store finished pdf files."""),
                default=None)

    args = parser.parse_args()
    flower = args.flowerName
    wd = args.workingDirectory
    jpgs = args.jpgDirectory
    if args.outputDirectory: 
        outDir = args.outputDirectory
    else: outDir = wd + "/" + flower


    main(flower, wd, jpgs, outDir)
 



