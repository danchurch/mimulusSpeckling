#!/usr/bin/env bash

getpols='/Users/danthomas/Documents/speckling/make_polygons/get_pols.py'
wd='/Users/danthomas/Documents/speckling/make_polygons/polygons'

cd $wd

for i in *; do
    echo $i 
    cd $i 
    for j in *; do
        fullN=$PWD/$j
        $getpols $fullN 0.5 $fullN
    done
    cd ../
done
