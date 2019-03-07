#!/usr/bin/env bash

#repo="/home/daniel/Documents/cooley_lab/mimulusSpeckling/" ## my comp
repo="/Users/danthomas/Documents/speckling/" ## mac
wd=$repo"make_polygons/polygons/plate3"
packages=$repo"make_polygons/package/makeFlowerPolygons/"
get_spots=$packages"get_spots.py"
get_zones=$packages"get_zones.py"
makePDFs=$packages"makePDFs.py"
outDir='/Users/danthomas/Documents/bigPDF'
jpgDirectory=$repo"dougRaster/Rotated_and_Cropped/plate3"
cd $wd

#echo "########################################"
#echo "Making petals and spots"
#echo ""
#echo ""
#
#aa=$(find $wd -name "*melted.csv")
#
#for i in ${aa[@]}; do
#    echo "Now making petal and spots for: "$i
#    $get_spots $i
#done
#
#
#
#echo ""
#echo "########################################"
#echo "Calling zones"
#echo ""
#echo ""
#
#bb=$(find $wd -name "*geojson")
#
#for i in ${bb[@]}; do
#    echo $i
#    $get_zones $i 0.5
#done
#
echo ""
echo "########################################"
echo "Creating PDFs"
echo ""
echo ""

for flower in *; do
    echo $flower
    $makePDFs $flower $wd $jpgDirectory -o $outDir
done


