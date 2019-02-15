#!/usr/bin/env python3

"""A new spot breaker module, that doesn't work on a spot basis,
but simply introduces yellow space into the petal, clipping polygons
where necessary.
"""
import matplotlib as mp
mp.use("TkAgg")
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
        self.petal=spots
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
        self.redraw()
        self.drawVerts()
        self.drawPol()

    def redraw(self):
        aa=self.ax.get_xlim(); bb=self.ax.get_ylim()
        self.ax.cla()
        self.ax.set_xlim(aa); self.ax.set_ylim(bb)
        geojsonIO.addOne(petal, col='yellow')
        geojsonIO.addOne(spots, col='red')

    def drawVerts(self):
        self.ax.plot(self.xVerts,
                        self.yVerts,
                        marker='o',
                        markersize=3,
                        color="black")

    def drawPol(self):
        try:
            poly=sg.Polygon(self.xyVerts)
            geojsonIO.addOne(poly, a=0.8, col='yellow')
        except ValueError:
            return


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

  
def breakup(petal, spots):
    plt.ion()
    geojsonIO.plotOne(petal)
    geojsonIO.addOne(spots)
    print("Look okay?")
    ok=choice()
    if ok=='y': return(spots)
    if ok=='n': 
        geojsonIO.plotOne(petal)
        geojsonIO.addOne(spots)
        print('Draw in some yellow space.')
        breakPatch=DrawYellow(petal, spots, fig=plt.gcf(),)
        finished()
        spots=spots.difference(sg.Polygon(breakPatch.xyVerts))
        breakPatch.redraw()
        breakup(petal, spots)

#######################################################

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


    newSpots=breakup(petal,spots)

    geojsonIO.plotOne(petal)
    geojsonIO.addOne(newSpots)
    finished()

#plot petal
#plot spots
#draw poly
#take difference 
#update
#keepgoing?


