#!/usr/bin/env python3

########################################################
## for local development, use this:                   ##
########################################################
#import sys
#sys.path.append("/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/package/makeFlowerPolygons")
#import geojsonIO
########################################################


import matplotlib as mp
mp.use("TkAgg")
import matplotlib.image as mpimg
import os, argparse, json
import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry as sg
import makeFlowerPolygons.geojsonIO as geojsonIO
import makeFlowerPolygons.get_zones as gz
import matplotlib.pyplot as plt

def plotFlowerZones(petal,spots,center,edge,throat):
    geojsonIO.plotOne(petal)
    geojsonIO.addOne(spots)
    geojsonIO.addOne(edge, col='white', a=0.5)
    geojsonIO.addOne(throat, col='white', a=0.5)
    if mp.get_backend() == 'TkAgg':
        plt.gcf().canvas.manager.window.wm_geometry("+900+350")
    return(plt.gcf(),plt.gca())

def showJpeg(jpeg, photoBB):
    plt.ion()
    img=mpimg.imread(jpeg)
    photoBB = [ int(i) for i in photoBB ]
    justPetal = img[photoBB[1]:photoBB[3],photoBB[0]:photoBB[2]]
    jpegFig, jpegAx = plt.subplots(1,1)
    jpegAx.imshow(justPetal, origin='lower')
    jpegFig.canvas.manager.window.wm_geometry("+900+0")
    jpegFig.set_size_inches([6,3], forward = True)
    return(jpegFig, jpegAx)


def choice():
    try:
        aa = input("(y/n): ")
        assert aa in {"y","n"}
    except AssertionError as err:
        print('Enter "y" or "n"')
        aa = choice()
    finally:
        return(aa)

def finished():
    f=input("Finished? (y): ")
    try:
        assert f == "y"
        return
    except AssertionError:
        print("Enter 'y' when finished.")
        finished()


def valNum():
    try:
        aa = input("(Enter a numeric value): ")
        aa = float(aa)
    except ValueError as err:
        print('Did you enter a number?')
        aa = valNum()
    finally:
        return(aa)

def getNewEdgeThroat(pol, petal, center):
    aa = pol.intersection(petal)
    newThroat = aa.difference(center)
    marg = petal.difference(center)
    newEdge = marg.difference(newThroat)
    return(newEdge, newThroat)

def saveOut ( petal,spots,center,edge,throat, 
                spotEstimates, photoBB, 
                scalingFactor, outFileName):
    fig,ax = plotFlowerZones(petal,spots,center,edge,throat)
    print('Save new zones?')
    newOK=choice()
    if newOK == 'y':
        ## write it out
        print('Saving as ' + outFileName)
        featC = geojsonIO.writeGeoJ(petal,spots,center,edge,throat, 
                    spotEstimates, photoBB, scalingFactor)
        with open(outFileName, 'w') as fp:
            json.dump(featC, fp)
    if newOK == 'n': 
        print('Not saving...')
        print('Back to editing')
    plt.close(fig)
    return (newOK)

