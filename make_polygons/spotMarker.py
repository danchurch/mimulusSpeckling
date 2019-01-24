#!/usr/bin/env python3

import argparse, json
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
        self.done = 0
        self.event = None
        self.centerx = None
        self.centery = None
        self.circs = []
        self.circArts = []
        self.centerpts = []
        self.markCID = self.fig.canvas.mpl_connect('button_press_event', self)
        self.releaseCID = self.fig.canvas.mpl_connect('button_release_event', self)
        self.keyCID = self.fig.canvas.mpl_connect('key_press_event', self)
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
            circle = sg.Point(self.centerx, self.centery).buffer(circleRad)
            self.circs.append(circle)
            circArt = geojsonIO.addOne(self.circs[-1], col = 'blue')
            self.circArts.append(circArt)

        elif (self.event.name == 'button_press_event' 
            and self.event.button != 1):
            try:
                self.centerpt.remove()
                self.circArts[-1].remove()
                del(self.centerpts[-1])
                del(self.circArts[-1])
                del(self.circs[-1])
            except (IndexError, AttributeError, ValueError):
                pass
            try:
                self.centerpt = self.centerpts[-1]
                self.circle = self.circs[-1]
            except (IndexError):
                self.centerpt = None
                self.circle = None

        elif (self.event.name == 'key_press_event'
            and self.event.key == 'enter'
            and self.done == 0):
            self.done += 1
            self.fig.suptitle('All done? Press enter again to confirm.')

        elif (self.event.name == 'key_press_event'
            and self.event.key == 'enter'
            and self.done == 1): 
                self.fig.canvas.mpl_disconnect(self.markCID)
                self.fig.canvas.mpl_disconnect(self.releaseCID)
                self.fig.canvas.mpl_disconnect(self.keyCID)
                plt.close('all')
 


######### helper functions #################

def choice():
    """ a way to keep the script running till user is done"""
    try:
        aa = input("Finished (y)? ")
        assert aa == "y"
    except AssertionError as err:
        print('Enter "y" when done.')
        choice()

def main(geojson): 
    plt.ion()
    petal,spots,center,edge,throat,spotEstimates = geojsonIO.parseGeoJson(geojson)
    geojsonIO.plotOne(petal); geojsonIO.addOne(spots)
    spotMarker = SpotMarker()
    choice()
    spotEstimates = sg.MultiPolygon(spotMarker.circs)
    featC = geojsonIO.writeGeoJ(petal,spots,center,edge,throat, spotEstimates)
    with open(outFileName, 'w') as fp:
        json.dump(featC, fp)

##########################

if __name__ == "__main__":

    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('geojson',
                help=("""Name of the geojson file to which you want to
                        estimate spots. """),
                type=str)
    parser.add_argument('-o', '--out',
                help=("Name for outfile. If none given, modified in place."),
                type=str,
                default=None)

    args = parser.parse_args()
    if args.out is not None:
        outFileName = args.out
    else:
        outFileName = args.geojson

    main(args.geojson)

