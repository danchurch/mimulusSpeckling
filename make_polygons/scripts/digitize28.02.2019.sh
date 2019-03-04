#!/usr/bin/env bash

#repo="/home/daniel/Documents/cooley_lab/mimulusSpeckling/" ## my comp
repo="/Users/danthomas/Documents/speckling/" ## mac
wd=$repo"make_polygons/polygons/plate3"
packages=$repo"make_polygons/package/makeFlowerPolygons/"
get_spots=$packages"get_spots.py"
get_zones=$packages"get_zones.py"

cd $wd

aa=$(find . -name "*melted.csv")

for i in ${aa[@]}; do
    echo $i
    $get_spots $i 
    j=${i/_melted.csv/_polys.geojson}
    echo $j
    $get_zones $j 0.5 
done
