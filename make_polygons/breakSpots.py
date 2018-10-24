#!/usr/bin/env python3

import FlowerPetal
import os, copy, json, argparse
import matplotlib.backend_bases
from matplotlib import pyplot as plt
from shapely import geometry as sg
from descartes import PolygonPatch

############ Picker ##################
class PolyPicker:
    def __init__(self, flowerPetal):
        plt.gcf().suptitle("Pick a spot to edit.")
        self.fig = plt.gcf()
        self.axes = plt.gca()
        self.cidPick = plt.gcf().canvas.mpl_connect('pick_event', self)
        self.cidEnter = plt.gcf().canvas.mpl_connect('key_press_event', self)
        self.flowerPetal = flowerPetal
        self.spot = None
        self.spotConfirmed = False
        self.otherSpots = []
        self.x = None
        self.y = None
    def __call__(self, event):
        plt.ion()
        if event.name == 'pick_event':
            self.x = event.mouseevent.xdata
            self.y = event.mouseevent.ydata
            self.spotConfirmed = False
            self.fig.suptitle("")
            aa=self.axes.get_xlim(); bb=self.axes.get_ylim()
            self.axes.cla()
            self.fig.suptitle("Press enter to confirm spot.")
            self.axes.add_patch(PolygonPatch(self.flowerPetal.petal,
                          fc='yellow', ec='black',
                          linewidth=2, alpha=1.0))
            self.axes.set_xlim(aa); self.axes.set_ylim(bb)
            pt=sg.point.Point([self.x, self.y])
            self.otherSpots = [ i for i in list(self.flowerPetal.spots) if not i.contains(pt) ]
            self.spot = [ i for i in list(self.flowerPetal.spots) if i.contains(pt) ][0]
            for i in self.otherSpots:
                    self.axes.add_patch(PolygonPatch(i,
                                  fc='red', ec='black',
                                  picker=True,
                                  linewidth=2, alpha=1.0))
            self.axes.add_patch(PolygonPatch(self.spot,
                          fc='green', ec='black',
                          picker=True,
                          linewidth=2, alpha=1.0))
        elif event.name == 'key_press_event' and event.key == 'enter': 
            try:
                assert(self.spot is not None)
                self.spotConfirmed = True
                self.fig.canvas.mpl_disconnect(self.cidPick)
                self.fig.canvas.mpl_disconnect(self.cidEnter)
                drawGap = DrawGap(self.flowerPetal, self.spot)  
                self.fig.suptitle("Spot picked...break it up!")
            except AssertionError as err:
                self.fig.suptitle("No spot picked? press escape "
                                + "to leave without editing.")
                plt.ioff()
                return
############ Picker ##################

############ drawGap ##################
class DrawGap:
    def __init__(self, flowerPetal, spot):
        plt.gcf().suptitle("Draw where you want to break spot")
        self.event = None
        self.fig = plt.gcf()
        self.axes = plt.gca()
        self.flowerPetal = flowerPetal
        self.spot = spot
        self.gap = sg.polygon.Polygon()
        self.xs = []
        self.ys = []
        self.mouseCid = self.fig.canvas.mpl_connect('button_press_event', self)
        self.keyCid = self.fig.canvas.mpl_connect('key_press_event', self)
    def addPoint(self):
        aa=self.axes.get_xlim(); bb=self.axes.get_ylim()
        self.axes.plot(self.event.xdata, 
                        self.event.ydata, 
                        marker='o', 
                        markersize=3, 
                        color="black")
        self.axes.set_xlim(aa); self.axes.set_ylim(bb)
        self.xs.append(self.event.xdata)
        self.ys.append(self.event.ydata)
    def drawPol(self):
        try:
            self.gap = sg.polygon.Polygon(list(zip(self.xs, self.ys)))
            aa=self.axes.get_xlim(); bb=self.axes.get_ylim()
            self.axes.cla()
            self.axes.set_xlim(aa); self.axes.set_ylim(bb)
            self.axes.add_patch(PolygonPatch(self.flowerPetal.petal,
                          fc='yellow', ec='black',
                          linewidth=2, alpha=1.0))
            self.axes.add_patch(PolygonPatch(self.spot,
                          fc='red', ec='black',
                          linewidth=2, alpha=1.0))
            self.axes.add_patch(PolygonPatch(self.gap,
                          fc='yellow', ec='black',
                          linewidth=1, alpha=1.0))
            return
        except ValueError:
            return
    def __call__(self, event):
        plt.ion()
        self.event = event
        if plt.get_current_fig_manager().toolbar.mode != '': return
        elif event.name == 'button_press_event':
            if event.inaxes!=self.axes: return
            elif event.button==1:
                self.addPoint()
                self.drawPol()
                plt.ioff()
                return
            elif event.button in {2,3}:
                self.xs.pop()
                self.ys.pop()
                self.drawPol()
                plt.ioff()
                self.fig.ioff()
                return
        elif event.name == 'key_press_event' and event.key == 'enter': 
            self.fig.suptitle('Done breaking spot.')
            self.fig.canvas.mpl_disconnect(self.mouseCid)
            self.fig.canvas.mpl_disconnect(self.keyCid)
            breakSpot = BreakSpot(self.flowerPetal,self.spot, self.gap)
        plt.ioff()
        return
