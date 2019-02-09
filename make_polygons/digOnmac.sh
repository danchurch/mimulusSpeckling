#!/usr/bin/env bash

getSpots='/Users/danthomas/Documents/speckling/make_polygons/get_spots.py'
getZones='/Users/danthomas/Documents/speckling/make_polygons/get_zones.py'
makePDFs='/Users/danthomas/Documents/speckling/make_polygons/makePDFs.py'
wd='/Users/danthomas/Documents/speckling/make_polygons/polygons/'
jpgDirectory='/Users/danthomas/Documents/speckling/dougRaster/Rotated_and_Cropped/plate2'
outDir='/Users/danthomas/Documents/bigPDF/'
plate='plate2/'

cd $wd$plate

for flower in *; do 
    echo $flower
    find $flower -name "*.csv" -exec $getSpots {} \;
    find $flower -name "*.geojson" -exec $getZones {} 0.5 \;
    $makePDFs $flower $wd$plate $jpgDirectory -o $outDir
done
