#!/usr/bin/env bash

## change repo for mac
repo="/home/daniel/Documents/cooley_lab/mimulusSpeckling/" ## 
wd=$repo"make_polygons/toy/" ## change to wd
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
