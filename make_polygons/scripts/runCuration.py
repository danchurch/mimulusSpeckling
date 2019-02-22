#!/usr/bin/env python3

## for build
wd=pathlib.Path('/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/toy')
jpegs=pathlib.Path('/home/daniel/Documents/cooley_lab/mimulusSpeckling/dougRaster/Rotated_and_Cropped/plate2')
plate2='/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/polygons/plate2'

import os, argparse, pathlib, json
import makeFlowerPolygons

## deal with args:
parser = argparse.ArgumentParser()
parser.add_argument('folder',
        help=("Enter the working directory that has the geojsons"
            " that you are curating"))
parser.add_argument('jpgFolder',
        help=("Enter the folder that contains the jpeg files"
            " corresponding to the geojsons in your working folder."))
#parser.add_argument('-l', '--log',
#        help=("The name of the log that keep track of your progress"))

args = parser.parse_args()
wd=pathlib.Path(args.folder)
jpegs=pathlib.Path(args.jpgFolder)

if not wd.is_dir():
    print("Can't find the working directory: {}.".format(str(wd)))
    quit()
if not jpegs.is_dir():
    print("Can't find the jpeg directory: {}.".format(str(jpegs)))
    quit()


def choice():
    ch=input('(y/n)')
    try:
        assert(ch in {'y','n'})
        return(ch)
    except AssertionError:
        print("Respond with 'y' or 'n'.")
        return(choice())

def progChoice():
    progs={'Spotbreaker':None,
            'ManualZoneCaller': None,
            'SpotMarker': None}
    for i in progs.keys():
        print("Do you want to run {}"
                        " on all files in working directory?"
                        " (y/n):".format(i))
        yn=choice()
        progs[i]=yn
    return(progs)


def findLog(dir=os.getcwd()):
    try:
        oldLog=[i for i in os.listdir(dir) if "LOG" in i][0]
    except IndexError:
        print('No log found, starting new.')
        return
    print("Log found: {} ".format(oldLog))
    print("Use this?")
    ch=choice()
    if ch == 'y': return(oldLog)
    if ch == 'n': 
        print('Starting new log.')
        return

def findGeojs(dir):
    """ make our todo list"""
    listGeojs=[]
    bb = os.walk(dir, topdown=True)
    for i in bb:
        _,_,files = i
        [ listGeojs.append(i) for i in files if('geojson' in i)]
    return(listGeojs)

def makeNewLog(listGeojs):
    """make a empty log"""
    onefile={'Spotbreaker':False, 'ManualZoneCaller': False, 'SpotMarker': False}
    emptylogs = [onefile] * len(listGeojs)
    log=dict(list(zip(listGeojs, emptylogs)))
    return(log)


os.chdir(wd)
allGeojs=findGeojs(wd)
logfile=findLog(wd)
if not logfile:
    log=makeNewLog(allGeojs)
with open(logfile, 'r') as f:
    log=json.load(f)
pc=progChoice()

## todo lists:
sbDone={k:v['Spotbreaker'] for (k,v) in log.items()}
mzDone={k:v['ManualZoneCaller'] for (k,v) in log.items()}
smDone={k:v['SpotMarker'] for (k,v) in log.items()}

for i in allGeojs:
    if pc['Spotbreaker']=='y':
        if not sbDone[i]:
            makeFlowerPolygons.breakSpots.main(i,
            sbDone[i] = True
    if pc['ManualZoneCaller']=='y':
        if not mzDone[i]:
            makeFlowerPolygons.manZoneCaller.main(i,
            mzDone[i] == True
    if pc['SpotMarker']=='y':
        if not smDone[i]:
            makeFlowerPolygons.spotMarker.main(i,
            smDone[i] == True

## test modifications on individual programs, update pypi and comp
## clean up some of the above 
## sort list of geojs alphabetically
## figure out finding jpegs
## write out changes to log
## make a way to quit?
