#!/usr/bin/env python3

import matplotlib
matplotlib.use('TkAgg')
import os, json, argparse, re, pickle
from makeFlowerPolygons import geojsonIO
import numpy as np
import shapely.geometry as sg
import shapely.ops as so
import matplotlib.pyplot as plt
import pandas as pd
from descartes import PolygonPatch
from statistics import mean

################
## class here ##
################

class FlowerPetal():
    def __init__(self):
                self.plantName = None
                self.flowerName = None
                self.petalName = None
                self.geojson = None
                self.petal = None
                self.spots = None
                self.center = None
                self.edge = None
                self.throat = None
                self.spotEstimates = None
                self.photoBB = None
                self.scalingFactor = None
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
                self.propSpotsInThroat = None
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
                self.propSpotsInQuadIII = None
                self.quadIIICoveredbySpots = None
                self.nuQuadIVSpots = None
                self.propSpotsInQuadIV = None
                self.quadIVCoveredbySpots = None

    def parseGeoJson(self):
                (self.petal, self.spots, self.center, 
                self.edge, self.throat, self.spotEstimates,
                self.photoBB, self.scalingFactor) = geojsonIO.parseGeoJson(self.geojson) 

    ## function to clean (multi)polygons if self-intersecting 
    def cleanPolys(self, poly):
        if poly.is_valid:
            print('Polygon is ok! Returning it as is.')
            return(poly)
        elif not poly.is_valid:
            polyBuff = poly.buffer(0.0)
            print('Polygon is not valid...buffering...')
        if not polyBuff.is_valid:
            print('Unable to clean ' + self.geojson + ' Still invalid. Returning empty polygon.')
            return(sg.polygon.Polygon())
        else:
            print('Returning shiny new (multi)polygon.')
            return(polyBuff)

    ## use poly cleaning function to make a flower cleaning function
    def cleanFlowerPetal(self):
        assert isinstance(self, FlowerPetal), "Not flower"
        print('Checking petal')
        self.petal = self.cleanPolys(self.petal)
        ## check to see if this made a multipolygon:
        if type(self.petal) == sg.multipolygon.MultiPolygon:
            print('This made a multipolygon for your petal.')
            areas = [ i.area for i in self.petal ]
            self.petal = [ i for i in self.petal if i.area == max(areas) ][0]
            print('Picking largest polygon for petal.')
        print('Checking spots')
        self.spots = self.cleanPolys(self.spots)
        ## we need our spots to be multipolygons, to make this class:
        if type(self.spots) == sg.polygon.Polygon:
            self.spots = sg.multipolygon.MultiPolygon([self.spots])
        print('Checking center')
        self.center = self.cleanPolys(self.center)
        print('Checking edge')
        self.edge = self.cleanPolys(self.edge)
        print('Checking throat')
        self.throat = self.cleanPolys(self.throat)


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
            centerCoveredbySpots = None
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
            throatfrags = self.petal.exterior.difference(self.throat.buffer(0.01))
            if len(throatfrags) > 1:
                petalRim = so.linemerge(throatfrags)
            else: petalRim = throatfrags
            avgDistSpotEdge2Edge = mean([ petalRim.distance(i) for i in self.spots ])
        except:
            print('unable to calulate avgDistSpotEdge2Edge')
            avgDistSpotEdge2Edge = None
        try:
            avgDistSpotCentroid2Edge = mean([ petalRim.distance(i.centroid) for i in self.spots ])
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
    def find_ThroatStats(self):
        try:
            partSpotsInThroat = [ i.intersection(self.throat) for i in self.spots if i.intersects(self.throat) ]
            listz = [ list(i) if type(i) == sg.multipolygon.MultiPolygon else [i] for i in partSpotsInThroat ]
            unNest = sum(listz, []) 
            partSpotsInThroat =  sg.multipolygon.MultiPolygon(unNest)
            throatCoveredbySpots = partSpotsInThroat.area / self.throat.area
        except:
            print('unable to calulate throatCoveredbySpots')
            throatCoveredbySpots = None
        try:
            propSpotsInThroat = partSpotsInThroat.area / self.spots.area
        except:
            print('unable to calulate propSpotsInThroat')
            propSpotsInThroat = None
        try:
            nuSpotsTouchThroat = sum([ i.intersects(self.throat) for i in self.spots ])
        except:
            print('unable to calulate nuSpotsTouchThroat')
            nuSpotsTouchThroat = None
        try:
            nuSpotsMostlyInThroat = len([ i for i in self.spots if (i.intersection(self.throat).area / i.area > 0.5) ])
        except:
            print('unable to calulate nuSpotsMostlyInThroat')
            nuSpotsMostlyInThroat = None
        try:
            nuSpotsTouchCut = len([ i for i in partSpotsInThroat if i.intersects(self.petal.exterior) ])
        except:
            print('unable to calulate nuSpotsTouchCut')
            nuSpotsTouchCut = None
        return(throatCoveredbySpots,
               propSpotsInThroat, 
               nuSpotsTouchThroat, 
               nuSpotsMostlyInThroat, 
               nuSpotsTouchCut, 
                )
    def find_ProxStats(self):
        try:
            ## make a box
            proxBox=sg.box(-1,0,1,1)
            ## get the area of our petal in this box:
            petalProx = self.petal.intersection(proxBox)
            ## get the area of spots that fall into this
            spottedSurfaceProx = self.spots.intersection(petalProx)
            ## the outputs
            nuProxSpots = sum([ i.intersects(petalProx) for i in self.spots ])
            propSpotsInProx = spottedSurfaceProx.area / self.spots.area
            proxCoveredbySpots = spottedSurfaceProx.area / petalProx.area
        except:
            print('unable to calulate ProxStats')
            nuProxSpots = None
            propSpotsInProx = None
            proxCoveredbySpots = None
        return(nuProxSpots, 
                propSpotsInProx,
                proxCoveredbySpots,
                )
    def find_DistalStats(self):
        try:
            ## make a box
            distBox=sg.box(-1,-1,1,0)
            ## get the area of our petal in this box:
            petalDist = self.petal.intersection(distBox)
            ## get the area of spots that fall into this
            spottedSurfaceDist = self.spots.intersection(petalDist)
            ## the outputs
            nuDistSpots = sum([ i.intersects(petalDist) for i in self.spots ])
            propSpotsInDist = spottedSurfaceDist.area / self.spots.area
            distCoveredbySpots = spottedSurfaceDist.area / petalDist.area
        except:
            print('unable to calulate DistalStats')
            nuDistSpots = None
            propSpotsInDist = None
            distCoveredbySpots = None
        return(nuDistSpots, 
                propSpotsInDist,
                distCoveredbySpots,
                )
    def find_QuadIStats(self):
        try:
            quadIbox=sg.box(0,0,1,1)
            petalQuadI = self.petal.intersection(quadIbox)
            spottedSurfaceQuadI = self.spots.intersection(petalQuadI)
            nuQuadISpots = len([ i for i in self.spots if i.centroid.x > 0 and i.centroid.y > 0 ])
            propSpotsInQuadI = spottedSurfaceQuadI.area / self.spots.area
            quadICoveredbySpots = spottedSurfaceQuadI.area / petalQuadI.area
        except:
            print('unable to calulate QuadIStats')
            (nuQuadISpots,
            propSpotsInQuadI,
            quadICoveredbySpots) = None, None, None
        return(
            nuQuadISpots,
            propSpotsInQuadI,
            quadICoveredbySpots,
                )
    def find_QuadIIStats(self):
        try:
            quadIIbox=sg.box(-1,0,0,1)
            petalQuadII = self.petal.intersection(quadIIbox)
            spottedSurfaceQuadII = self.spots.intersection(petalQuadII)
            nuQuadIISpots = len([ i for i in self.spots if i.centroid.x < 0 and i.centroid.y > 0 ])
            propSpotsInQuadII = spottedSurfaceQuadII.area / self.spots.area
            quadIICoveredbySpots = spottedSurfaceQuadII.area / petalQuadII.area
        except:
            print('unable to calulate QuadIIStats')
            (nuQuadIISpots,
            propSpotsInQuadII,
            quadIICoveredbySpots) = None, None, None
        return(
            nuQuadIISpots,
            propSpotsInQuadII,
            quadIICoveredbySpots,
                )
    def find_QuadIIIStats(self):
        try:
            quadIIIbox=sg.box(-1,-1,0,0)
            petalQuadIII = self.petal.intersection(quadIIIbox)
            spottedSurfaceQuadIII = self.spots.intersection(petalQuadIII)
            nuQuadIIISpots = len([ i for i in self.spots if i.centroid.x < 0 and i.centroid.y < 0 ])
            propSpotsInQuadIII = spottedSurfaceQuadIII.area / self.spots.area
            quadIIICoveredbySpots = spottedSurfaceQuadIII.area / petalQuadIII.area
        except:
            print('unable to calulate QuadIIIStats')
            (nuQuadIIISpots,
            propSpotsInQuadIII,
            quadIIICoveredbySpots) = None, None, None
        return(
            nuQuadIIISpots,
            propSpotsInQuadIII,
            quadIIICoveredbySpots,
                )
    def find_QuadIVStats(self):
        try:
            quadIVbox=sg.box(0,-1,1,0)
            petalQuadIV = self.petal.intersection(quadIVbox)
            spottedSurfaceQuadIV = self.spots.intersection(petalQuadIV)
            nuQuadIVSpots = len([ i for i in self.spots if i.centroid.x > 0 and i.centroid.y < 0 ])
            propSpotsInQuadIV = spottedSurfaceQuadIV.area / self.spots.area
            quadIVCoveredbySpots = spottedSurfaceQuadIV.area / petalQuadIV.area
        except:
            print('unable to calulate QuadIVStats')
            (nuQuadIVSpots,
            propSpotsInQuadIV,
            quadIVCoveredbySpots) = None, None, None
        return(
            nuQuadIVSpots,
            propSpotsInQuadIV,
            quadIVCoveredbySpots,
                )
    ############### fillOut columns #############
    def fillColumns(self):
        try:
            assert(len(self.spots) > 0)
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
            (self.throatCoveredbySpots,
                self.propSpotsInThroat,
                self.nuSpotsTouchThroat,
                self.nuSpotsMostlyInThroat,
                self.nuSpotsTouchCut,
                ) = self.find_ThroatStats()
            (self.nuProxSpots,
                self.propSpotsInProx,
                self.proxCoveredbySpots,
                ) = self.find_ProxStats()
            (self.nuDistSpots,
                self.propSpotsInDist,
                self.distCoveredbySpots,
                ) = self.find_DistalStats()
            (self.nuQuadISpots,
                self.propSpotsInQuadI,
                self.quadICoveredbySpots,
                ) = self.find_QuadIStats()
            (self.nuQuadIISpots,
                self.propSpotsInQuadII,
                self.quadIICoveredbySpots,
                ) = self.find_QuadIIStats()
            (self.nuQuadIIISpots,
                self.propSpotsInQuadIII,
                self.quadIIICoveredbySpots,
                ) = self.find_QuadIIIStats()
            (self.nuQuadIVSpots,
                self.propSpotsInQuadIV,
                self.quadIVCoveredbySpots,
                ) = self.find_QuadIVStats()
        except AssertionError:
            print('No spots detected. Most statistics will be None or 0.')
            self.biggestSpotArea = None
            self.smallestSpotArea = None
            self.avgSpotSize = None
            self.medSpotSize = None
            self.nuSpots = 0
            self.nuSpotsContainedInCenter = 0
            self.nuSpotsTouchCenter = 0
            self.nuSpotsMostlyInCenter = 0
            self.nuSpotCentroidsInCenter = 0
            self.avgDist2CenterAllSpots = None
            self.avgDist2CenterCenterSpots = None
            self.propSpotsInCenter = None
            self.centerCoveredbySpots = 0
            self.spotOnCentroid = False
            self.nuSpotsContainedInEdge = 0
            self.nuSpotsTouchEdge = 0
            self.propSpotsInEdge = None
            self.nuSpotsMostlyInEdge = 0
            self.edgeCoveredbySpots = 0
            self.nuSpotsTouchActualEdge = 0
            self.realEdgeSpotted = 0
            self.avgDistSpotEdge2Edge = None
            self.avgDistSpotCentroid2Edge = None
            self.throatCoveredbySpots = 0
            self.propSpotsInThroat = None
            self.nuSpotsTouchThroat = 0
            self.nuSpotsMostlyInThroat = 0
            self.nuSpotsTouchCut = 0
            self.nuProxSpots = 0
            self.propSpotsInProx = None
            self.proxCoveredbySpots = 0
            self.nuDistSpots = 0
            self.propSpotsInDist = None
            self.distCoveredbySpots = 0
            self.nuQuadISpots = 0
            self.propSpotsInQuadI = None
            self.quadICoveredbySpots = 0
            self.nuQuadIISpots = 0
            self.propSpotsInQuadII = None
            self.quadIICoveredbySpots = 0
            self.nuQuadIIISpots = 0
            self.propSpotsInQuadIII = None
            self.quadIIICoveredbySpots = 0
            self.nuQuadIVSpots = 0
            self.propSpotsInQuadIV = None
            self.quadIVCoveredbySpots = 0

    ############### plotting ###################
    def plotOne(self=None, poly=None, l=2, a=1.0, col='yellow', pick=None):
        print('oops. Use the new geojsonIO plotOne function instead.')

    def addOne(self=None, poly=None, l=2, a=1.0, col='red', pick=None):
        print('oops. Use the new geojsonIO addOne function instead.')

