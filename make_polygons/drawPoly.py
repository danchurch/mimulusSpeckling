import FlowerPetal
import os, copy
import matplotlib.backend_bases
from matplotlib import pyplot as plt
from shapely import geometry as sg
from descartes import PolygonPatch

############ Picker ##################
class PolyPicker:
    def __init__(self, flowerPetal):
        self.fig = plt.gcf()
        self.axes = plt.gca()
        self.cidPick = plt.gcf().canvas.mpl_connect('pick_event', self)
        self.cidEnter = plt.gcf().canvas.mpl_connect('key_press_event', self)
        self.flowerPetal = flowerPetal
        self.spot = None
        self.spotPicked = False
        self.noSpot = False
        self.otherSpots = []
        self.x = None
        self.y = None
    def __call__(self, event):
        if event.name == 'pick_event':
            self.x = event.mouseevent.xdata
            self.y = event.mouseevent.ydata
            self.spotPicked = False
            self.fig.suptitle("")
            aa=self.axes.get_xlim(); bb=self.axes.get_ylim()
            self.axes.cla()
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
                if self.spotPicked:
                    self.fig.suptitle("Spot picked...break it up!")
                    self.fig.canvas.mpl_disconnect(self.cidPick)
                    self.fig.canvas.mpl_disconnect(self.cidEnter)
                elif not self.spotPicked:
                    self.fig.suptitle("Spot chosen. Press enter again to confirm")
                    self.spotPicked = True
                    return
            except AssertionError as err:
                if self.noSpot == False: 
                    self.fig.suptitle("No spot chosen. Is this correct? Press \"enter\" again to confirm.")
                    self.noSpot = True 
                elif self.noSpot == True: 
                    self.fig.suptitle("Okay, no spots edited.")
                    self.fig.canvas.mpl_disconnect(self.cidPick)
                    self.fig.canvas.mpl_disconnect(self.cidEnter)
############ Picker ##################

############ drawGap ##################
class drawGap:
    def __init__(self, flowerPetal, spot):
        self.event = None
        self.fig = plt.gcf()
        self.axes = plt.gca()
        self.flowerPetal = flowerPetal
        self.spot = spot
        self.poly = sg.polygon.Polygon()
        self.xs = []
        self.ys = []
        self.mouseCid = self.fig.canvas.mpl_connect('button_press_event', self)
        self.keyCid = self.fig.canvas.mpl_connect('key_press_event', self)
    def addPoint(self):
        aa=self.axes.get_xlim(); bb=self.axes.get_ylim()
        self.axes.plot(self.event.xdata, self.event.ydata, marker='o', markersize=3, color="black")
        self.axes.set_xlim(aa); self.axes.set_ylim(bb)
        self.xs.append(self.event.xdata)
        self.ys.append(self.event.ydata)
    def drawPol(self):
        try:
            self.poly = sg.polygon.Polygon(list(zip(self.xs, self.ys)))
            aa=self.axes.get_xlim(); bb=self.axes.get_ylim()
            self.axes.cla()
            self.axes.set_xlim(aa); self.axes.set_ylim(bb)
            self.axes.add_patch(PolygonPatch(self.flowerPetal.petal,
                          fc='yellow', ec='black',
                          linewidth=2, alpha=1.0))
            self.axes.add_patch(PolygonPatch(self.spot,
                          fc='red', ec='black',
                          linewidth=2, alpha=1.0))
            self.axes.add_patch(PolygonPatch(self.poly,
                          fc='yellow', ec='black',
                          linewidth=1, alpha=1.0))
            return
        except ValueError:
            return
    def __call__(self, event):
        self.event = event
        if plt.get_current_fig_manager().toolbar.mode != '': return
        elif event.name == 'button_press_event':
            if event.inaxes!=self.axes: return
            elif event.button==1:
                self.addPoint()
                self.drawPol()
                return
            elif event.button in {2,3}:
                self.xs.pop()
                self.ys.pop()
                self.drawPol()
                return
        elif event.name == 'key_press_event' and event.key == 'enter': 
            print ('Done breaking spots.')
            self.fig.canvas.mpl_disconnect(self.mouseCid)
            self.fig.canvas.mpl_disconnect(self.keyCid)
        return
############ drawGap ##################

############ breakSpots ##################

def breakSpot(flowerPetal, oldSpot, gap):
    fig = plt.gcf()
    ax = plt.gca()
    newSpots = oldSpot.difference(gap)
    lsc = list(flowerPetal.spots)
    lsc.remove(oldSpot) 
    nls = lsc + list(newSpots)
    flowerPetal.spots = sg.multipolygon.MultiPolygon(nls)
    aa=ax.get_xlim(); bb=ax.get_ylim()
    ax.cla()
    ax.set_xlim(aa); ax.set_ylim(bb)
    ax.add_patch(PolygonPatch(flowerPetal.petal,
                  fc='yellow', ec='black',
                  linewidth=2, alpha=1.0))
    ax.add_patch(PolygonPatch(flowerPetal.spots,
                  fc='red', ec='black',
                  linewidth=2, alpha=1.0))
 
############ breakSpots ##################


class testMpl:
    def __init__(self):
        self.keyCid = plt.gcf().canvas.mpl_connect('key_press_event', self)
        self.mouseCid = plt.gcf().canvas.mpl_connect('button_press_event', self)
        self.event = None
    def __call__(self, event):
        print(event)
        self.event = event
            #plt.gcf().canvas.mpl_disconnect(self.keyCid)

xx = testMpl()





                
#geoJ='/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/polygons/P765F1/left/P765F1_left_polys.geojson'
geoJ='/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/polygons/P765F1/right/P765F1_right_polys.geojson'
fl = FlowerPetal.FlowerPetal()
fl.plantName = 'P765'
fl.flowerName = 'F1'
fl.petalName = 'left'
fl.geojson = 'P765F1_left_polys.geojson'
fl.parseGeoJson(geoJ)
fl.cleanFlowerPetal()

## plot all spots, pick one:
plt.ion()
fl.plotOne(fl.petal)
fl.addOne(fl.spots, pick=True)

## pick it
aa = PolyPicker(fl)

## show where to break it
bb = drawGap(fl, aa.spot) 

## break it, add it to the spots

len(fl.spots)
breakSpot(fl,bb.spot,bb.poly)
len(fl.spots)


## works. build it back into the breaker.

## or not. We gotta think about how this pipeline 
## will function. 

## ideally we have all the various functions we need
## in different modules. 
## script in a different files that calls them.

## this script would be the master file for 
## creating geojsons from our images, then 
## creates flowerPetal objects, and allows the user 
## to sanity-check/correct as it goes. 

## so this, maybe leave the spot selector and breaker
## as they are, and use the master script to 
## glue them together and modify the flowerPetal object.

## seems like for modularity's sake, these functions 
## shouldn't have the built in capacity to modify 
## flowerPetals. 

## so for tomorrow - 

## add a second axis that has an image of the flower petals that 
## the user can zoom into (or a second canvas?)

## clear up the gcf/gcas, so that a picker or breaker stays with
## the right axes, dies/disconnects when it needs to. 

## if there is still time (there won't be), start smoothing out 
## the pipeline, functions in their files, master pipeline in another.

## and then, take it for a spin!

zz = [3,6,3,89,3]
yy = [1,1,1,19,4]

xx = zz + yy

xx.append(5)
