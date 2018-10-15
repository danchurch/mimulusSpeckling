from matplotlib import pyplot as plt
from shapely import geometry as sg
from descartes import PolygonPatch

class LineBuilder:
    def __init__(self, line, poly):
        self.popped = False
        self.line = line
        self.poly = poly
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
    def __call__(self, event):
        print('click', event)
        if event.inaxes!=self.line.axes: return
        if not self.popped: 
            self.xs.pop(0)
            self.ys.pop(0)
            self.popped=True
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
        pts = list(zip(linebuilder.xs, linebuilder.ys))
        try:
                self.poly = sg.polygon.Polygon(pts)
        except ValueError:
            return


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click to build line segments')
line, = ax.plot([0], [0])  # empty line
poly = sg.polygon.Polygon()
linebuilder = LineBuilder(line, poly)

addOne(linebuilder.poly, a=0.3)

plt.close()

## how can we add onto the polygon?

p = list(zip(linebuilder.xs, linebuilder.ys))
q = sg.polygon.Polygon(p)

p = [(0, 0), (1, 1), (1, 0)]



import matplotlib.pyplot as plt
import numpy as np
plt.ion()
for i in range(50):
    y = np.random.random([10,1])
    plt.plot(y)
    plt.draw()
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


