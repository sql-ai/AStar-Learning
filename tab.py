import sys
import traceback
import os
import glob
from gameScene import *

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qsci import *

tabform_class = uic.loadUiType("tab.ui")[0]

class Tab(QFrame, tabform_class):
    def __init__(self, algorithm, parent=None):
        if not algorithm in inserted_places:
            raise "Unknown algorithm"
        self.algorithm = algorithm

        QtWidgets.QFrame.__init__(self, parent)
        self.setupUi(self)

        # Setup display area
        self.scene = GameScene(self)
        self.layout = QVBoxLayout()
        self.displayFrame.setLayout(self.layout)
        self.layout.addWidget(self.scene)
        self.scene.start()

        # Setup starter code
        self.codeWidget.addTab(self.createEditor(), "yourCode.py")
        with open("search.py", "r") as f:
            data = f.readlines()
        begin, end = inserted_places[algorithm]
        starterCode = "".join(data[begin-1:end])
        self.codeWidget.widget(0).setText(starterCode);

        # Display other code
        for file in glob.glob("*.py"):
            self.codeWidget.addTab(self.createTextBox(file), file)

        # Debug console
        textBox0 = QTextEdit()
        textBox1 = QTextEdit()
        textBox0.setReadOnly(True)
        textBox1.setReadOnly(True)
        self.terminalWidget.addTab(textBox0, "Terminal")
        self.terminalWidget.addTab(textBox1, "Debug Console")

    def createEditor(self):
        #QScintilla Editor Setup
        editor = QsciScintilla()

        # Python Lexer
        # 1. Create a PYTHON lexer object
        lexer = QsciLexerPython(editor)

        # 2. Install the lexer onto your editor
        editor.setLexer(lexer)
        
        editor.setUtf8(True)  # Set encoding to UTF-8
        editor.setBaseSize(1, 1)
        #editor.setEolMode(QsciScintilla.EolUnix)

        # Indentation
        editor.setIndentationGuides(True)
        editor.setIndentationsUseTabs(False)
        editor.setTabWidth(4)
        editor.setAutoIndent(True)
        editor.setCaretForegroundColor(QColor("#ff0000ff"))
        
        # Margin 0 = Line number margin

        editor.setMarginType(0, QsciScintilla.NumberMargin)
        editor.setMarginWidth(0, "0000")
        editor.setMarginsForegroundColor(QColor("#ff888888"))

        # Autocompletion
        editor.setAutoCompletionCaseSensitivity(False)
        editor.setAutoCompletionReplaceWord(False)
        editor.setAutoCompletionSource(QsciScintilla.AcsDocument)
        editor.setAutoCompletionThreshold(1)

        return editor

    def createTextBox(self, filename):
        textBox = self.createEditor()
        textBox.setReadOnly(True)
        with open(filename, "r") as f:
            content = f.read()
        textBox.setText(content)
        return textBox

    def runCode(self):
        actions = []
        visited = []
        initialState = self.scene.gameState
        code = (self.codeWidget.widget(0).text())
        begin, end = inserted_places[self.algorithm]
        code = self.combineCode("search.py", begin, end, code)
        code += extraCode[self.algorithm]
        # print(code)
        # with open("tmp.py", "w") as f:
            # f.write(code)

        import util
        from gameState import Directions, Actions
        error_msg = ""
        try:
            exec(code, {'Directions': Directions, 'Actions':Actions, "util":util}, {'visited':visited, 'actions': actions, 'initialState': initialState})
        except SyntaxError as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            line_number = err.lineno
            error_msg = "{} at line {} of source string: {}".format(error_class, line_number, detail)
        except Exception as err:
            error_class = err.__class__.__name__
            detail = err.args[0]
            cl, exc, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            error_msg = traceback.format_exc()

        self.terminalWidget.widget(0).setText(error_msg)
        self.scene.setActions(actions)
        self.scene.setSearchPlan(visited)

    def combineCode(self, filename, lineStart, lineEnd, insertedCode):
        lineStart -= 1
        lineEnd -= 1
        inserted = [line + '\n' for line in insertedCode.splitlines()]
        # print(insertedCode)
        # print(inserted)

        with open(filename, "r") as f:
            data = f.readlines()
        del data[lineStart:lineEnd+1]
        data[lineStart:lineStart] = inserted
        return "".join(data)

# Place in search.py to insert user's code into
inserted_places = {
    "dfs": (146, 150),
    "bfs": (152, 156),
    "astar": (182, 187),
    "adverserial": (189, 193)
}

# Code to append to search.py to test user's implementation
extraCode = {
    "dfs" : '''
prob = PositionSearchProblem(initialState, start=initialState.getPacmanPos(), goal=(1,1))
actions.extend(dfs(prob))
visited.extend(prob.visitedlist)
print(actions)
''',
    "bfs":'''
prob = PositionSearchProblem(initialState, start=initialState.getPacmanPos(), goal=(1,1))
actions.extend(bfs(prob))
visited.extend(prob.visitedlist)
print(actions)
''',
    "astar":'''
prob = PositionSearchProblem(initialState, start=initialState.getPacmanPos(), goal=(1,1))
actions.extend(aStarSearch(prob))
visited.extend(prob.visitedlist)
print(actions)
''',
    "adverserial":'''
prob = PositionSearchProblem(initialState, start=initialState.getPacmanPos(), goal=(1,1))
actions.extend(adverserialSearch(prob))
visited.extend(prob.visitedlist)
print(actions)
'''
}