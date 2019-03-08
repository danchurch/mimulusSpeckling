#!/usr/bin/env python3

import os, argparse, pathlib, json, re, copy
import pandas as pd
from makeFlowerPolygons import breakSpots, manZoneCaller, spotMarker
import shapely.errors

## while working without internet, for updating packages
#import sys
#sys.path.append("/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/package/makeFlowerPolygons")
#import breakSpots
#import manZoneCaller 
#import  spotMarker

## debug variables:

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
                    " on all files in working directory?".format(i))
        yn=choice()
        progs[i]=yn
    return(progs)


def findLog(dir=os.getcwd()):
    try:
        oldLog=[i for i in os.listdir(dir) if "log.json" in i][0]
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
        di,_,fi = i
        pathDi=pathlib.Path(di)
        [ listGeojs.append(str(pathDi / i)) for i in fi if('geojson' in i)]
    return(listGeojs)

def makeNewLog(listGeojs):
    """make a empty log"""
    emptylogs = [ {'Spotbreaker':False, 'ManualZoneCaller': False,
                'SpotMarker': False} for i in listGeojs ]
    log=dict(list(zip(listGeojs, emptylogs)))
    return(log)


def findJPG(geojson, jpgs):
    """
    given a directory, find our flower jpeg in it. Use pathlib.Path objects
    """
    allJpgs = os.listdir(jpgs)
    aa = re.search('(P.*?)_', geojson.name)
    flowerName = aa.groups()[0]
    jpgList = [ i for i in allJpgs if (flowerName in i and "JPG" in i) ]
    try:
        assert jpgList
        jpgName=jpgList[0]
        jpg = pathlib.Path(jpgName)
        return(jpgs / jpg)
    except AssertionError as err:
        print("Can't find jpeg. Check geojson name or jpeg folder.")
        quit()

def updateLog(logfile, log):
    ## save out log
    with open(logfile, 'w') as f:
        json.dump(log, f)

def textLog(log):
    ## write out a text version for user to read if they like
    pdLog = pd.DataFrame.from_dict(log,orient='index')
    pdLog.to_csv('log.csv')

def main(wd, jpgs):
    os.chdir(wd)
    allGeojs=findGeojs(wd)
    allGeojs.sort()
    if not allGeojs: 
        print("No geojsons found in this folder.")
        return
    logfile=findLog(wd)
    if logfile:
        with open(logfile, 'r') as f:
            log=json.load(f)
    elif not logfile:
        log=makeNewLog(allGeojs)
        logfile="log.json"
    pc=progChoice()


    for i in allGeojs:
        print(i)
        jpg=findJPG(pathlib.Path(i), jpgs)
        if pc['Spotbreaker']=='y':
            if not log[i]['Spotbreaker']:
                print("Breaking spots in {}".format(i))
                try:
                    breakSpots.main(i, jpg, i)
                    log[i]['Spotbreaker'] = True
                except shapely.errors.TopologicalError:
                    print('That failed due to invalid polygons. Skipping.')
                    log[i]['Spotbreaker'] = False
                updateLog(logfile, log)
                textLog(log)

        if pc['ManualZoneCaller']=='y':
            if not log[i]['ManualZoneCaller']:
                print("Calling zones in {}".format(i))
                manZoneCaller.main(i,i,jpg)
                log[i]['ManualZoneCaller'] = True
                updateLog(logfile, log)
                textLog(log)

        if pc['SpotMarker']=='y':
            if not log[i]['SpotMarker']:
                print("Estimating spot events in {}".format(i))
                spotMarker.main(i, jpg, i)
                log[i]['SpotMarker'] = True
                updateLog(logfile, log)
                textLog(log)

    
    updateLog(logfile, log)
    textLog(log)

## deal with args:
if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('folder',
            help=("Enter the working directory that has the geojsons"
                " that you are curating"))
    parser.add_argument('jpgFolder',
            help=("Enter the folder that contains the jpeg files"
                " corresponding to the geojsons in your working folder."))

    args = parser.parse_args()
    wd=pathlib.Path(args.folder)
    jpgs=pathlib.Path(args.jpgFolder)
    if not wd.is_dir():
        print("Can't find the working directory: {}.".format(str(wd)))
        quit()
    if not jpgs.is_dir():
        print("Can't find the jpeg directory: {}.".format(str(jpgs)))
        quit()

    main(wd, jpgs)
