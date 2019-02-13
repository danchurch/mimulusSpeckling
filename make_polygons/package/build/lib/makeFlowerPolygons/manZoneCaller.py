#!/usr/bin/env python3

import matplotlib as mp
mp.use("TkAgg")
import os, argparse, json
import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry as sg
import makeFlowerPolygons.geojsonIO as geojsonIO
import makeFlowerPolygons.get_zones as gz
import matplotlib.pyplot as plt

def auto_call(geojson, centerSize, simp):
    (petal,spots,
    center,edge,throat, 
    spotEstimates, photoBB, 
    scalingFactor) = geojsonIO.parseGeoJson(geojson)
    center = gz.findCenter(petal, centerSize)
    edge, throat = gz.findEdgeThroat(petal, center, simp=simp)
    return(petal,spots,center,edge,throat)

def plotFlowerZones(petal,spots,center,edge,throat):
    geojsonIO.plotOne(petal)
    geojsonIO.addOne(spots)
    geojsonIO.addOne(edge, col='white', a=0.5)
    geojsonIO.addOne(throat, col='white', a=0.5)
    if mp.get_backend() == 'TkAgg':
        plt.gcf().canvas.manager.window.wm_geometry("+900+0")

def choice():
    try:
        aa = input("(y/n): ")
        assert aa in {"y","n"}
    except AssertionError as err:
        print('Enter "y" or "n"')
        aa = choice()
    finally:
        return(aa)

def valNum():
    try:
        aa = input("(Enter a numeric value): ")
        aa = float(aa)
    except ValueError as err:
        print('Did you enter a number?')
        aa = valNum()
    finally:
        return(aa)

def getNewEdgeThroat(pol, petal, center):
    aa = pol.intersection(petal)
    newThroat = aa.difference(center)
    marg = petal.difference(center)
    newEdge = marg.difference(newThroat)
    return(newEdge, newThroat)

def saveOut ( petal,spots,center,edge,throat, 
                spotEstimates, photoBB, 
                scalingFactor, centerSize, geojson, outFileName):
    print('Save new zones?')
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

class PolyMaker:
    def __init__(self, petal, center):
        geojsonIO.plotOne(petal)
        geojsonIO.addOne(center, col='white', a=0.5)
        self.fig = plt.gcf()
        self.ax = plt.gca()
        newYLim = [ i * 1.1 for i in list(self.ax.get_ylim()) ]
        newXLim = [ i * 1.1 for i in list(self.ax.get_xlim()) ]
        self.ax.set_ylim(newYLim)
        self.ax.set_xlim(newXLim)
        if mp.get_backend() == 'TkAgg':
            self.fig.canvas.manager.window.wm_geometry("+900+0")
        self.petal = petal
        self.center = center
        self.verts = []
        self.poly = None
        self.mouseCID = self.fig.canvas.mpl_connect('button_press_event', self)
        self.keyCID = self.fig.canvas.mpl_connect('key_press_event', self)
    def __call__(self,event):
        if plt.get_current_fig_manager().toolbar.mode != '': return
        self.event = event
        if event.name == "button_press_event":
            if event.inaxes!=self.ax: return
            if event.button == 1:
                self.verts.append((event.xdata,event.ydata))
            elif event.button != 1:
                try:
                    self.verts.pop()
                except IndexError as err:
                    print(err)
                    pass
            aa = np.array(self.verts).transpose()
            geojsonIO.clearOne()
            geojsonIO.addOne(self.petal, col='yellow')
            geojsonIO.addOne(self.center, col='white', a=0.5)
            try:
                assert(len(self.verts) > 0)
                self.ax.plot(aa[0],aa[1],'o', color='red')
            except (IndexError, AssertionError) as err:
                pass
            ## plot poly
            try:
                geojsonIO.clearOne()
                geojsonIO.addOne(self.petal, col='yellow')
                geojsonIO.addOne(self.center, col='white', a=0.5)
                self.ax.plot(aa[0],aa[1],'o', color='red')
                geojsonIO.addOne(sg.Polygon(self.verts), a= 0.3)
            except (ValueError, IndexError):
                pass
        elif event.name == "key_press_event" and event.key == 'enter':
            self.ax.set_title('Creating/updating polygon')
            self.poly = sg.Polygon(self.verts)
        elif event.name == "key_press_event" and event.key == 'escape':
            plt.close('all')
            self.fig.canvas.mpl_disconnect(self.mouseCID)
            self.fig.canvas.mpl_disconnect(self.keyCID)
            return


def main( petal,spots,center,edge,throat, 
                spotEstimates, photoBB, 
                scalingFactor, centerSize, geojson, outFileName):
    plt.ion()
    plotFlowerZones(petal,spots,center,edge,throat)
    print("Here's the flower and zones. Look ok? ", end = "")
    ZonesOK=choice()

    if ZonesOK == 'y': 
        ## write it out?
        saveOut( petal,spots,center,edge,throat, 
                spotEstimates, photoBB, 
                scalingFactor, centerSize, geojson, outFileName)
    elif ZonesOK == 'n': 
        print('Try automated zone call with another simplification level?', end ="")
        anotherSimp=choice()

        if anotherSimp == 'y':
            print('Enter simplification level. ', end ="")
            simp=valNum()
            plt.close('all')
            petal,spots,center,edge,throat = auto_call( geojson, 
                                                        centerSize, 
                                                        simp)
            main( petal,spots,center,edge,throat, 
                            spotEstimates, photoBB, 
                            scalingFactor, centerSize, geojson, outFileName)
        elif anotherSimp == 'n':
            print('Try manual zone call?', end ="")
            manDraw=choice()
            if manDraw == 'y':
                plt.close('all')
                print('Draw polygon to define the left and right boundaries of throat.'
                    ' Tell us when done by typing y.')
                pm = PolyMaker(petal, center)
                choice()
                edge, throat = getNewEdgeThroat(pm.poly, petal, center)
                plotFlowerZones(petal,spots,center,edge,throat)
                saveOut( petal,spots,center,edge,throat, 
                        spotEstimates, photoBB, 
                        scalingFactor, centerSize, geojson, outFileName)
            elif manDraw == 'n':
                print("Let's startover")
                plt.close('all')
                main( petal,spots,center,edge,throat, 
                                spotEstimates, photoBB, 
                                scalingFactor, centerSize, geojson, outFileName)


########################################

if __name__ == '__main__':

    ## deal with arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('geojson',
                help=("""Name of the geojson file to which you want to\
                        assign zones. """))
    parser.add_argument('centerSize',
                help=("""give the proportion of the middle of the flower \
                       you would like to call Center Zone, from 0.01 \
                       to 0.99."""),
                type=float)
#    parser.add_argument("simplification",
#                help=("""How much simplification to inflict on the petal
#                       polygons to find zones. A good start might be 0.5
#                       (the default)."""),
#                default=0.5,
#                type=float)
    parser.add_argument('-o', '--out',
                help=("Name for outfile. If none given, modified in place."),
                type=str,
                default=None)

    args = parser.parse_args()

    if args.out is not None:
        outFileName = args.out
    else:
        outFileName = args.geojson

    (petal,spots,
    center,edge,throat, 
    spotEstimates, photoBB, 
    scalingFactor) = geojsonIO.parseGeoJson(args.geojson)

    main( petal,spots,center,edge,throat, 
                spotEstimates, photoBB, 
                scalingFactor, args.centerSize, args.geojson, outFileName )