class PolyMaker:
    def __init__(self, petal, center):
        geojsonIO.plotOne(petal)
        geojsonIO.addOne(center, col='white', a=0.5)
        self.fig = plt.gcf()
        self.ax = plt.gca()
        newYLim = [ i * 1.1 for i in list(self.ax.get_ylim()) ]
        newXLim = [ i * 1.1 for i in list(self.ax.get_xlim()) ]
        self.ax.set_ylim(newYLim)
        self.ax.set_xlim(newXLim)
        if mp.get_backend() == 'TkAgg':
            self.fig.canvas.manager.window.wm_geometry("+900+350")
        self.petal = petal
        self.center = center
        self.verts = []
        self.poly = None
        self.mouseCID = self.fig.canvas.mpl_connect('button_press_event', self)
    def __call__(self,event):
        if plt.get_current_fig_manager().toolbar.mode != '': return
        self.event = event
        if event.name == "button_press_event":
            if event.inaxes!=self.ax: return
            if event.button == 1:
                self.verts.append((event.xdata,event.ydata))
            elif event.button != 1:
                try:
                    self.verts.pop()
                except IndexError as err:
                    #print(err)
                    return
            aa = np.array(self.verts).transpose()
            geojsonIO.clearOne()
            geojsonIO.addOne(self.petal, col='yellow')
            geojsonIO.addOne(self.center, col='white', a=0.5)
            ## plot verts
            try:
                assert(len(self.verts) > 0)
                self.ax.plot(aa[0],aa[1],'o', color='red')
            except (IndexError, AssertionError) as err:
                return
            ## plot poly
            try:
                self.poly = sg.Polygon(self.verts)
                assert(self.poly.is_valid)
                geojsonIO.clearOne()
                geojsonIO.addOne(self.petal, col='yellow')
                geojsonIO.addOne(self.center, col='white', a=0.5)
                self.ax.plot(aa[0],aa[1],'o', color='red')
                geojsonIO.addOne(sg.Polygon(self.verts), a= 0.3)
            except (ValueError): return
            except (AssertionError):
                print('Invalid polygon. New spots'
                        ' will fail unless you fix this.')
                return

def main(geojson, outFileName, jpeg=None):
    (petal,spots,
    center,edge,throat, 
    spotEstimates, photoBB, 
    scalingFactor) = geojsonIO.parseGeoJson(geojson)
    try:
        assert(center)
    except AssertionError:
        print ('Center zone not found. Have you run this geojson'
        ' through our automated zone calling steps?')
        return
    plt.ion()
    jpegFig, jpegAx = showJpeg(jpeg, photoBB)
    petalFig, petalAx = plotFlowerZones(petal,spots,center,edge,throat)
    print("Here's the flower and zones. Look ok? ", end = "")
    ZonesOK=choice()

    if ZonesOK == 'y': 
        print("Okay! moving on...")
        plt.close('all')
        return

    if ZonesOK == 'n': 
        plt.close(petalFig)
        pm = PolyMaker(petal, center)
        whileDrawing(pm, 
            petal,spots,center,edge,throat, 
            spotEstimates, photoBB, 
            scalingFactor, geojson, outFileName)

def whileDrawing (polymaker, 
            petal,spots,center,edge,throat, 
            spotEstimates, photoBB, 
            scalingFactor, geojson, outFileName):
    """ 
    this should keep the zone editing alive as long as the user needs.
    """ 
    print("Draw polygon to define the left"
            " and right boundaries of throat.")
    print('Press "y" when finished.')
    finished()
    newEdge, newThroat = getNewEdgeThroat(polymaker.poly, petal, center)
    saveYN=saveOut( petal,spots,center,newEdge, newThroat, 
            spotEstimates, photoBB, 
            scalingFactor, outFileName)
    if saveYN=='y':
        polymaker.fig.canvas.mpl_disconnect(polymaker.mouseCID)
        plt.close('all')
        return
    elif saveYN=='n':
        print('Back to editing zones.')
        whileDrawing(polymaker, 
            petal,spots,center,newEdge,newThroat, 
            spotEstimates, photoBB, 
            scalingFactor, geojson, outFileName)
        return



########################################

if __name__ == '__main__':

    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('geojson',
                help=("""Name of the geojson file to which you want to\
                        assign zones. """))
    parser.add_argument('-j', '--jpeg',
                help=("The jpeg associated with this flower."),
                type=str,
                default=None)
    parser.add_argument('-o', '--out',
                help=("Name for outfile. If none given, modified in place."),
                type=str,
                default=None)

    args = parser.parse_args()

    if args.out is not None:
        outFileName = args.out
    else:
        outFileName = args.geojson

    main(args.geojson, outFileName, jpeg=args.jpeg )
