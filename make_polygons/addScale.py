#!/usr/bin/env python3

import get_spots, geojsonIO, json, argparse

def getScale(meltedMatrix):
    photoBB, petalMat, spotsMat = get_spots.parseDougMatrix(meltedMatrix)
    petPolRaw = get_spots.digitizePols(petalMat)
    petPol = get_spots.cleanCollections(petPolRaw)
    scale,_ = get_spots.getPetGeoInfo(petPol)
    return(scale)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('meltedMatrix',
                help=("""Name of file that contains CSV versions of
                         doug's "melted" matrix, the result of
                         manually choosing color centers from his
                         matlab color-categorization scripts.
                       """))
    parser.add_argument('geojson',
                help=("""geojson file that you are adding scaling factor to"""), 
                default=None)
    parser.add_argument('--outFileName',"-o",
                help=("""output geojson file"""), 
                default=None)

    args = parser.parse_args()
    if args.outFileName:
        outFileName = args.outFileName
    else: outFileName = args.geojson

    ## deal with arguments

    ## read old geojson:
    (petal, spots, 
        center, edge, throat, 
        spotEstimates, 
        photoBB, 
        scalingFactor) = geojsonIO.parseGeoJson(args.geojson)

    ## get scaling factor
    scalingFactor=getScale(args.meltedMatrix)

    ## Write  out new geojson:
    geoDict = geojsonIO.writeGeoJ(petal, spots, 
            center, edge, throat, 
            spotEstimates, photoBB, 
            scalingFactor)

    with open(outFileName, 'w') as fp:
        json.dump(geoDict, fp)