############ drawGap ##################

############ breakSpots ##################

class BreakSpot:
    def __init__(self, flowerPetal, oldSpot, gap):
        plt.gcf().suptitle("Spots split! Do another?")
        self.flowerPetal = flowerPetal
        self.oldSpot = oldSpot
        self.gap = gap
        self.fig = plt.gcf()
        self.ax = plt.gca()
        self.newSpots = self.oldSpot.difference(self.gap)
        lsc = list(self.flowerPetal.spots)
        lsc.remove(oldSpot) 
        try:
            nls = lsc + list(self.newSpots)
        except TypeError as err:
            lsc.append(self.newSpots)
            nls = lsc
        self.flowerPetal.spots = sg.multipolygon.MultiPolygon(nls)
        aa=self.ax.get_xlim(); bb=self.ax.get_ylim()
        self.ax.cla()
        self.ax.set_xlim(aa); self.ax.set_ylim(bb)
        self.ax.add_patch(PolygonPatch(self.flowerPetal.petal,
                      fc='yellow', ec='black',
                      picker=None,
                      linewidth=2, alpha=1.0))
        self.ax.add_patch(PolygonPatch(self.flowerPetal.spots,
                      fc='red', ec='black',
                      picker=True,
                      linewidth=2, alpha=1.0))
        self.keyCid = self.fig.canvas.mpl_connect('key_press_event', self)
    def __call__(self,event):
        plt.ion()
        if event.key in {'y','Y'}:
            self.fig.canvas.mpl_disconnect(self.keyCid)
            polyPicker = PolyPicker(self.flowerPetal)
        if event.key in {'n','N'}:
            plt.gcf().suptitle("Spot editing completed.")
            self.fig.canvas.mpl_disconnect(self.keyCid)
            plt.close()
            return
 
############ breakSpots ##################

if __name__ == '__main__':

    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('geoJ',
                help=('The geojson file of the petal.'),
                type=str)
    parser.add_argument('--outFileName','-o', 
                help=('place to put edited geojson. '
                      'If none, geojson will overwrite. '
                      'Use quotes.'),
                default=None, type=str)
    args = parser.parse_args()

                
    ## load flower geojson and plot cartoon of flower:
    fl = FlowerPetal.FlowerPetal()
    fl.geojson = args.geoJ
    fl.parseGeoJson()
    fl.cleanFlowerPetal()
    plt.ion()
    fl.plotOne(fl.petal)
    fl.addOne(fl.spots, pick=True)

    ok = input('Spots okay? (y/n): ') 
    plt.ioff()

    if ok == 'n':
        print("Pick a spot to edit.")
        ## pick it
        polyPicker = PolyPicker(fl)
    elif ok == 'y': quit()

    plt.ioff()
    plt.show()
    ## the blocking by the plot is needed, to keep 
    ## the script from ending before data is collected. 

    ## save new spots:
    fl.saveOut(args.outFileName)


