#!/user/bin/env python3

import os, json 
import numpy as np
import shapely.geometry as sg
import shapely.ops as so
import matplotlib.pyplot as plt
import pandas as pd
from descartes import PolygonPatch
from statistics import mean

####################
## functions here ##
####################

################
## class here ##
################


class Flower():
    def __init__(self):
                self.flowerName = None
                self.geojson = None
                self.petal = None
                self.spots = None
                self.center = None
                self.edge = None
                self.throat = None
                self.biggestSpotArea = None
                self.smallestSpotArea = None
                self.avgSpotSize = None
                self.medSpotSize = None
                self.nuSpots = None
                self.nuSpotsContainedInCenter = None
                self.nuSpotsTouchCenter = None
                self.nuSpotsMostlyInCenter = None
                self.nuSpotCentroidsInCenter = None
                self.avgDist2CenterAllSpots = None
                self.avgDist2CenterCenterSpots = None
                self.propSpotsInCenter = None
                self.centerCoveredbySpots = None
                self.spotOnCentroid = None
                self.nuSpotsContainedInEdge = None
                self.nuSpotsTouchEdge = None
                self.propSpotsInEdge = None
                self.nuSpotsMostlyInEdge = None
                self.edgeCoveredbySpots = None
                self.nuSpotsTouchActualEdge = None
                self.realEdgeSpotted = None
                self.avgDistSpotEdge2Edge = None
                self.avgDistSpotCentroid2Edge = None
                self.throatCoveredbySpots = None
                self.propSpotsInthroat = None
                self.nuSpotsTouchThroat = None
                self.nuSpotsMostlyInThroat = None
                self.nuSpotsTouchCut = None
                self.nuProxSpots = None
                self.propSpotsInProx = None
                self.proxCoveredbySpots = None
                self.nuDistSpots = None
                self.propSpotsInDist = None
                self.distCoveredbySpots = None
                self.nuQuadISpots = None
                self.propSpotsInQuadI = None
                self.quadICoveredbySpots = None
                self.nuQuadIISpots = None
                self.propSpotsInQuadII = None
                self.quadIICoveredbySpots = None
                self.nuQuadIIISpots = None
                self.quadIIISpotsInQuadIII = None
                self.quadIIICoveredbySpots = None
                self.nuQuadIVSpots = None
                self.propSpotsInQuadIV = None
                self.quadIVCoveredbySpots = None
    def parseGeoJson(self, geoj):
        with open(geoj) as gjf:
            aa = json.load(gjf)
            listP = (aa['features'])
            try:
                petalGJ = [ i for i in listP if i['properties']['id'] == 'Petal' ][0]['geometry']
                self.petal = sg.shape(petalGJ)
            except:
                self.petal = sg.polygon.Polygon()
            try:
                spotsGJ = [ i for i in listP if i['properties']['id'] == 'Spots' ][0]['geometry']
                self.spots= sg.shape(spotsGJ)
            except:
                self.spots = sg.polygon.Polygon()
            try:
                centerGJ = [ i for i in listP if i['properties']['id'] == 'Center' ][0]['geometry']
                self.center = sg.shape(centerGJ)
            except:
                self.center = sg.polygon.Polygon()
            try:
                edgeGJ = [ i for i in listP if i['properties']['id'] == 'Edge' ][0]['geometry']
                self.edge = sg.shape(edgeGJ)
            except:
                self.edge = sg.polygon.Polygon()
            try:
                throatGJ = [ i for i in listP if i['properties']['id'] == 'Throat' ][0]['geometry']
                self.throat = sg.shape(throatGJ)
            except:
                self.throat = sg.polygon.Polygon()
    ## function to clean (multi)polygons if self-intersecting 
    def cleanPolys(self, poly):
        if poly.is_valid:
            print('Polygon is ok! Returning it as is.')
            return(poly)
        elif not poly.is_valid:
            polyBuff = poly.buffer(0.0)
            print('Polygon is not valid...buffering...')
        if not polyBuff.is_valid:
            print('Unable to clean ' + flowerName + ' Still invalid. Returning empty polygon.')
            return(sg.polygon.Polygon())
            print('Returning shiny new (multi)polygon.')
            return(polyBuff)
    ############ stats ##############################
    def find_generalStats(self):
        try:
            biggestSpotArea = max([ i.area for i in self.spots ])
        except:
            print('unable to calulate biggestSpotArea')
            biggestSpotArea = None
        try:
            smallestSpotArea = min([ i.area for i in self.spots ])
        except:
            print('unable to calulate smallestSpotArea')
            smallestSpotArea = None
        try:
            avgSpotSize = mean([ i.area for i in self.spots ])
        except:
            print('unable to calulate avgSpotSize')
            avgSpotSize = None
        try:
            medSpotSize = np.median([ i.area for i in self.spots ])
        except:
            print('unable to calulate medSpotSize')
            medSpotSize = None
        try:
            nuSpots = len([ i.area for i in self.spots ])
        except:
            print('unable to calulate nuSpots')
            nuSpots = None
        return(biggestSpotArea,
                smallestSpotArea,
                avgSpotSize,
                medSpotSize,
                nuSpots,
                )
    def find_CenterStats(self):
        try:
            nuSpotsContainedInCenter = sum([ i.within(self.center) for i in self.spots ])
        except:
            print('unable to calulate nuSpotsContainedInCenter')
            nuSpotsContainedInCenter = None
        return(nuSpotsContainedInCenter,
                )
    ############### fillOut columns #############
    def fillColumns(self):
        (self.biggestSpotArea,
        self.smallestSpotArea,
        self.avgSpotSize,
        self.medSpotSize,
        self.nuSpots,
            ) = self.find_generalStats()
        (self.nuSpotsContainedInCenter,
            ) = self.find_CenterStats()
    ############### plotting ###################
    def plotOne(self, poly, l=2, a=1.0, col='yellow'):
        fig = plt.figure()
        ax1 = plt.axes()
        ax1.set_xlim(min(poly.exterior.xy[0]), max(poly.exterior.xy[0]))
        ax1.set_ylim(min(poly.exterior.xy[1]), max(poly.exterior.xy[1]))
        ax1.set_aspect('equal')
        ax1.add_patch(PolygonPatch(poly,
                      fc=col, ec='black',
                      linewidth=l, alpha=a))
    def addOne(self, poly, l=2, a=1.0, col='red'):
        ax1 = plt.axes()
        ax1.add_patch(PolygonPatch(poly,
                      fc=col, ec='black',
                      linewidth=l, alpha=a))




if __name__ == '__main__':



###############

plt.ion()

aa = Flower()
aa.geojson="/home/daniel/Documents/mimulusSpeckling/make_polygons/polygons/P297F2/right/P297F2_right_polys.geojson"
aa.parseGeoJson(aa.geojson)

aa.avgSpotSize
aa.nuSpots
aa.nuSpotsContainedInCenter

aa.fillColumns()
aa.avgSpotSize
aa.nuSpots
aa.nuSpotsContainedInCenter

aa.plotOne(aa.petal)
[ aa.addOne(i) for i in aa.spots ]
aa.addOne(aa.center, a=0.3, col='orange')

