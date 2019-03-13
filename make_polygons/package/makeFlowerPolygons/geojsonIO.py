import matplotlib
matplotlib.use('TkAgg')
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
            spotEstimates = sg.shape(spotEstimatesGJ)
        except:
            spotEstimates = sg.polygon.Polygon()
        try:
            photoBB = aa['metadata']["photoBB"]
        except:
            print("can't find BB")
            photoBB = None
        try:
            scalingFactor = aa['metadata']["scalingFactor"]
        except:
            scalingFactor = None
    return(petal,spots,center,edge,throat, spotEstimates, photoBB, scalingFactor)

def writeGeoJ(petal, spots, center, edge, throat, spotEstimates, photoBB, scalingFactor):
    """Function for putting polygons into a dictionary that can be written out \
    to json format, = geojson."""
    featC = {
            "type" : "FeatureCollection",
            "features" : [],
            "metadata" : {},
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
    ## add scalingFactor and bounding box
    try:
        featC['metadata']["scalingFactor"] = scalingFactor
    except (NameError, AttributeError):
        featC['metadata']["scalingFactor"] = None
    try:
        featC['metadata']["photoBB"] = photoBB
    except (NameError, AttributeError):
        featC['metadata']["photoBB"] = None
    return(featC)


def plotOne(poly,
            l=2, a=1.0,
            col='yellow',
            bkgcol='yellow',
            pick=None):
    fig = plt.figure()
    ax1 = plt.axes()
    ax1.set_xlim(min(poly.exterior.xy[0]), max(poly.exterior.xy[0]))
    ax1.set_ylim(min(poly.exterior.xy[1]), max(poly.exterior.xy[1]))
    ax1.set_aspect('equal')
    art = ax1.add_patch(PolygonPatch(poly,
                  fc=col, ec='black',
                  picker=pick,
                  linewidth=l, alpha=a))
    if poly.interiors:
        for i in poly.interiors:
            intPoly=sg.Polygon(i)
            ax1.add_patch(PolygonPatch(intPoly,
                          fc=bkgcol, ec='black',
                          picker=pick,
                  linewidth=l, alpha=a))

def addOne(poly,
            l=2, a=1.0,
            col='red',
            bkgcol='yellow',
            pick=None):
    ax1 = plt.gca()
    if poly.is_empty:
        print('Empty polgyon?')
        return
    elif not poly.is_empty:
        try:
            art = None
            for i in poly:
                ax1.add_patch(PolygonPatch(i,
                              fc=col, ec='black',
                              picker=pick,
                              linewidth=l, alpha=a))
                if i.interiors:
                    for j in i.interiors:
                        intPoly=sg.Polygon(j)
                        ax1.add_patch(PolygonPatch(intPoly,
                                      fc=bkgcol, ec='black',
                                      picker=pick,
                              linewidth=l, alpha=a))
        except TypeError:
            art = ax1.add_patch(PolygonPatch(poly,
                          fc=col, ec='black',
                          picker=pick,
                          linewidth=l, alpha=a))
            if poly.interiors:
                for i in poly.interiors:
                    intPoly=sg.Polygon(i)
                    ax1.add_patch(PolygonPatch(intPoly,
                                  fc=bkgcol, ec='black',
                                  picker=pick,
                          linewidth=l, alpha=a))



def clearOne():
    aa=plt.gca().get_xlim(); bb=plt.gca().get_ylim()
    plt.gca().cla()
    plt.gca().set_xlim(aa); plt.gca().set_ylim(bb)
 
