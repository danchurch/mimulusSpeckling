#!/usr/bin/env python3

import os, json 
import numpy as np
import shapely.geometry as sg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from descartes import PolygonPatch

def parseGeoj(file):
    with open(file) as gjf:
        aa = json.load(gjf)
        listP = (aa['features'])
        try:
            petalGJ = [ i for i in listP if i['properties']['id'] == 'Petal' ][0]['geometry'] 
            petalPoly = sg.shape(petalGJ)
        except:
            petalPoly = sg.polygon.Polygon()
        try:
            spotsGJ = [ i for i in listP if i['properties']['id'] == 'Spots' ][0]['geometry'] 
            spotsPoly = sg.shape(spotsGJ)
        except:
            spotsPoly = sg.polygon.Polygon()
        try:
            centerGJ = [ i for i in listP if i['properties']['id'] == 'Center' ][0]['geometry'] 
            centerPoly = sg.shape(centerGJ)
        except:
            centerPoly = sg.polygon.Polygon()
        try:
            edgeGJ = [ i for i in listP if i['properties']['id'] == 'Edge' ][0]['geometry'] 
            edgePoly = sg.shape(edgeGJ)
        except:
            edgePoly = sg.polygon.Polygon()
        try:
            throatGJ = [ i for i in listP if i['properties']['id'] == 'Throat' ][0]['geometry'] 
            throatPoly = sg.shape(throatGJ)
        except:
            throatPoly = sg.polygon.Polygon()
    return(petalPoly, spotsPoly, centerPoly, edgePoly, throatPoly)

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
    ax1.add_patch(PolygonPatch(centerPoly,
                  fc='white', ec='black',
                  linewidth=l, alpha=alp))
    ax1.add_patch(PolygonPatch(edgePoly,
                  fc='white', ec='black',
                  linewidth=l, alpha=alp))
    try:
        ax1.add_patch(PolygonPatch(throatPoly,
                      fc='white', ec='black',
                      linewidth=l, alpha=alp))
    except:
        ax1.set_xlabel('throat and edges failed')

if __name__ == "__main__":

    ## make these into command line args?
    polDir='/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/polygons'
    dougDir='/home/daniel/Documents/cooley_lab/mimulusSpeckling/dougRaster/Rotated_and_Cropped'
    targetDir='/home/daniel/Documents/cooley_lab/bigPDF'

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
        os.chdir(polDir + "/" + flowerName) ## go to flower directory
        counter = 0 ## for keeping track of the 6 plots, second row
        for n,j in enumerate(['left', 'mid', 'right']):
            os.chdir(j)
            print("We are on " + j)
            spotsCSV = [ i for i in os.listdir() if 'spots' in i ][0]
            petalCSV = [ i for i in os.listdir() if 'petal' in i ][0]
            ## get rasters as CSVs
            petalMat = np.genfromtxt(petalCSV, delimiter=',')
            spotsMat = np.genfromtxt(spotsCSV, delimiter=',')
            ## plot these two rasters, petal outline and spots
            ax = plt.subplot2grid((4,6), (1, counter))
            ax.imshow(petalMat, cmap='gray')
            counter += 1
            ax = plt.subplot2grid((4,6), (1, counter))
            ax.imshow(spotsMat, cmap='gray')
            counter += 1
            ## get geojsons, turn them into polygons
            try: 
                geoj = [ i for i in os.listdir() if 'geojson' in i ][0]
                print('GeoJson found at: ' + os.getcwd())
                petalPoly, spotsPoly, centerPoly, edgePoly, throatPoly = parseGeoj(geoj)
            except: 
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
        os.chdir(dougDir)

