from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant

class TasksModel(QAbstractTableModel):
    def __init__(self, listOfTasks, dir):
        super(TasksModel, self).__init__()
        self.listOfTasks = sorted(listOfTasks)
        self.dir = dir

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.listOfTasks)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            tasks = self.listOfTasks[index.row()].split(self.dir)[1].split('/')[1]
            return tasks
        else:
            return QVariant()

    def get_data(self, index):
        return self.listOfTasks[index.row()]
