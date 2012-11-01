#!/usr/bin/python
# -*- coding: utf-8 -*-

# fichier définissant l'interface générale
import sys
from PyQt4 import QtGui, QtCore

class Interface(QtGui.QMainWindow):
    
    def __init__(self,conf):
        self.app = QtGui.QApplication(sys.argv)
        super().__init__()
        self.initUI()
        self.conf = conf

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
        self.confWidget = ConfigurationWidget(self.conf)


class ConfigurationWidget(QtGui.QWidget):
    def __init__(self,conf):
        super().__init__()
        self.conf = conf
        self.initUI()

    def initUI(self):
        self.setWindowTitle('World Configuration')

        validator = QtGui.QIntValidator(0,100)
        
        taux_arbres_label = QtGui.QLabel('Taux d\'arbres (%)')
        taux_animaux_label = QtGui.QLabel('Taux d\'animaux (%)')

        taux_arbres_edit = QtGui.QLineEdit(str(self.conf['taux_arbres']))
        taux_arbres_edit.setValidator(validator)
        taux_arbres_edit.textChanged[str].connect(self.taux_arbres_changevalue)

        taux_animaux_edit = QtGui.QLineEdit(str(self.conf['taux_animaux']))
        taux_animaux_edit.setValidator(validator)
        taux_animaux_edit.textChanged[str].connect(self.taux_animaux_changevalue)
        
        # configuration has a grid layout
        grid = QtGui.QGridLayout()
        self.grid = grid

        grid.addWidget(taux_arbres_label,1,0)
        grid.addWidget(taux_arbres_edit,1,1)
        grid.addWidget(taux_animaux_label,2,0)
        grid.addWidget(taux_animaux_edit,2,1)
        
        self.setLayout(grid)

        self.setGeometry(200,200,50,200)
        self.show()

    def taux_arbres_changevalue(self,new_val):
        if new_val != "":
            self.conf["taux_arbres"]=int(new_val)
            print(self.conf)

    def taux_animaux_changevalue(self,new_val):
        if new_val != "":
            self.conf["taux_animaux"]=int(new_val)
            print(self.conf)
