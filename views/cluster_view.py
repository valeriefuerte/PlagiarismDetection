from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import numpy as np
from models.model import Model

class PlotCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 1, height = 1, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi,facecolor="white")
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.ax = self.figure.add_subplot(111)

    def plot(self, x):
        self.ax.clear()
        mds = MDS(n_components=2, dissimilarity="precomputed")
        pos = mds.fit(x).embedding_

        self.ax.scatter(pos[:, 0], pos[:, 1], color='darkcyan')
        self.draw()
