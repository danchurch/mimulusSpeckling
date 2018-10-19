import FlowerPetal
import os
from matplotlib import pyplot as plt
from shapely import geometry as sg
from descartes import PolygonPatch

class PolyBuilder:
    def __init__(self):
        self.poly = sg.polygon.Polygon()
        self.xs = []
        self.ys = []
        self.cid = plt.gcf().canvas.mpl_connect('button_press_event', self)
    def __call__(self, event):
        if plt.get_current_fig_manager().toolbar.mode != '': return
        print('click', event)
        if event.inaxes!=plt.gca(): return
        aa=plt.gca().get_xlim()
        bb=plt.gca().get_ylim()
        plt.plot(event.xdata, event.ydata, marker='o', markersize=3, color="red")
        plt.gca().set_xlim(aa)
        plt.gca().set_ylim(bb)
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        try:
            self.poly = sg.polygon.Polygon(list(zip(self.xs, self.ys)))
            aa=plt.gca().get_xlim()
            bb=plt.gca().get_ylim()
            plt.gca().cla()
            plt.gca().set_xlim(aa)
            plt.gca().set_ylim(bb)
            plt.gca().add_patch(PolygonPatch(self.poly,
                          fc='red', ec='black',
                          linewidth=0.5, alpha=0.3))
        except ValueError:
            return
        finally:
            if event.dblclick==True: 
                print ('done!')
                plt.gcf().canvas.mpl_disconnect(self.cid)
                self.xs.pop() 
                self.ys.pop()
            return

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click to build polygons')
polyBuilder = PolyBuilder()

## Picker ##

geoJ='/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/polygons/P765F1/left/P765F1_left_polys.geojson'
fl = FlowerPetal.FlowerPetal()
fl.plantName = P765
fl.flowerName = 'F1'
fl.petalName = 'left'
fl.geojson = 'P765F1_left_polys.geojson'
fl.parseGeoJson(geoJ)
fl.cleanFlowerPetal()

class PolyPicker:
    def __init__(self, petal):
        self.cid = plt.gcf().canvas.mpl_connect('pick_event', self)
        self.petal = petal
        self.spot = None
        self.otherSpots = []
        self.x = None
        self.y = None
    def __call__(self, event):
        self.x = event.mouseevent.xdata
        self.y = event.mouseevent.ydata
        aa=plt.gca().get_xlim()
        bb=plt.gca().get_ylim()
        plt.gca().cla()
        plt.gca().set_xlim(aa)
        plt.gca().set_ylim(bb)
        pt=sg.point.Point([self.x, self.y])
        self.otherSpots = [ i for i in list(fl.spots) if not i.contains(pt) ]
        self.spot = [ i for i in list(fl.spots) if i.contains(pt) ][0]
        for i in self.otherSpots:
                plt.gca().add_patch(PolygonPatch(i,
                              fc='red', ec='black',
                              picker=True,
                              linewidth=0.2, alpha=0.5))
        plt.gca().add_patch(PolygonPatch(self.spot,
                      fc='green', ec='black',
                      picker=True,
                      linewidth=0.4, alpha=1.0))




## plot it:

plt.ion()
fl.plotOne(fl.petal)
fl.addOne(fl.spots, pick=True)

polyPicker = PolyPicker(fl)

aa = plt.gca().patches


## print flower, select spot to change, redraw, delete old polygon, append new ones

## how do we integrate these two objects to correct a problem 
## spot?