#### end of flowerPetal class #####


if __name__ == '__main__':

    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('geojFolder',
                help=('The folder of geojson files.'))
    parser.add_argument('dataframe',
                help=('The desired name of the output, '
                        'formatted as a .csv file and'
                        ' a pickled pandas dataframe, '
                        'saved in the geojFolder.'
                        '(Put it in quotes)'))
    args = parser.parse_args()

    ## make our FlowerPetal objects
    os.chdir(args.geojFolder)
    petals = os.listdir()
    petals.sort()
    flowerpetalList = []
    for i,plantFlowerPetal in enumerate(petals):
        print("file is {}.".format(plantFlowerPetal))
        fl = FlowerPetal()
        fl.plantName = re.sub(r"(P.*)F.*",r"\1",plantFlowerPetal)
        fl.flowerName = re.sub(r"P.*(F\d).*",r"\1",plantFlowerPetal)
        fl.petalName = re.sub(".*(left|mid|right).*",r"\1",plantFlowerPetal)
        fl.geojson = plantFlowerPetal
        fl.parseGeoJson()
        fl.cleanFlowerPetal()
        fl.fillColumns()
        row = vars(fl)
        flowerpetalList.append(row)

    ## make the all-petals dataframe dataframe:
    allPetalDf = pd.DataFrame(flowerpetalList)

    ## get our plant, flower and petal name forward:
    allPetalDf = allPetalDf.set_index('petalName').reset_index()
    allPetalDf = allPetalDf.set_index('flowerName').reset_index()
    allPetalDf = allPetalDf.set_index('plantName').reset_index()

    ## get rid of geometries:
    del allPetalDf['petal']
    del allPetalDf['spots']
    del allPetalDf['center']
    del allPetalDf['edge']
    del allPetalDf['throat']

## save it as a csv and pickle it:
    allPetalDf.to_csv(args.dataframe + ".csv")
    pickle.dump(allPetalDf, open(args.dataframe + ".p", "wb"))
