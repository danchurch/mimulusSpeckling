#!/usr/bin/env python3

"""A new spot breaker module, that doesn't work on a spot basis,
but simply introduces yellow space into the petal, clipping polygons
where necessary.
"""
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
    print('Zoop!')
    plt.ion()
    bb = list(zip(*photoBB))
    lowerLeft = [ min(i)-2 for i in bb ]
    upperRight = [ max(i)+2 for i in bb ]
    img=mpimg.imread(jpeg)
    justPetal = img[lowerLeft[1]:upperRight[1],lowerLeft[0]:upperRight[0]]
    jpegFig, jpegAx = plt.subplots(1,1)
    jpegAx.imshow(justPetal, origin='lower')
    jpegFig.canvas.manager.window.wm_geometry("+900+0")
    jpegFig.set_size_inches([6,3], forward = True)


def saveOut ( petal,spots,center,edge,throat,
                spotEstimates, photoBB,
                scalingFactor, outFileName ):
    print('Save new spots?')
    newOK=choice()
    if newOK == 'y':
        ## write it out
        print('Saving as ' + outFileName)
        featC = geojsonIO.writeGeoJ(petal,spots,center,edge,throat,
                    spotEstimates, photoBB, scalingFactor)
        with open(outFileName, 'w') as fp:
            json.dump(featC, fp)
        quit()
    if newOK == 'n':
        print('Not saving...')
        quit()

def breakup(petal, spots):
    newSpots=spots
    plt.ion()
    geojsonIO.plotOne(petal)
    geojsonIO.addOne(newSpots)
    plt.gcf().canvas.manager.window.wm_geometry("+900+350")
    firstView=plt.gcf()
    print("Look okay?")
    ok=choice()
    if ok=='y': return(newSpots)
    if ok=='n': 
        plt.close(firstView)
        geojsonIO.plotOne(petal)
        geojsonIO.addOne(newSpots)
        plt.gcf().canvas.manager.window.wm_geometry("+900+350")
        print('Draw in some yellow space.')
        breakPatch=DrawYellow(petal, newSpots, fig=plt.gcf(),)
        finished()
        newSpots=newSpots.difference(sg.Polygon(breakPatch.xyVerts))
        if isinstance(newSpots, sg.polygon.Polygon):
            newSpots = sg.multipolygon.MultiPolygon([newSpots])
        redraw(petal, newSpots)
        newSpots=breakup(petal, newSpots)
        return(newSpots)

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

    (petal,spots,center,edge,throat,
        spotEstimates, photoBB,
                    scalingFactor) = geojsonIO.parseGeoJson(args.geoJ)

    showJpeg(args.jpeg, photoBB)

    newSpots=breakup(petal,spots)

    saveOut ( petal, newSpots, center, edge, throat,
                spotEstimates, photoBB,
                scalingFactor, outFileName )

