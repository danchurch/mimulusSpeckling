#!/usr/bin/env bash

getSpots='/Users/danthomas/Documents/speckling/make_polygons/get_spots.py'
getZones='/Users/danthomas/Documents/speckling/make_polygons/get_zones.py'
wd='/Users/danthomas/Documents/speckling/make_polygons/polygons'

cd $wd

for i in *; do
    echo $i 
    cd $i 
    for j in *; do
        fullN=$PWD/$j
        $getSpots $fullN $fullN
        find $fullN -name "*.geojson" -exec $getZones {} 0.5 \;
    done
    cd ../
done
