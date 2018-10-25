#!/usr/bin/env python3

import FlowerPetal
import os, copy, json, argparse
import matplotlib.backend_bases
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from shapely import geometry as sg
from descartes import PolygonPatch

############ Picker ##################
class PolyPicker:
    def __init__(self, flowerPetal,fig, axs):
        self.fig = fig
        self.axs = axs
        self.cidPick = self.fig.canvas.mpl_connect('pick_event', self)
        self.cidEnter = self.fig.canvas.mpl_connect('key_press_event', self)
        self.flowerPetal = flowerPetal
        self.spot = None
        self.spotConfirmed = False
        self.otherSpots = []
        self.x = None
        self.y = None
        self.fig.suptitle("Pick a spot to edit.")
    def __call__(self, event):
        plt.ion()
        if event.name == 'pick_event':
            self.x = event.mouseevent.xdata
            self.y = event.mouseevent.ydata
            self.spotConfirmed = False
            self.fig.suptitle("")
            aa=self.axs.get_xlim(); bb=self.axs.get_ylim()
            self.axs.cla()
            self.fig.suptitle("Press enter to confirm spot.")
            self.axs.add_patch(PolygonPatch(self.flowerPetal.petal,
                          fc='yellow', ec='black',
                          linewidth=2, alpha=1.0))
            self.axs.set_xlim(aa); self.axs.set_ylim(bb)
            pt=sg.point.Point([self.x, self.y])
            self.otherSpots = [ i for i in list(self.flowerPetal.spots) if not i.contains(pt) ]
            self.spot = [ i for i in list(self.flowerPetal.spots) if i.contains(pt) ][0]
            for i in self.otherSpots:
                    self.axs.add_patch(PolygonPatch(i,
                                  fc='red', ec='black',
                                  picker=True,
                                  linewidth=2, alpha=1.0))
            self.axs.add_patch(PolygonPatch(self.spot,
                          fc='green', ec='black',
                          picker=True,
                          linewidth=2, alpha=1.0))
        elif event.name == 'key_press_event' and event.key == 'enter': 
            try:
                assert(self.spot is not None)
                self.spotConfirmed = True
                self.fig.canvas.mpl_disconnect(self.cidPick)
                self.fig.canvas.mpl_disconnect(self.cidEnter)
                drawGap = DrawGap(flowerPetal=self.flowerPetal, 
                                    spot=self.spot,   
                                    fig=self.fig,   
                                    axs=self.axs )  
                self.fig.suptitle("Spot picked...break it up!")
            except AssertionError as err:
                self.fig.suptitle("No spot picked? press escape "
                                + "to leave without editing.")
                plt.ioff()
                return
        elif event.name == 'key_press_event' and event.key == 'escape': 
            self.fig.canvas.mpl_disconnect(self.cidPick)
            self.fig.canvas.mpl_disconnect(self.cidEnter)
            plt.close()
            return
############ Picker ##################

