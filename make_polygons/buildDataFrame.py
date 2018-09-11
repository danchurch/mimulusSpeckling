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

def cleanFlower(flower):
    flower.petal = flower.cleanPolys(flower.petal)
    flower.spots = flower.cleanPolys(flower.spots)
    flower.center = flower.cleanPolys(flower.center)
    flower.edge = flower.cleanPolys(flower.edge)
    flower.throat = flower.cleanPolys(flower.throat)
    return(flower)

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
        else:
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
        try:
            nuSpotsTouchCenter = sum([ i.intersects(self.center) for i in self.spots ])
        except:
            print('unable to calulate nuSpotsTouchCenter')
            nuSpotsTouchCenter = None
        try:
            spotsMostlyInCenter = [ i for i in self.spots if (i.intersection(self.center).area / i.area > 0.5) ]
            nuSpotsMostlyInCenter = len(spotsMostlyInCenter)
        except:
            print('unable to calulate nuSpotsMostlyInCenter')
            nuSpotsMostlyInCenter = None
        try:
            nuSpotCentroidsInCenter = sum([ i.centroid.intersects(self.center) for i in self.spots ] )
        except:
            print('unable to calulate nuSpotCentroidsInCenter')
            nuSpotCentroidsInCenter = None
        try:
            avgDist2CenterAllSpots = mean([ i.centroid.distance(self.center.centroid) for i in self.spots ])
        except:
            print('unable to calulate avgDist2CenterAllSpots')
            avgDist2CenterAllSpots = None
        try:
            spotsMostlyInCenter = [ i for i in self.spots if (i.intersection(self.center).area / i.area > 0.5) ]
            avgDist2CenterCenterSpots = mean([ i.centroid.distance(self.center.centroid) for i in spotsMostlyInCenter ])
        except:
            print('unable to calulate avgDist2CenterCenterSpots')
            avgDist2CenterCenterSpots = None
        try:
            partSpotsInCenter = [ i.intersection(self.center) for i in self.spots if i.intersects(self.center) ]
            ## this makes multipolys often. To handle this...
            ## make a list of lists, even of single polygons
            listz = [ list(i) if type(i) == sg.multipolygon.MultiPolygon else [i] for i in partSpotsInCenter ]
            unNest = sum(listz, []) ## seems to work... not sure why...
            ## bring it back
            partSpotsInCenter = sg.multipolygon.MultiPolygon(unNest)
            propSpotsInCenter = partSpotsInCenter.area / self.spots.area
            centerCoveredbySpots = partSpotsInCenter.area / self.center.area 
        except:
            print('unable to calulate propSpotsInCenter and centerCoveredbySpots')
            propSpotsInCenter = None
        try:
            spotOnCentroid = any([ i.intersects(self.petal.centroid) for i in self.spots ])
        except:
            print('unable to calulate spotOnCentroid')
            spotOnCentroid = None
        return(nuSpotsContainedInCenter,
                nuSpotsTouchCenter,
                nuSpotsMostlyInCenter,
                nuSpotCentroidsInCenter,
                avgDist2CenterAllSpots,
                avgDist2CenterCenterSpots,
                propSpotsInCenter,
                centerCoveredbySpots,
                spotOnCentroid,
                )
    def find_EdgeStats(self):
        try:
            nuSpotsContainedInEdge = sum([ i.within(self.edge) for i in self.spots ])
        except:
            print('unable to calulate nuSpotsContainedInEdge')
            nuSpotsContainedInEdge = None
        try:
            nuSpotsTouchEdge = sum([ i.intersects(self.edge) for i in self.spots ])
        except:
            print('unable to calulate nuSpotsTouchEdge')
            nuSpotsTouchEdge = None
        try:
            partSpotsInEdge = [ i.intersection(self.edge) for i in self.spots if i.intersects(self.edge) ]
            ## make a list of lists, even of single polygons
            listz = [ list(i) if type(i) == sg.multipolygon.MultiPolygon else [i] for i in partSpotsInEdge ]
            unNest = sum(listz, []) ## seems to work... not sure why...
            ## bring it back
            partSpotsInEdge =  sg.multipolygon.MultiPolygon(unNest)
            propSpotsInEdge = partSpotsInEdge.area / self.spots.area 
        except:
            print('unable to calulate propSpotsInEdge')
            propSpotsInEdge = None
        try:
            nuSpotsMostlyInEdge = nuSpotsMostlyInEdge = len([ i for i in self.spots if (i.intersection(self.edge).area / i.area > 0.5) ])
        except:
            print('unable to calulate nuSpotsMostlyInEdge')
            nuSpotsMostlyInEdge = None
        try:
            edgeCoveredbySpots = partSpotsInEdge.area / self.edge.area  
        except:
            print('unable to calulate edgeCoveredbySpots')
            edgeCoveredbySpots = None
        try:
            nuSpotsTouchActualEdge = sum([ i.intersects(self.petal.exterior) for i in partSpotsInEdge ])
        except:
            print('unable to calulate nuSpotsTouchActualEdge')
            nuSpotsTouchActualEdge = None
        try:
            spotEdges = sum([ i.intersection(self.petal.exterior).length for i in partSpotsInEdge ])
            realEdgeSpotted = spotEdges / self.petal.exterior.length 
        except:
            print('unable to calulate realEdgeSpotted')
            realEdgeSpotted = None
        try:
            flowerCut = self.throat.intersection(self.petal.exterior)
            notTube = [ i for i in self.spots if not i.intersects(flowerCut)]
            avgDistSpotEdge2Edge = mean([ self.petal.exterior.distance(i) for i in notTube ])
        except:
            print('unable to calulate avgDistSpotEdge2Edge')
            avgDistSpotEdge2Edge = None
        try:
            avgDistSpotCentroid2Edge = mean([ self.petal.exterior.distance(i.centroid) for i in notTube ])
        except:
            print('unable to calulate avgDistSpotCentroid2Edge')
            avgDistSpotCentroid2Edge = None
        return(nuSpotsContainedInEdge,
                nuSpotsTouchEdge,
                propSpotsInEdge,
                nuSpotsMostlyInEdge,
                edgeCoveredbySpots,
                nuSpotsTouchActualEdge,
                realEdgeSpotted,
                avgDistSpotEdge2Edge,
                avgDistSpotCentroid2Edge,
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
        self.nuSpotsTouchCenter,
        self.nuSpotsMostlyInCenter,
        self.nuSpotCentroidsInCenter,
        self.avgDist2CenterAllSpots,
        self.avgDist2CenterCenterSpots,
        self.propSpotsInCenter,
        self.centerCoveredbySpots,
        self.spotOnCentroid,
            ) = self.find_CenterStats()
        (self.nuSpotsContainedInEdge,
            self.nuSpotsTouchEdge,
            self.propSpotsInEdge,
            self.nuSpotsMostlyInEdge,
            self.edgeCoveredbySpots,
            self.nuSpotsTouchActualEdge,
            self.realEdgeSpotted,
            self.avgDistSpotEdge2Edge,
            self.avgDistSpotCentroid2Edge,
            ) = self.find_EdgeStats()
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
aa = cleanFlower(aa)

aa.avgSpotSize
aa.avgDistSpotEdge2Edge
aa.avgDistSpotCentroid2Edge

aa.fillColumns()

aa.avgSpotSize
aa.avgDistSpotEdge2Edge
aa.avgDistSpotCentroid2Edge


aa.plotOne(aa.petal)
[ aa.addOne(i) for i in aa.spots ]
aa.addOne(aa.center, a=0.3, col='orange')
aa.addOne(aa.throat, a=0.3, col='orange')

