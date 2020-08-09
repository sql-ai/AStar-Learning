import sys
from gameScene import *
from tab import *

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qsci import *

form_class = uic.loadUiType("pacman.ui")[0]

class MainWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))

        self.setWindowTitle("User: Bill Gates -  Introduction to Artificial Intelligence - Lesson 3: Agent planning")
        self.setCentralWidget(self.tabWidget)

        # Each problem will be on a seperate tab
        self.problem1 = Tab("dfs", self)
        self.tabWidget.addTab(self.problem1, "Depth-first Search")

        self.problem2 = Tab("bfs", self)
        self.tabWidget.addTab(self.problem2, "Breadth-first Search")

        self.problem3 = Tab("astar", self)
        self.tabWidget.addTab(self.problem3, "A* Search")

        self.problem4 = Tab("adverserial", self)
        self.tabWidget.addTab(self.problem4, "Multi-agent Search")

    def runCode(self):
        currentTabId = self.tabWidget.currentIndex()
        self.tabWidget.widget(currentTabId).runCode()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.runCode()
            currentTabId = self.tabWidget.currentIndex()
            self.tabWidget.widget(currentTabId).scene.gameState.restart()

        if event.key() == Qt.Key_Escape:
            self.close()

app = QtWidgets.QApplication(sys.argv)
myWindow = MainWindow()
myWindow.setFixedSize(1900, 1300)
myWindow.show()
app.exec_()