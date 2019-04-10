#!/usr/bin/env python3

"""A new spot breaker module, that doesn't work on a spot basis,
but simply introduces yellow space into the petal, clipping polygons
where necessary.
"""

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
import os, copy, json, argparse
import makeFlowerPolygons.geojsonIO as geojsonIO
from matplotlib import pyplot as plt
from shapely import geometry as sg

class DrawYellow:
    def __init__(self, petal, spots, fig=None, ax=None):
        if fig: self.fig = fig 
        elif not fig: self.fig = plt.gcf() 
        if ax: self.ax = ax 
        elif not ax: self.ax = plt.gca() 
        self.petal=petal
        self.spots=spots
        self.xVerts=[]
        self.yVerts=[]
        self.xyVerts = []
        self.mouseCid = self.fig.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if plt.get_current_fig_manager().toolbar.mode != '': return
        if event.inaxes!=self.ax: return
        self.event = event
        if event.button==1:
            self.xVerts.append(self.event.xdata)
            self.yVerts.append(self.event.ydata)
            self.xyVerts.append((self.event.xdata, self.event.ydata))
        if event.button!=1:
            try:
                del(self.xVerts[-1])
                del(self.yVerts[-1])
                del(self.xyVerts[-1])
            except IndexError:
                return
        redraw(self.petal, self.spots)
        self.drawVerts()
        self.drawPol()

    def drawVerts(self):
        self.ax.plot(self.xVerts,
                        self.yVerts,
                        marker='o',
                        markersize=3,
                        color="black")

    def drawPol(self):
        try:
            poly=sg.Polygon(self.xyVerts)
            assert(poly.is_valid)
            geojsonIO.addOne(poly, a=0.8, col='yellow')
        except ValueError:
            return
        except AssertionError:
            print('Invalid polygon. New spots' 
                    'will fail unless you fix this.')
            return

def redraw(petal, spots):
    aa=plt.gca().get_xlim(); bb=plt.gca().get_ylim()
    plt.gca().cla()
    plt.gca().set_xlim(aa); plt.gca().set_ylim(bb)
    geojsonIO.addOne(petal, col='yellow')
    geojsonIO.addOne(spots, col='red')

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

def saveOut ( petal,spots,center,edge,throat,
                spotEstimates, photoBB,
                scalingFactor, outFileName ):
    print('Save new spots?')
    geojsonIO.plotOne(petal)
    geojsonIO.addOne(spots)
    plt.gcf().canvas.manager.window.wm_geometry("+900+350")
    newOK=choice()
    if newOK == 'y':
        ## write it out
        print('Saving as ' + outFileName)
        featC = geojsonIO.writeGeoJ(petal,spots,center,edge,throat,
                    spotEstimates, photoBB, scalingFactor)
        with open(outFileName, 'w') as fp:
            json.dump(featC, fp)
        plt.close('all')
        return
    if newOK == 'n':
        print('Not saving...')
        return

def breakup(petal, spots):
    geojsonIO.plotOne(petal)
    geojsonIO.addOne(spots)
    fig=plt.gcf()
    fig.canvas.manager.window.wm_geometry("+900+350")
    print('Draw in some yellow space.')
    breakPatch=DrawYellow(petal, spots, fig=fig)
    finished()
    newSpots=spots.difference(sg.Polygon(breakPatch.xyVerts))
    if isinstance(newSpots, sg.polygon.Polygon):
        newSpots = sg.multipolygon.MultiPolygon([newSpots])
    breakPatch.fig.canvas.mpl_disconnect(breakPatch.mouseCid)
    del(breakPatch)
    redraw(petal, newSpots)
    print("Break up more spots?")
    more=choice()
    plt.close(fig)
    print(more)
    if more=='n': 
        return(newSpots)
    elif more=='y': 
        newSpots=breakup(petal, newSpots)
    return(newSpots)

def main(geoJ,jpeg,outFileName):
    (petal,spots,center,edge,throat,
        spotEstimates, photoBB,
                    scalingFactor) = geojsonIO.parseGeoJson(geoJ)
    plt.ion()
    geojsonIO.plotOne(petal)
    geojsonIO.addOne(spots)
    firstView=plt.gcf()
    firstView.canvas.manager.window.wm_geometry("+900+350")
    jpegFig, jpegAx = showJpeg(jpeg, photoBB)
    jpegFig.canvas.manager.window.wm_geometry("+900+0")
    print("Look okay?")
    ok=choice()
    plt.close(firstView)
    if ok=='y': 
        return
    if ok=='n': 
        showJpeg(jpeg, photoBB)
        newSpots=breakup(petal,spots)
        print(type(newSpots))
        saveOut ( petal, newSpots, center, edge, throat,
                    spotEstimates, photoBB,
                    scalingFactor, outFileName )

######################################################

if __name__ == '__main__':
    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('geoJ',
                help=('The geojson file of the petal.'),
                type=str)
    parser.add_argument('jpeg',
                help=('jpeg image of flower. '
                      'Use entire path.'),
                type=str)
    parser.add_argument('--outFileName','-o',
                help=('place to put edited geojson. '
                      'If none, geojson will overwrite.'),
                default=None, type=str)
    args = parser.parse_args()

    if not args.outFileName:
        outFileName = args.geoJ
    else: outFileName = args.outFileName

    main(args.geoJ,args.jpeg,outFileName)


