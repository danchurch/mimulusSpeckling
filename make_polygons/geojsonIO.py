import json
import shapely.geometry as sg
import matplotlib.pyplot as plt
from descartes import PolygonPatch



def parseGeoJson(geojson):
    with open(geojson) as gjf:
        aa = json.load(gjf)
        listP = (aa['features'])
        try:
            petalGJ = [ i for i in listP if i['properties']['id'] == 'Petal' ][0]['geometry']
            petal = sg.shape(petalGJ)
        except:
            petal = sg.polygon.Polygon()
        try:
            spotsGJ = [ i for i in listP if i['properties']['id'] == 'Spots' ][0]['geometry']
            spots= sg.shape(spotsGJ)
        except:
            spots = sg.polygon.Polygon()
        try:
            centerGJ = [ i for i in listP if i['properties']['id'] == 'Center' ][0]['geometry']
            center = sg.shape(centerGJ)
        except:
            center = sg.polygon.Polygon()
        try:
            edgeGJ = [ i for i in listP if i['properties']['id'] == 'Edge' ][0]['geometry']
            edge = sg.shape(edgeGJ)
        except:
            edge = sg.polygon.Polygon()
        try:
            throatGJ = [ i for i in listP if i['properties']['id'] == 'Throat' ][0]['geometry']
            throat = sg.shape(throatGJ)
        except:
            throat = sg.polygon.Polygon()
        try:
            spotEstimatesGJ = [ i for i in listP if i['properties']['id'] == 'spotEstimates' ][0]['geometry']
            spotEstimates = sg.shape(spotsGJ)
        except:
            spotEstimates = sg.polygon.Polygon()
    return(petal,spots,center,edge,throat, spotEstimates)

def writeGeoJ(petal, spots, center, edge, throat, spotEstimates):
    """Function for putting polygons into a dictionary that can be written out \
    to json format, = geojson."""
    featC = {
            "type" : "FeatureCollection",
            "features" : [],
            }

    ## fill it with features
    partNames = ['Petal', 'Spots', 'Center', 'Edge', 'Throat', 'spotEstimates']
    ## each geometry needs a feature wrapper
    for i,part in enumerate([petal, spots, center, edge, throat, spotEstimates]):
        try:
            gj_i = sg.mapping(part)
        except (NameError, AttributeError):
            gj_i = {"type": "Polygon", "coordinates": []}
        finally:
            feature_i = {"type": "Feature",
                  "geometry": gj_i,
                  "properties": {"id":(partNames[i])}}
            featC['features'].append(feature_i)
    return(featC)

def plotOne(poly, l=2, a=1.0, col='yellow', pick=None):
    fig = plt.figure()
    ax1 = plt.axes()
    ax1.set_xlim(min(poly.exterior.xy[0]), max(poly.exterior.xy[0]))
    ax1.set_ylim(min(poly.exterior.xy[1]), max(poly.exterior.xy[1]))
    ax1.set_aspect('equal')
    ax1.add_patch(PolygonPatch(poly,
                  fc=col, ec='black',
                  picker=pick,
                  linewidth=l, alpha=a))


def addOne(poly, l=2, a=1.0, col='red', pick=None):
    ax1 = plt.gca()
    if poly.is_empty:
        print('Empty polgyon?')
        return
    elif not poly.is_empty:
        try:
            for i in poly:
                ax1.add_patch(PolygonPatch(i,
                              fc=col, ec='black',
                              picker=pick,
                              linewidth=l, alpha=a))
        except TypeError:
            ax1.add_patch(PolygonPatch(poly,
                          fc=col, ec='black',
                          picker=pick,
                          linewidth=l, alpha=a))

def clearOne():
    aa=plt.gca().get_xlim(); bb=plt.gca().get_ylim()
    plt.gca().cla()
    plt.gca().set_xlim(aa); plt.gca().set_ylim(bb)
 
