from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import numpy as np
from models.model import Model

class PlotCanvasOld(FigureCanvas):
    def __init__(self, parent = None, width = 1, height = 1, dpi = 100):
        fig, _ = plt.subplots(nrows=2, ncols=2) #верхний объект Figure
        # print("figure: {}, type = {}".format(fig, type(fig)))
        self.fig = fig
        # one_tick = fig.axes[0].yaxis.get_major_ticks()[0]
        #print(one_tick)


        #fig = Figure(figsize=(width, height), dpi=dpi,facecolor="white")
        #self.axes = fig.add_subplot(111)
        x = np.array([[0, 11, 9,  12, 4,  9,  4,  10, 9,  16],
             [11, 0,  12, 19, 14, 12, 14, 6,  3,  13],
             [9,  12, 0,  15, 10, 0,  10, 11, 10, 17],
             [12, 19, 15, 0,  13, 15, 13, 18, 17, 11],
             [4,  14, 10, 13, 0,  10, 0,  13, 12, 19],
             [9,  12, 0,  15, 10, 0,  10, 11, 10, 17],
             [4,  14, 10, 13, 0,  10, 0,  13, 12, 19],
             [10, 6,  11, 18, 13, 11, 13, 0,  4,  13],
             [9,  3,  10, 17, 12, 10, 12, 4,  0,  11],
             [16, 13, 17, 11, 19, 17, 19, 13, 11, 0]])

        FigureCanvas.__init__(self, fig)
        d = Model().getDistance()
        if(d):
            self.plot(d)
        else:
            self.plot(x)

        #self.setParent(parent)
        #FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        #FigureCanvas.updateGeometry(self)

        #self.plot()

    def plot(self, x):
        #x = np.array(str)
        #print(x)
        #print(x.shape)
        #embedding = MDS(n_components=2)
        #X_transformed = embedding.fit_transform(x[:25], dissimilarity=='precomputed')
        mds = MDS(n_components=2, dissimilarity="precomputed")
        pos = mds.fit(x).embedding_
        #print(pos[:, 0])
        plt.scatter(pos[:, 0], pos[:, 1], color='turquoise')
        plt.title("MDS")
        #self.axes.contourf(x,y,100, cmap=plt.cm.gnuplot,vmax=np.max(y), vmin=np.min(y))

    def debug(self):
        # plt.figure(self.fig)
        print("debug cluster view")
        plt.clf()
        plt.subplot(2, 2, 1)
        plt.scatter([1, 2, 3], [5, 3, 4])
        self


class PlotCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 1, height = 1, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi,facecolor="white")
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        x = np.array([[0, 11, 9,  12, 4,  9,  4,  10, 9,  16],
             [11, 0,  12, 19, 14, 12, 14, 6,  3,  13],
             [9,  12, 0,  15, 10, 0,  10, 11, 10, 17],
             [12, 19, 15, 0,  13, 15, 13, 18, 17, 11],
             [4,  14, 10, 13, 0,  10, 0,  13, 12, 19],
             [9,  12, 0,  15, 10, 0,  10, 11, 10, 17],
             [4,  14, 10, 13, 0,  10, 0,  13, 12, 19],
             [10, 6,  11, 18, 13, 11, 13, 0,  4,  13],
             [9,  3,  10, 17, 12, 10, 12, 4,  0,  11],
             [16, 13, 17, 11, 19, 17, 19, 13, 11, 0]])

        self.ax = self.figure.add_subplot(111)

        # d = Model().getDistance()
        # if(d):
        #     self.plot(d)
        # else:
        self.plot(x)

    def plot(self, x):
        mds = MDS(n_components=2, dissimilarity="precomputed")
        pos = mds.fit(x).embedding_

        self.ax.scatter(pos[:, 0], pos[:, 1], color='turquoise')
        self.draw()


    def debug(self):
        # plt.figure(self.fig)
        print("debug cluster view")
        self.ax.clear()
        self.ax.scatter([1, 2, 3], [5, 3, 4])
        self.draw()
