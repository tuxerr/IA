#!/usr/bin/python
# -*- coding: utf-8 -*-

# fichier définissant l'interface générale
import sys
from PyQt4 import QtGui, QtCore

class Interface(QtGui.QMainWindow):
    
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        super().__init__()
        self.initUI()

    def getAppHandle(self):
        return self.app
        
    def initUI(self):               
        self.setWindowTitle('Projet IA')    
        self.toolbar = self.addToolBar('General Toolbar')

        # add all toolbar buttons defined in initToolbarActions
        actionList = self.initToolbarActions()
        for action in actionList:
            self.toolbar.addAction(action)

        self.setGeometry(0,0, 800, 600)
        self.show()

    def initToolbarActions(self):

        actionList = [];

        exitAction = QtGui.QAction(QtGui.QIcon('resources/exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)

        confAction = QtGui.QAction(QtGui.QIcon('resources/settings.png'), 'Configuration', self)
        confAction.setShortcut('Ctrl+C')
        confAction.triggered.connect(self.popConfigurationWindow)

        runAction = QtGui.QAction(QtGui.QIcon('resources/run.png'), 'Run simulation', self)
        runAction.setShortcut('Ctrl+R')
        runAction.triggered.connect(self.popConfigurationWindow)

        actionList.append(exitAction);
        actionList.append(confAction);
        actionList.append(runAction);
        return actionList;

    def popConfigurationWindow(self):
        self.confWidget = ConfigurationWidget()


class ConfigurationWidget(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('World Configuration')
        
        taux_arbres_label = QtGui.QLabel('Taux d\'arbres')
        taux_animaux_label = QtGui.QLabel('Taux d\'animaux')
        
        # configuration has a grid layout
        grid = QtGui.QGridLayout()
        self.grid = grid

        grid.addWidget(taux_arbres_label,1,0)
        grid.addWidget(taux_animaux_label,2,0)
        
        self.setLayout(grid)

        self.setGeometry(200,200,400,600)
        self.show()
        
