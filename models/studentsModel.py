from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant

class StudentsModel(QAbstractTableModel):
    def __init__(self, studentsList):
        super(StudentsModel, self).__init__()
        self.studentsList = studentsList

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.studentsList)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            students = self.studentsList[index.row()][0]
            return students
        else:
            return QVariant()
