#!/usr/bin/env python3

import os, argparse, json
import matplotlib.pyplot as plt
import geojsonIO as gj
import get_zones as gz

def auto_call(geojson, centerSize, simp):
    petal,spots,center,edge,throat = gj.parseGeoJson(geojson)
    center = gz.findCenter(petal, centerSize)
    edge, throat = gz.findEdgeThroat(petal, center, simp=simp)
    return(petal,spots,center,edge,throat)

def plotFlowerZones(petal,spots,center,edge,throat):
    gj.plotOne(petal)
    gj.addOne(spots)
    gj.addOne(edge, col='white', a=0.5)
    gj.addOne(throat, col='white', a=0.5)

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

def main(geojson, centerSize, simp):
    ## run autocall and plot:
    petal,spots,center,edge,throat = auto_call( geojson, 
                                                centerSize, 
                                                simp)
    plt.ion()
    plotFlowerZones(petal,spots,center,edge,throat)
    print("Here's the flower and zones. Look ok? ", end = "")
    ZonesOK=choice()
    if ZonesOK == 'y': quit()
    elif ZonesOK == 'n': 
        print('Try automated zone call with another simplification level?', end ="")
        anotherSimp=choice()

    if anotherSimp == 'y':
        print('Enter simplification level. ', end ="")
        simp=valNum()
        plt.close('all')
        main(geojson, centerSize, simp)
    elif anotherSimp == 'n':
        print('Try manual zone call?', end ="")
        manDraw=choice()

    if manDraw == 'y':
        print('okay, its time to get real...')




    elif manDraw == 'n':
        print("I'm confused....")
        main(geojson, centerSize, simp)

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
    parser.add_argument("simplification",
                help=("""How much simplification to inflict on the petal
                       polygons to find zones. A good start might be 0.5
                       (the default)."""),
                default=0.5,
                type=float)
    parser.add_argument('-o', '--out',
                help=("Name for outfile. If none given, modified in place."),
                type=str,
                default=None)

    args = parser.parse_args()

    if args.out is not None:
        outFileName = args.out
    else:
        outFileName = args.geojson

######

## for debug
#class Args:
#    def __init__(self):
#        self.geojson = "/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/polygons/P338F1/right/P338F1_right_polys.geojson"
#        self.centerSize = 0.5
#        self.simplification = 0.5
#
#args=Args()




#        petal,spots,center,edge,throat = auto_call( geojson, 
#                                                    centerSize, 
#                                                    simp)
#

main(args.geojson,
        args.centerSize,
        args.simplification) 

#    ## write it out
#    with open(outFileName, 'w') as fp:
#        json.dump(featC, fp)

##########3

## interactive zone caller.


