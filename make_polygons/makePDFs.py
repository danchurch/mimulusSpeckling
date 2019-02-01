#!/usr/bin/env python3

import os, json, pathlib
import numpy as np
import geojsonIO 
from get_spots import parseDougMatrix as parseDougMatrix
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

def plotRow2(wd, flower):
    """ our second row is doug's pixel info, peeled apart"""
    pWD=pathlib.Path(wd)
    counter = 0 ## for keeping track of the 6 plots, second row
    try:
        assert flower in list(os.walk(pWD))[0][1], "Is this flower in your working directory?"
        flowerHome = pWD / flower
        for n,j in enumerate(list(os.walk(flowerHome))[0][1]):
            meltcsv = [ i for i in os.listdir(flowerHome / j) if "melted.csv" in i][0]
            meltCSV = flowerHome / j / meltcsv
            photoBB, petalMat, spotsMat = parseDougMatrix(meltCSV)
            return(photoBB, petalMat.shape, spotsMat.shape)
            bb = list(zip(*photoBB))
            lowerleft = [ min(i) for i in bb ]
            upperRight = [ max(i) for i in bb ]
            ## plot these two rasters, petal outline and spots
            ax = plt.subplot2grid((4,6), (1, counter))
            ax.imshow(petalMat, cmap='gray')
            counter += 1
            ax = plt.subplot2grid((4,6), (1, counter))
            ax.imshow(spotsMat, cmap='gray')
            counter += 1
    except AssertionError as err:
        print (err)


def plotRow3(wd, flower):
    ## row 3 plot petal and spot geojsons if we have them. 
    pWD = pathlib.Path(wd, flower)
    for n,petal in enumerate(os.listdir(pWD)):
        print(petal)
        geoJ = [ i for i in os.listdir(pWD / petal) if "geojson" in i ][0]
        (petalPoly,spotsPoly,
                _,_,_,_,_,_) = geojsonIO.parseGeoJson(pWD / petal / geoJ)
        try:
            plotNoZone(petalPoly, spotsPoly, 2, n)
        except: 
            ax=plt.subplot2grid((4,3),(2,n)) ## blank

def plotRow4(wd, flower):
    pWD = pathlib.Path(wd, flower)
    for n,petal in enumerate(os.listdir(pWD)):
        print(petal)
        geoJ = [ i for i in os.listdir(pWD / petal) if "geojson" in i ][0]
        (petalPoly,spotsPoly,
         centerPoly,edgePoly,throatPoly,
                      _,_,_) = geojsonIO.parseGeoJson(pWD / petal / geoJ)
        try:
            plotYesZone (petalPoly,spotsPoly,centerPoly,edgePoly,throatPoly,3,n)
        except: 
            ax=plt.subplot2grid((4,3),(3,n)) ## blank


plt.ion()
jpgs='/home/daniel/Documents/cooley_lab/mimulusSpeckling/dougRaster/Rotated_and_Cropped/plate2'
wd='/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/plate2'
flower='P739F1'
petal='mid'

plotRow1(jpgs, flower)

plotRow2(wd, flower)

plotRow3(wd, flower)
plotRow4(wd, flower)


n = 0

## row 3 plot petal and spot geojsons if we have them. 
try:
    plotNoZone(petalPoly, spotsPoly, 2, n)
except: 
    ax=plt.subplot2grid((4,3),(2,n)) ## blank

## row 4 plot these with zones, if we have them:
try:
        plotYesZone(petalPoly, spotsPoly, centerPoly, edgePoly, throatPoly, 3, n)
except: 
    ax=plt.subplot2grid((4,3),(3,n)) ## blank




if __name__ == "__main__":

    
    os.chdir(dougDir)
    aa = os.listdir()
    bb = [ i for i in aa if 'JPG' in i]
    
    for flowerJpg in bb:
        flowerName = flowerJpg[0:-4] ##flower name
        fig = plt.figure()
        fig.suptitle(flowerName, fontsize=12)
        ## our first row is a plot using one of these jpegs:
        imgFullName=(dougDir + '/' + flowerJpg)
        ax1 = plt.subplot2grid((4,3), (0,0), colspan=3)
        img=mpimg.imread(imgFullName)
        ax1.imshow(img)
        ## second row is Doug's rasters
        try:
            os.chdir(polDir + "/" + flowerName) ## go to flower directory
            counter = 0 ## for keeping track of the 6 plots, second row
            for n,j in enumerate(['left', 'mid', 'right']):
                os.chdir(j)
                print("We are on " + flowerName + j)
                meltCSV = [ i for i in os.listdir() if "melted.csv" in i ][0]
                _, petalMat, spotsMat = parseDougMatrix(meltCSV)
                ## get rasters as CSVs
                #petalMat = np.genfromtxt(petalCSV, delimiter=',')
                #spotsMat = np.genfromtxt(spotsCSV, delimiter=',')
                ## plot these two rasters, petal outline and spots
                ax = plt.subplot2grid((4,6), (1, counter))
                ax.imshow(petalMat, cmap='gray')
                counter += 1
                ax = plt.subplot2grid((4,6), (1, counter))
                ax.imshow(spotsMat, cmap='gray')
                counter += 1
                ## get geojsons, turn them into polygons
                try: 
                    ## originally, we used the geojsons in the polygon file tree
                    geoj = [ i for i in os.listdir() if 'geojson' in i ][0]
                    ## to use the working directory for geojsons instead, uncomment:
                    #geoj = [ i for i in os.listdir(workingGeoJDir) if j in i and flowerName in i ][0]
                    #geojFull = (workingGeoJDir + "/" +geoj)
                    #petalPoly, spotsPoly, centerPoly, edgePoly, throatPoly, _,_,_ = geojsonIO.parseGeoJson(geojFull)
                    petalPoly, spotsPoly, centerPoly, edgePoly, throatPoly, _,_,_ = geojsonIO.parseGeoJson(geoj)
                    print('GeoJson found: ' + geoj)
                except (IndexError, OSError, FileNotFoundError): 
                    print('Error - GeoJson not found.')
                ## row 3 plot petal and spot geojsons if we have them. 
                try:
                    plotNoZone(petalPoly, spotsPoly, 2, n)
                except: 
                    ax=plt.subplot2grid((4,3),(2,n)) ## blank
                ## row 4 plot these with zones, if we have them:
                try:
                        plotYesZone(petalPoly, spotsPoly, centerPoly, edgePoly, throatPoly, 3, n)
                except: 
                    ax=plt.subplot2grid((4,3),(3,n)) ## blank
                os.chdir(polDir + "/" + flowerName) ## go back to flower directory
            plt.savefig(targetDir + "/" + flowerName + ".pdf")
            plt.close('all')
        except FileNotFoundError as eror:
            print(eror)
        finally:
            os.chdir(dougDir)



