import sys
import random

from gameState import *

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

BACKGROUND_COLOR = QColor(0x000000)

DEFAULT_GRID_SIZE = 30

MAX_MAZE_WIDTH = 870
MAX_MAZE_HEIGHT = 800
WALL_COLOR = QColor(0x0033FF)

PACMAN_SIZE = 9
PACMAN_COLOR = QColor(0xFFFF3D)
PACMAN_SPEED = 10

# Food
FOOD_COLOR = QColor(0xFFFFFF)
FOOD_SIZE = 5

# Path
PATH_COLOR = QColor(0xFF0000)

# Score
SCORE_COLOR = PACMAN_COLOR
SCORE_SIZE = 10
SCORE_OFFSET = QPointF(100, 850)
SEARCH_OFFSET = QPointF(550, 850)
# fps
FPS = 10

class GameScene(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateScene)

        self.gameState = LoadGameState(".\\layouts\\bigCorners.lay")
        w, h = self.gameState.getSize()
        self.gridSize = int(min(MAX_MAZE_WIDTH / w, MAX_MAZE_HEIGHT / h))
        self.gridSize = min(self.gridSize, DEFAULT_GRID_SIZE)
        self.mazeOffset = (MAX_MAZE_HEIGHT/2 - h/2*self.gridSize, MAX_MAZE_WIDTH/2 - w/2*self.gridSize)
        # self.mazeOffset = (0, 870)
        self.remainingActions = []
        self.visitedlist = []
        self.setFocusPolicy(Qt.StrongFocus)


    def start(self):
        self.timer.start(1000 / FPS)

    remainingFrame = FPS
    def updateScene(self):
        if len(self.visitedlist) > 0:
            self.update()
            return None

        if len(self.remainingActions) > 0:
            dir = Actions.directionToVector(self.remainingActions[0])
            v = (PACMAN_SPEED * dir[0] / FPS, PACMAN_SPEED * dir[1] / FPS)
            self.gameState.movePacman(v)

            GameScene.remainingFrame -= PACMAN_SPEED 
            if GameScene.remainingFrame <= 0:
                GameScene.remainingFrame = FPS
                self.remainingActions.pop(0)
            if len(self.remainingActions) == 0:
                self.gameState.score += 500
        self.update()

    def extendActions(self, actions):
        self.remainingActions.extend(actions)
    
    def setActions(self, actions):
        self.remainingActions = actions

    def setSearchPlan(self, visitedlist):
        self.visitedlist = visitedlist

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up:
            self.setActions([Directions.NORTH])
        elif key == Qt.Key_Down:
            self.setActions([Directions.SOUTH])
        elif key == Qt.Key_Left:
            self.setActions([Directions.WEST])
        elif key == Qt.Key_Right:
            self.setActions([Directions.EAST])

        return super().keyPressEvent(event)


    def paintEvent(self, a0):
        painter = QPainter(self)
        # fill background
        rect = self.contentsRect()
        painter.fillRect(rect, BACKGROUND_COLOR)
        self.drawSearchPath(painter)
        painter.fillRect(rect, BACKGROUND_COLOR)
        self.drawSearchPath(painter)
        # draw maze
        self.drawWalls(painter, self.gameState.getWalls())
        # draw food
        self.drawFood(painter, self.gameState.getFood())
        # draw pacman
        self.drawPacman(painter, self.gameState.getPacmanPos(), 0)
        # draw score
        self.drawScore(painter)
    
    def drawSearchPath(self, painter):
        if len(self.visitedlist) > 0:
            x, y = self.visitedlist[0]
            self.visitedlist.pop(0)
            self.gameState.searchCost += 1
            painter.fillRect(self.mazeOffset[1]+y*self.gridSize, self.mazeOffset[0]+x*self.gridSize, self.gridSize, self.gridSize, PATH_COLOR)

    def drawScore(self, painter):
        painter.setPen(SCORE_COLOR)
        painter.setFont(QFont('Decorative', 20, 20))
        painter.drawText(SCORE_OFFSET, "Score: {}".format(self.gameState.score))
        painter.drawText(SEARCH_OFFSET, "Seach cost: {}".format(self.gameState.searchCost))

    def drawWalls(self, painter, wallMatrix):
        wallColor = WALL_COLOR
        for x, row in enumerate(wallMatrix):
            for y, cell in enumerate(row):
                if cell:
                    painter.fillRect(self.mazeOffset[1]+y*self.gridSize, self.mazeOffset[0]+x*self.gridSize, self.gridSize, self.gridSize, wallColor)

    def drawFood(self, painter, foodMatrix):
        painter.setBrush(FOOD_COLOR)
        s = self.gridSize
        for x, row in enumerate(foodMatrix):
            for y, cell in enumerate(row):
                if cell:
                    center = QPoint(self.mazeOffset[1], self.mazeOffset[0])
                    center += QPoint(y*s + s//2, x*s + s//2)
                    painter.drawEllipse(center, FOOD_SIZE, FOOD_SIZE)

    pacmanOpenMouth = 0
    def drawPacman(self, painter, pos, dir, animate=True):
        s = self.gridSize
        center = QPoint(self.mazeOffset[1] + pos[1]*s + s//2, self.mazeOffset[0] + pos[0]*s + s//2)
        painter.setBrush(PACMAN_COLOR)
        painter.drawEllipse(center, PACMAN_SIZE, PACMAN_SIZE)

        if animate:
            GameScene.pacmanOpenMouth ^= 1
        
        p1, p2 = self.getMouthPoints(center, self.gameState.getPacmanDir())
        # p1 = center + QPoint(s//2, -s//2)
        # p2 = center + QPoint(s//2, s//2)
        # if not GameScene.pacmanOpenMouth:
        #     p1 = center + QPoint(s//2, -s//8)
        #     p2 = center + QPoint(s//2, s//8)
        painter.setBrush(BACKGROUND_COLOR)
        painter.drawPolygon(center, p1, p2)

    def getMouthPoints(self, center, dir):
        p1, p2 = None, None
        s = self.gridSize
        o = 8
        if GameScene.pacmanOpenMouth:
            o = 2

        if dir == Directions.EAST:
            p1 = center + QPoint(s//2, -s//o)
            p2 = center + QPoint(s//2, s//o)
        elif dir == Directions.WEST:
            p1 = center + QPoint(-s//2, s//o)
            p2 = center + QPoint(-s//2, -s//o)
        elif dir == Directions.NORTH:
            p1 = center + QPoint(-s//o, -s//2)
            p2 = center + QPoint(s//o, -s//2)
        elif dir == Directions.SOUTH:
            p1 = center + QPoint(s//o, s//2)
            p2 = center + QPoint(-s//o, s//2)
        return (p1, p2)