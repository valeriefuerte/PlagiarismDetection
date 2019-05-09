import fnmatch
import os
from pandas import read_csv

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QVBoxLayout

from models.tasksModel import TasksModel
from models.studentsModel import StudentsModel

from views.mainWindow_ui import Ui_MainWindow
from views.cluster_view import PlotCanvas

class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.clusterView = PlotCanvas(self, width=1, height=1, dpi=100)
        layout = QVBoxLayout(self._ui.clusterWidget)
        layout.addWidget(self.clusterView)

        self.listOfTasks = list()
        self.studentsList = list()
        self.studentsDir = list()
        self.studentsTasks = list()

        self.activeTheme = 0
        self.activeDistance = 0
        self.currentFile = ''
        self.initUI()
        self.con()


    def initUI(self):
        self.statusBar().showMessage('Ready')

        openFile = QAction(QIcon('open.png'), 'Открыть', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Открыть директорию')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('Файл')
        fileMenu.addAction(openFile)

        self._ui.distanceComboBox.addItem("Левенштейна")
        self._ui.distanceComboBox.addItem("Жаккара")

    def con(self):
        self._ui.themeComboBox.currentIndexChanged.connect(self.themeComboBoxChanged)
        self._ui.distanceComboBox.currentIndexChanged.connect(self.distanceComboBoxChanged)
        self._ui.studentsTableView.clicked.connect(self.studentsTableViewClicked)
        self._ui.tasksTableView.clicked.connect(self.tasksTableViewClicked)

    def showDialog(self):
        dir = str(QFileDialog.getExistingDirectory(self, 'Выберите папкy', '/home/valerie/University/Diploma/Math-packages-course-automatization/mp2017-collect'))
        if dir:
            self._model.setDirectory(dir)
            self.statusBar().showMessage(dir)
            self.listOfTasks = sorted(getListOfFiles(dir, "*.m"))
            #print("listOfTasks")
            #print(self.listOfTasks)
            theme = self.listOfTasks[0].split(dir)[1].split('/')[1]
            self._model.setTheme(theme)
            i = 0
            while(i < len(self.listOfTasks)):
                self._ui.themeComboBox.addItem(self.listOfTasks[i].split(dir)[1].split('/')[1])
                i = i + 1

            self.showStudents(self.listOfTasks[0])

    def showStudents(self, dir):
        self.studentsDir = getListOfFiles(dir, "*.m")
        studentsList = list(list())
        for i in range(len(self.studentsDir)):
            files = os.listdir(self.studentsDir[i])
            for entry in files:
                if fnmatch.fnmatch(entry, '*.txt'):
                    studentsList.insert(i, [entry.split("STUDENT - ")[1].split(".txt")[0], self.studentsDir[i]])

        self.studentsList = sorted(studentsList)
        #print(self.studentsList)
        self.studentsModel = StudentsModel(self.studentsList)
        self._ui.studentsTableView.setModel(self.studentsModel)
        self._ui.studentsTableView.horizontalHeader().hide()
        self._ui.studentsTableView.horizontalHeader().setStretchLastSection(True)

    def themeComboBoxChanged(self, i):
        self.studentsList.clear()
        self._ui.programPlainTextEdit.clear()
        self.showStudents(self.listOfTasks[i])
        self.activeTheme = i
        theme = self.listOfTasks[i].split(self._model.getDirectory())[1].split('/')[1]
        self._model.setTheme(theme)

    def studentsTableViewClicked(self, i):
        index = self._ui.studentsTableView.selectedIndexes()[0].row()
        self._ui.programPlainTextEdit.clear()
        self.studentsTasks.clear()
        self.studentsTasks = sorted(getListOfFiles(self.studentsList[index][1], "*.m"))

        self.tasksModel = TasksModel(self.studentsTasks, self.studentsList[index][1])
        self._ui.tasksTableView.setModel(self.tasksModel)
        self._ui.tasksTableView.horizontalHeader().hide()
        self._ui.tasksTableView.horizontalHeader().setStretchLastSection(True)

    def tasksTableViewClicked(self, i):
        # debug canvas

        # self.clusterView.debug()

        # end debug canvas

        index = self._ui.tasksTableView.selectedIndexes()[0].row()
        self.currentFile = self.studentsTasks[index]
        self._ui.programPlainTextEdit.clear()
        self._ui.programPlainTextEdit.setPlainText(getText(self.currentFile))

        self._model.setTask(self.currentFile.split(self._model.getDirectory())[1].split(self._model.getTheme())[1].split('/')[2])

        self.countDistance(self.activeDistance)

        self.viewSameStudents(self._ui.studentsTableView.selectedIndexes()[0].row(), self.activeDistance)

        listOfTokens = self._model.getTokens()
        self.findLoops(listOfTokens[index])

    def countDistance(self, i):
        directory = self._model.getDirectory()
        problem = self._model.getTheme()
        task = self._model.getTask()
        if(directory):
            if(problem):
                if(task):
                    dirName = directory + "/" + problem
                    listOfFiles = getListOfFiles(dirName, "*.m")
                    #print(task)
                    #print(listOfFiles)
                    self._main_controller.countDistance(listOfFiles, task, self.studentsList, i)
                    #print(self._model.getDistance())
                    #self.clusterView = PlotCanvas(self, width=1, height=1, dpi=100)
                    self.clusterView.plot(self._model.getDistance())
                    #self.clusterView._update_dpi()
        #print(dirName)

    def distanceComboBoxChanged(self, i):
        self.activeDistance = i
        print(self.activeDistance)
        self.countDistance(self.activeDistance)

    def viewSameStudents(self, index, d):
        print(index)

        if(d == 0):
            df = read_csv('distance.csv', usecols=[0])
            listOfDistances = df.values
            print(listOfDistances)

    def findLoops(self, tokens):
        countF = 0
        countW = 0
        countR = 0
        for i in range(len(tokens)):
            t = tokens[i][1]
            if t == 'for':
                countF += 1
                print("For loop")
            if t == 'while':
                countW += 1
                print("While loop")
            if t == 'repeat':
                countR += 1
                print("Repeat loop")
        if(countF == 0 & countW == 0 & countR == 0):
            print("No loop")




'''
        # listen for model event signals
        self._model.amount_changed.connect(self.on_amount_changed)
        self._model.even_odd_changed.connect(self.on_even_odd_changed)
        self._model.enable_reset_changed.connect(self.on_enable_reset_changed)
'''

def getListOfFiles(dirName, pattern):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()

    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath) & fnmatch.fnmatch(entry, pattern):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

def getText(dir):
    try:
        if os.path.exists(dir) and os.path.getsize(dir) > 0:
            with open(dir, 'r', encoding="latin-1") as the_file:
                text = the_file.read()
                return text
    except IOError:
        print("Can't read files!")
