from matplotlib import pyplot as plt
from shapely import geometry as sg
from descartes import PolygonPatch

class PolyBuilder:
    def __init__(self):
        self.poly = sg.polygon.Polygon()
        self.xs = []
        self.ys = []
        self.cid = plt.gcf().canvas.mpl_connect('button_press_event', self)
    def __call__(self, event):
        print('click', event)
        if event.inaxes!=plt.gca(): return
        if event.dblclick==True: 
            print ('zoop!')
            plt.gcf().canvas.mpl_disconnect(self.cid)
            return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        try:
            self.poly = sg.polygon.Polygon(list(zip(self.xs, self.ys)))
            plt.gca().cla()
            plt.gca().add_patch(PolygonPatch(self.poly,
                          fc='red', ec='black',
                          linewidth=0.5, alpha=0.3))
        except ValueError:
            return


plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click to build polygons')
polyBuilder = PolyBuilder()



plt.close()

## how can we add onto the polygon?

p = list(zip(polyBuilder.xs, polyBuilder.ys))
q = sg.polygon.Polygon(p)

p = [(0, 0), (1, 1), (1, 0)]



import matplotlib.pyplot as plt
import numpy as np
plt.ion()

for i in range(50):
    y = np.random.random([10,1])
    plt.plot(y)
    plt.draw()

plt.gcf().gca().cla()

plt.gcf().gca().clear()

    plt.pause(0.0001)
    plt.clf()

def plotOne(poly, l=2, a=1.0, col='yellow'):
    fig = plt.figure()
    ax1 = plt.axes()
    ax1.set_xlim(min(poly.exterior.xy[0]), max(poly.exterior.xy[0]))
    ax1.set_ylim(min(poly.exterior.xy[1]), max(poly.exterior.xy[1]))
    ax1.set_aspect('equal')
    ax1.add_patch(PolygonPatch(poly,
                  fc=col, ec='black',
                  linewidth=l, alpha=a))

def addOne(poly, l=2, a=1.0, col='red'):
    ax1 = plt.gca()
    ax1.add_patch(PolygonPatch(poly,
                  fc=col, ec='black',
                  linewidth=l, alpha=a))

dir(sg.polygon.Polygon)

    ax1.add_patch(PolygonPatch(poly,
                  fc=col, ec='red',
                  linewidth=l, alpha=0.3))


fig, ax = plt.subplots()
ax.plot(np.random.rand(10))

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))

cid = fig.canvas.mpl_connect('button_press_event', onclick)
