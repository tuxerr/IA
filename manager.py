import sys
from PyQt4 import QtCore
from etre import *
global managerGlobal
class Manager():
    def __init__(self):
        global managerGlobal
        self.timer=QtCore.QTimer()
        QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"),self.runEtres)
        self.timeout=200
        self.listeEtres=[];
        managerGlobal=self
        
    def startSimulation(self):
        self.timer.start(self.timeout)

    def stopSimulation(self):
        self.timer.stop()

    def runEtres(self):
        for etre in self.listeEtres:
            etre.run()

    def addEtre(self,etre):
        self.listeEtres.append(etre)

    def removeEtre(self,etre):
        self.listeEtres.remove(etre)

        
