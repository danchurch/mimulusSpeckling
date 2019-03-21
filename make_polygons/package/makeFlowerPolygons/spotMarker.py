#!/usr/bin/env python3

import matplotlib as mp
mp.use("TkAgg")
import argparse, json, pathlib, os, re
import numpy as np
import shapely.geometry as sg
import shapely.ops as so
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import makeFlowerPolygons.flowerPetal
from descartes import PolygonPatch
from makeFlowerPolygons import geojsonIO
from scipy.spatial import distance

## while tweaking packages locally:
#import sys
#sys.path.append("/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/package/makeFlowerPolygons")
#import breakSpots
#import manZoneCaller
#import  spotMarker
#import  geojsonIO


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
        self.fig.canvas.manager.window.wm_geometry("+900+0")
        newYLim = [ i * 1.1 for i in list(self.ax.get_ylim()) ]
        newXLim = [ i * 1.1 for i in list(self.ax.get_xlim()) ]
        self.ax.set_ylim(newYLim)
        self.ax.set_xlim(newXLim)
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
            try:
                circleRad = distance.euclidean((self.centerx, self.centery),
                                    (event.xdata, event.ydata))
                assert(circleRad > 0)
                circle = sg.Point(self.centerx, self.centery).buffer(circleRad)
                self.circs.append(circle)
                circArt,_ = geojsonIO.addOne(self.circs[-1], col = 'blue', a=0.3)
                self.circArts.append(circArt[0])
            except (AssertionError, TypeError, AttributeError):
                ## if button released too quickly, cleanup
                print("zero radius spot")
                self.centerpt.remove()
                self.centerpt = None
                self.centerx = None; self.centery = None
                del(self.centerpts[-1])

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

def plotOutline(poly, ax=None, l=2, col='black'):
    """Plot the outline of a polgon. Maybe move this 
    to the geojsonIO module?"""
    x,y = poly.exterior.xy
    if not ax: 
        fig = plt.figure(); ax=plt.axes()
        ax.set_xlim(min(x), max(x))
        ax.set_ylim(min(y), max(y))
        ax.set_aspect('equal')
    out=ax.plot(x, y, color=col, alpha=0.7,
        linewidth=l, solid_capstyle='round', zorder=2)
    return(out)

def photoAndPetal(geojson,jpg):
    """plot the photo image of the petal that
    corresponds to the geojson, along with 
    an outline of our petal polygon"""
    (petal,spots,center,edge,throat, 
        spotEstimates, photoBB, 
                    scalingFactor) = geojsonIO.parseGeoJson(geojson)
    plt.ion()
    img=mpimg.imread(jpg)
    photoBB = [ int(i) for i in photoBB ]
    justPetal = img[photoBB[1]:photoBB[3],photoBB[0]:photoBB[2]]
    aa = plotOutline(petal, col='blue')
    plt.gca().imshow(justPetal, extent=plt.gca().get_xlim() + plt.gca().get_ylim(),
                    origin = 'lower')

def preview(spotEstimates, petal, ax=None):
    """view the existing spotEstimates of 
    a geojson"""
    if not ax: 
            x,y = petal.exterior.xy
            plotOutline(petal, ax=None, col='black')
            plt.gca().set_xlim(petal.bounds[0], petal.bounds[2])
            plt.gca().set_ylim(petal.bounds[1], petal.bounds[3])
            plt.gca().set_aspect('equal')
            geojsonIO.addOne(spotEstimates, a=0.3)
    elif ax: geojsonIO.addOne(spotEstimates, a=0.3)

def finished():
    """ a way to keep the script running till user is done"""
    try:
        aa = input("Finished (y)? ")
        assert aa == "y"
    except AssertionError as err:
        print('Enter "y" when done.')
        finished()

def choice():
    try:
        aa = input("(y/n): ")
        assert aa in {"y","n"}
    except AssertionError as err:
        print('Enter "y" or "n"')
        aa = choice()
    finally:
        return(aa)


def main(geojson, jpg, outFileName=None): 
    geojson = pathlib.Path(geojson)
    jpg = pathlib.Path(jpg)
    plt.ion()
    (petal,spots,center,edge,throat, 
        spotEstimates, photoBB, 
                    scalingFactor) = geojsonIO.parseGeoJson(geojson)
    photoAndPetal(geojson,jpg)
    preview(spotEstimates, petal, ax=plt.gca())
    plt.gcf().canvas.manager.window.wm_geometry("+900+0")
    inkspot=input("Spots estimates look okay? (y/n) ")
    try:
        assert(inkspot in {'y','n'})
    except AssertionError:
        print("Enter 'y' or 'n'")
        main(geojson, jpg, outFileName)
    if inkspot == 'n':
        plt.close('all')
        photoAndPetal(geojson,jpg)
        plt.gcf().canvas.manager.window.wm_geometry("+900+0")
        spotMarker = SpotMarker()
        finished()
        print("Save edited inkspots?")
        saveSp=choice()
        if saveSp == 'y':
            spotEstimates = sg.MultiPolygon(spotMarker.circs)
            featC = geojsonIO.writeGeoJ (petal,spots,center,edge,throat, 
                                            spotEstimates, photoBB, 
                                                        scalingFactor)
            plt.close('all')
            spotMarker.fig.canvas.mpl_disconnect(spotMarker.markCID)
            spotMarker.fig.canvas.mpl_disconnect(spotMarker.releaseCID)
            with open(outFileName, 'w') as fp:
                json.dump(featC, fp)
        elif saveSp == 'n':
            print("Okay, no changes to {} spot "
                    "estimates saved.".format(str(geojson.name)))
            plt.close('all')
            spotMarker.fig.canvas.mpl_disconnect(spotMarker.markCID)
            spotMarker.fig.canvas.mpl_disconnect(spotMarker.releaseCID)
            return
    elif inkspot == 'y':
        print('Bye for now from spotMarker!')
        plt.close('all')
        return

##########################

if __name__ == "__main__":

    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('geojson',
                help=("""Name of the geojson file to which you want to
                        add estimated spots. """),
                type=str)
    parser.add_argument('jpg',
                help=("""Name of the jpeg image that corresponds
                        to the geojson of petal."""),
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

    main(args.geojson,args.jpg, outFileName)