############ drawGap ##################
class DrawGap:
    def __init__(self, flowerPetal, spot, fig, axs):
        self.fig = fig
        self.axs = axs
        self.event = None
        self.flowerPetal = flowerPetal
        self.spot = spot
        self.gap = sg.polygon.Polygon()
        self.xs = []
        self.ys = []
        self.fig.suptitle("Draw where you want to break spot")
        self.mouseCid = self.fig.canvas.mpl_connect('button_press_event', self)
        self.keyCid = self.fig.canvas.mpl_connect('key_press_event', self)
    def addPoint(self):
        aa=self.axs.get_xlim(); bb=self.axs.get_ylim()
        self.axs.plot(self.event.xdata, 
                        self.event.ydata, 
                        marker='o', 
                        markersize=3, 
                        color="black")
        self.axs.set_xlim(aa); self.axs.set_ylim(bb)
        self.xs.append(self.event.xdata)
        self.ys.append(self.event.ydata)
    def drawPol(self):
        try:
            self.gap = sg.polygon.Polygon(list(zip(self.xs, self.ys)))
            aa=self.axs.get_xlim(); bb=self.axs.get_ylim()
            self.axs.cla()
            self.axs.set_xlim(aa); self.axs.set_ylim(bb)
            self.axs.add_patch(PolygonPatch(self.flowerPetal.petal,
                          fc='yellow', ec='black',
                          linewidth=2, alpha=1.0))
            self.axs.add_patch(PolygonPatch(self.spot,
                          fc='red', ec='black',
                          linewidth=2, alpha=1.0))
            self.axs.add_patch(PolygonPatch(self.gap,
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
            if event.inaxes!=self.axs: return
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
            breakSpot = BreakSpot(flowerPetal=self.flowerPetal, 
                                  oldSpot=self.spot, 
                                  gap=self.gap, 
                                  fig=self.fig, 
                                  axs=self.axs)
        plt.ioff()
        return
############ drawGap ##################

############ breakSpots ##################

class BreakSpot:
    def __init__(self, flowerPetal, oldSpot, gap, fig, axs):
        self.fig = fig
        self.flowerPetal = flowerPetal
        self.oldSpot = oldSpot
        self.gap = gap
        self.axs = axs
        self.newSpots = self.oldSpot.difference(self.gap)
        self.fig.suptitle("Spots split! Do another?")
        lsc = list(self.flowerPetal.spots)
        lsc.remove(oldSpot) 
        try:
            nls = lsc + list(self.newSpots)
        except TypeError as err:
            lsc.append(self.newSpots)
            nls = lsc
        self.flowerPetal.spots = sg.multipolygon.MultiPolygon(nls)
        aa=self.axs.get_xlim(); bb=self.axs.get_ylim()
        self.axs.cla()
        self.axs.set_xlim(aa); self.axs.set_ylim(bb)
        self.axs.add_patch(PolygonPatch(self.flowerPetal.petal,
                      fc='yellow', ec='black',
                      picker=None,
                      linewidth=2, alpha=1.0))
        self.axs.add_patch(PolygonPatch(self.flowerPetal.spots,
                      fc='red', ec='black',
                      picker=True,
                      linewidth=2, alpha=1.0))
        self.keyCid = self.fig.canvas.mpl_connect('key_press_event', self)
    def __call__(self,event):
        plt.ion()
        if event.key in {'y','Y'}:
            self.fig.canvas.mpl_disconnect(self.keyCid)
            polyPicker = PolyPicker(fl, fig=flf, axs=fla)
        if event.key in {'n','N'}:
            plt.gcf().suptitle("Spot editing completed.")
            print("Spot editing completed.")
            self.fig.canvas.mpl_disconnect(self.keyCid)
            plt.close('all')
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
    parser.add_argument('--jpeg','-j', 
                help=('Original jpeg image of flower. '
                      'Use entire path. Use quotes.'),
                default=None, type=str)
    args = parser.parse_args()

    ## load the original jpeg:

    plt.ion()
    jpegFig=plt.figure()
    img=mpimg.imread(args.jpeg)
    plt.imshow(img, origin='lower')
                
    ## load flower geojson and plot cartoon of flower:
    fl = FlowerPetal.FlowerPetal()
    fl.geojson = args.geoJ
    fl.parseGeoJson()
    fl.cleanFlowerPetal()
    fl.plotOne(fl.petal)
    fl.addOne(fl.spots, pick=True)
    ## hold onto these for the other objects
    flf = plt.gcf()
    fla = flf.gca()

    ok = input('Spots okay? (y/n): ') 
    plt.ioff()

    if ok == 'n':
        print("Pick a spot to edit.")
        ## pick it
        polyPicker = PolyPicker(fl, fig=flf, axs=fla)
    elif ok == 'y': quit()

    plt.ioff()
    plt.show()
    ## the blocking by the plot is needed, to keep 
    ## the script from ending before data is collected. 

    ## save new spots:
    fl.saveOut(outFileName=args.outFileName)
    print('Saving to: ' + args.outFileName)
    print('and done!')

    quit()



