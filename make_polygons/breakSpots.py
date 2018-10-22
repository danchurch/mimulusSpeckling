import FlowerPetal
import os, copy
import matplotlib.backend_bases
from matplotlib import pyplot as plt
from shapely import geometry as sg
from descartes import PolygonPatch


## to breakup a spot:
class spotBreaker:
    def __init__(self, spot):
        self.spot = spot
        self.poly = sg.polygon.Polygon()
        self.xs = []
        self.ys = []
        self.mouseCid = plt.gcf().canvas.mpl_connect('button_press_event', self)
        self.keyCid = plt.gcf().canvas.mpl_connect('key_press_event', self)
    def __call__(self, event):
        if plt.get_current_fig_manager().toolbar.mode != '': return
        elif event.inaxes!=plt.gca(): return
        elif event.name == 'button_press_event':
            aa=plt.gca().get_xlim(); bb=plt.gca().get_ylim()
            plt.plot(event.xdata, event.ydata, marker='o', markersize=3, color="black")
            plt.gca().set_xlim(aa); plt.gca().set_ylim(bb)
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            try:
                self.poly = sg.polygon.Polygon(list(zip(self.xs, self.ys)))
                aa=plt.gca().get_xlim(); bb=plt.gca().get_ylim()
                plt.gca().cla()
                plt.gca().set_xlim(aa); plt.gca().set_ylim(bb)
                plt.gca().add_patch(PolygonPatch(self.spot,
                              fc='green', ec='black',
                              linewidth=0.5, alpha=0.3))
                plt.gca().add_patch(PolygonPatch(self.poly,
                              fc='red', ec='black',
                              linewidth=0.5, alpha=0.5))
                return
            except ValueError:
                return
        elif event.name == 'key_press_event' and event.key == 'enter': 
            print ('done!')
            plt.gcf().canvas.mpl_disconnect(self.mouseCid)
            plt.gcf().canvas.mpl_disconnect(self.keyCid)
        return


class testMpl:
    def __init__(self):
        self.keyCid = plt.gcf().canvas.mpl_connect('key_press_event', self)
        self.mouseCid = plt.gcf().canvas.mpl_connect('button_press_event', self)
        self.event = None
    def __call__(self, event):
        print(event)
        self.event = event
            #plt.gcf().canvas.mpl_disconnect(self.keyCid)

aa = testMpl()

## need to build a clip by the petal outline. 



## Picker ##
class PolyPicker:
    def __init__(self, petal):
        self.cidPick = plt.gcf().canvas.mpl_connect('pick_event', self)
        self.cidEnter = plt.gcf().canvas.mpl_connect('key_press_event', self)
        self.petal = petal
        self.spot = None
        self.closePlot = False
        self.noSpot = False
        self.otherSpots = []
        self.x = None
        self.y = None
    def __call__(self, event):
        if event.name == 'pick_event':
            self.x = event.mouseevent.xdata
            self.y = event.mouseevent.ydata
            self.closePlot = False
            plt.gcf().suptitle("")
            aa=plt.gca().get_xlim(); bb=plt.gca().get_ylim()
            plt.gca().cla()
            plt.gca().set_xlim(aa); plt.gca().set_ylim(bb)
            pt=sg.point.Point([self.x, self.y])
            self.otherSpots = [ i for i in list(fl.spots) if not i.contains(pt) ]
            self.spot = [ i for i in list(fl.spots) if i.contains(pt) ][0]
            for i in self.otherSpots:
                    plt.gca().add_patch(PolygonPatch(i,
                                  fc='red', ec='black',
                                  picker=True,
                                  linewidth=0.2, alpha=0.2))
            plt.gca().add_patch(PolygonPatch(self.spot,
                          fc='green', ec='black',
                          picker=True,
                          linewidth=0.4, alpha=1.0))
        elif event.name == 'key_press_event' and event.key == 'enter': 
            try:
                assert(self.spot is not None)
                if self.closePlot:
                    plt.gcf().suptitle("Bye!")
                    plt.gcf().canvas.mpl_disconnect(self.cidPick)
                    plt.gcf().canvas.mpl_disconnect(self.cidEnter)
                    plt.close()
                elif not self.closePlot:
                    plt.gcf().suptitle("Spot chosen. Press enter again to confirm")
                    self.closePlot = True
                    return
            except AssertionError as err:
                if self.noSpot == False: 
                    plt.gcf().suptitle("No spot chosen. Is this correct? Press \"enter\" again to confirm.")
                    self.noSpot = True 
                elif self.noSpot == True: 
                    plt.gcf().suptitle("Okay, no spots edited.")
                    plt.gcf().canvas.mpl_disconnect(self.cidPick)
                    plt.gcf().canvas.mpl_disconnect(self.cidEnter)

                
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

## plot spot of interest
plt.ion()
fl.plotOne(fl.petal)
fl.addOne(aa.spot)

## break it
bb = spotBreaker(aa.spot) 

fl.plotOne(bb.spot)

## one of the "breaker polygons":
fl.addOne(bb.poly)

## this is what we want:
fl.addOne(bb.spot.difference(bb.poly), col='purple')

newSpots = bb.spot.difference(bb.poly)

## so this spot needs to be deleted from the flowerpetal object,
## and these new spots added 

## how to do this...

zz = [ i for i in fl.spots if i == (aa.spot) ][0]

fl.plotOne(zz)

## works, but how to remove just this spot?
## does this make a deep copy?
## not sure. to be safe:

sc = copy.deepcopy(fl.spots)
lsc = list(sc)
lsc.remove(zz)
sg.multipolygon.MultiPolygon(lsc)

len(fl.spots)
fl.spots = sg.multipolygon.MultiPolygon(lsc)
len(fl.spots)

## works, now add the two new spots?

sc = copy.deepcopy(fl.spots)
lsc = list(sc)

nlsc = lsc + list(newSpots)


len(fl.spots)
fl.spots = sg.multipolygon.MultiPolygon(nlsc)
len(fl.spots)

fl.plotOne(fl.petal)
fl.addOne(fl.spots)

## works. build it back into the breaker.


