import fnmatch
import os
from pandas import read_csv

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QVBoxLayout

from models.tasksModel import TasksModel
from models.studentsModel import StudentsModel
from models.similarStudentsModel import SimilarStudentsModel
from views.mainWindow_ui import Ui_MainWindow
from views.cluster_view import PlotCanvas

class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        self.setWindowTitle("Автоматизация анализа массива решений заданий по программированию, включая анализ на плагиат")
        #self.setWindowIcon(QIcon('icon.png'))

        self.clusterView = PlotCanvas(self, width=1, height=1, dpi=100)
        layout = QVBoxLayout(self._ui.clusterWidget)
        layout.addWidget(self.clusterView)

        self.listOfTasks = list()
        self.studentsList = list()
        self.studentsDir = list()
        self.studentsTasks = list()

        self.activeTheme = 0
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

        #self.studentsList = sorted(studentsList)
        self.studentsList = studentsList
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
        index = self._ui.tasksTableView.selectedIndexes()[0].row()
        self.currentFile = self.studentsTasks[index]
        self._ui.programPlainTextEdit.clear()
        self._ui.programPlainTextEdit.setPlainText(getText(self.currentFile))

        self._model.setTask(self.currentFile.split(self._model.getDirectory())[1].split(self._model.getTheme())[1].split('/')[2])

        activeDistance = self._model.getActiveDistance()
        self.countDistance(activeDistance)

        self.viewSimilarStudents(self._ui.studentsTableView.selectedIndexes()[0].row(), activeDistance)

        listOfTokens = self._model.getTokens()
        i = self._ui.studentsTableView.selectedIndexes()[0].row()
        #print(listOfTokens[i])
        self.findLoops(listOfTokens[i])


    def countDistance(self, i):
        directory = self._model.getDirectory()
        problem = self._model.getTheme()
        task = self._model.getTask()
        if directory:
            if problem:
                if task:
                    dirName = directory + "/" + problem
                    listOfFiles = getListOfFiles(dirName, "*.m")
                    self._main_controller.countDistance(listOfFiles, task, self.studentsList, i)
                    d = self._model.getDistance()
                    #print(d)
                    self.clusterView.plot(d)


    def distanceComboBoxChanged(self, i):
        self._model.setActiveDistance(i)
        activeDistance = self._model.getActiveDistance()
        self.countDistance(activeDistance)
        if self._ui.studentsTableView.selectedIndexes() != []:
            self.viewSimilarStudents(self._ui.studentsTableView.selectedIndexes()[0].row(), activeDistance)


    def viewSimilarStudents(self, index, d):
        listOfSimilar = list(list())
        if d == 0:
            df = read_csv('distance.csv', usecols=[index])
        if d == 1:
            df = read_csv('distanceJaccard.csv', usecols=[index])
        listOfDistances = df.values
        for i in range(len(listOfDistances)):
            listOfSimilar.insert(i, [self.studentsList[i][0], listOfDistances[i][0]])

        ss = sorted(listOfSimilar, key=lambda student: student[1])

        self.similarStudentsModel = SimilarStudentsModel(ss)
        self._ui.similarTableView.setModel(self.similarStudentsModel)
        self._ui.similarTableView.horizontalHeader().hide()
        self._ui.similarTableView.horizontalHeader().setStretchLastSection(True)


    def findLoops(self, tokens):
        countF = 0
        countW = 0
        countR = 0
        #print(tokens)
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
            if t == 'rep':
                countR += 1
                print("Repeat loop")
            if t == 'repmat':
                countR += 1
                print("Repeat loop")
        #if(countF == 0 & countW == 0 & countR == 0):
            #print("No loop")
        yesStr = "Встречаются"
        noStr = "Не встречаются"

        if countF != 0:
            self._ui.forLineEdit.setText(yesStr)
        else:
            self._ui.forLineEdit.setText(noStr)
        if countW != 0:
            self._ui.whileLineEdit.setText(yesStr)
        else:
            self._ui.whileLineEdit.setText(noStr)
        if countR != 0:
            self._ui.repeatLineEdit.setText(yesStr)
        else:
            self._ui.repeatLineEdit.setText(noStr)


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
