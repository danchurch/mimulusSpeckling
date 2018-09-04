#!/usr/bin/env bash

getpols='/home/daniel/Documents/mimulusSpeckling/make_polygons/get_pols.py'
wd='/home/daniel/Documents/mimulusSpeckling/make_polygons/polygons'

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
