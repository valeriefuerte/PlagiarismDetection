from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant

class SimilarStudentsModel(QAbstractTableModel):
    def __init__(self, listOfSimilar):
        super(SimilarStudentsModel, self).__init__()
        self.listOfSimilar = listOfSimilar

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.listOfSimilar)

    def columnCount(self, parent=None, *args, **kwargs):
        return 2

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            a = self.listOfSimilar[index.row()][0]
            b = str(self.listOfSimilar[index.row()][1])
            if index.column() == 0:
                return a
            else:
                return b
        else:
            return QVariant()
