import numpy as np
import shapely.geometry as sg
import shapely.ops as so
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import FlowerPetal, geojsonIO
from scipy.spatial import distance


class SpotMarker:
    def __init__(self): 
        self.fig = plt.gcf()
        self.ax = plt.gca()
        self.event = None
        self.centerx = None
        self.centery = None
        self.centerpt = None
        self.circs = []
        self.centerpts = []
        self.circlePolys = []
        self.circle = None
        self.markCID = self.fig.canvas.mpl_connect('button_press_event', self)
        self.releaseCID = self.fig.canvas.mpl_connect('button_release_event', self)
    def __call__(self, event):
        if plt.get_current_fig_manager().toolbar.mode != '': return
        self.event = event
        if (self.event.name == 'button_press_event' 
            and self.event.button == 1):
            self.centerx = event.xdata; self.centery = event.ydata
            try:
                self.centerpt, = self.ax.plot(event.xdata, event.ydata, 
                        marker='+', markersize=3, color = 'k')
                self.centerpts.append(self.centerpt)
            except ValueError:
                pass
        elif (self.event.name == 'button_release_event'
            and self.event.button == 1):
            circleRad = distance.euclidean((self.centerx, self.centery),
                                    (event.xdata, event.ydata))
            self.circle = plt.Circle((self.centerx, self.centery), circleRad)
            self.circs.append(self.circle)
            self.ax.add_patch(self.circle)
            circlePoly = sg.Polygon(self.circle.get_verts())
            self.circlePolys.append(circlePoly)
        elif (self.event.name == 'button_press_event' 
            and self.event.button != 1):
            try:
                self.centerpt.remove()
                self.circle.remove()
                del(self.centerpts[-1])
                del(self.circs[-1])
                del(self.circlePolys[-1])
            except (IndexError):
                pass
            try:
                self.centerpt = self.centerpts[-1]
                self.circle = self.circs[-1]
            except (IndexError):
                self.centerpt = None
                self.circle = None
