#!/usr/bin/env python3

import sys
sys.path.append("/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/package/")
import matplotlib.pyplot as plt
import shapely.validation as sv
import shapely.geometry as sg
from makeFlowerPolygons import geojsonIO
from makeFlowerPolygons import get_spots
from makeFlowerPolygons.geojsonIO import plotOne, addOne
plt.ion()

Rect=sg.box(-3.5, -3.5, 15.0, 15.0)
center=sg.Point(0, 0)
small = center.buffer(1)
medium = center.buffer(2)
large = center.buffer(3)
offCenter=sg.Point(10, 10)
offLarge = offCenter.buffer(3)
offLargeHole1 = sg.Point(9.5, 10).buffer(0.5)
offLargeHole2 = sg.Point(11.5, 10).buffer(0.5)
allpols = sg.MultiPolygon( [Rect, large, medium, small, offLarge, offLargeHole1, offLargeHole2 ] )
import pdb; pdb.set_trace()
aa=get_spots.organizeSpots(allpols)
input('about to end')
