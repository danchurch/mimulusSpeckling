#!/usr/bin/env bash

dellWD=''
macWD='/Users/danthomas/Documents/speckling'
WD=$macWD
gSpots='make_polygons/get_spots.py'
gZones='make_polygons/get_zones.py'
getSpots=$WD"/"$gSpots
getZones=$WD"/"$gZones

cd /Users/danthomas/Documents/speckling/make_polygons/plate2
for i in *; do
    echo $i 
    cd $i
    for j in *; do
        echo $j
        cd $j
            #$getSpots *melted.csv
            #$getZones *geojson 0.5
            ls *melted.csv
            ls *geojson 
        cd ..
    done
    cd ..
    pwd
done
