# flowerPetal 

This package is a very simple set of python modules that the Cooley lab
at Whitman College is using to analyze spotting patterns in Mimulus flowers.
It is still very much in alpha, with lots of bugs.

It currently accepts .csv files that contain image matrices of flowers. 
Three color types are accepted:  

photo background color = 0 
petal color = 2
spot color = 3

Image matrices initially must be "melted" into three columns,  x, y, and color. 
Functions provided then parse this into two image matrices, one for petal shape
and one for petal outline. These new images are saved as CSV files for 
downstream digitization into polygons of the shapely package class. 
Alternatively, you can start with spot and petal csvs already made.

Documentation is being developed at:

https://nbviewer.jupyter.org/github/danchurch/mimulusSpeckling/blob/master/make_polygons/notebooks/petals_to_polygons.ipynb 

For questions about use of the package, contact: thomasdc@whitman.edu

