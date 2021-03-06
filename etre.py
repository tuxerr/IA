#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
import interface
import iamap
import manager
import random
from iamap import *
from main import *
from interface import *
from manager import *

class Etre:

    def __init__(self,sprite,sprite_scale,position):
        self.qitem = interface.overviewWidgetGlobal.addItemToScene(sprite,position,sprite_scale)
        self.gender=random.choice(['F','M'])
        self.position=position
        self.etat='vivant'
        self.chemin=[]
        self.notMove=False

    def noMove(self):
        self.notMove=True

    def move(self,movement):
        i,j=self.position
        x,y=movement
        canGo=self.canGo((i+x,j+y))
        if canGo:
            interface.overviewWidgetGlobal.moveItem(self.qitem,movement)
            self.position=(i+x,j+y)
            iamap.matrixglobal[i][j].remove_have(self)
            iamap.matrixglobal[i][j].remove_property(self.typeObjet())
            iamap.matrixglobal[i+x][j+y].set_have(self)
            iamap.matrixglobal[i+x][j+y].set_property(self.typeObjet())
        return canGo
    
    def setPos(self,pos):
        i,j=self.position
        x,y=pos
        canGo=self.canGo(pos)
        if canGo:
            interface.overviewWidgetGlobal.setItemPos(self.qitem,pos)
            self.position=pos
            iamap.matrixglobal[i][j].remove_have(self)
            iamap.matrixglobal[i][j].remove_property(self.typeObjet())
            iamap.matrixglobal[x][y].set_have(self)
            iamap.matrixglobal[x][y].set_property(self.typeObjet())
        return canGo
    def mort(self):
        i,j=self.position
        self.etat='mort'
        interface.overviewWidgetGlobal.removeItem(self.qitem)
        iamap.matrixglobal[i][j].remove_have(self)
        iamap.matrixglobal[i][j].remove_property(self.typeObjet())
        manager.managerGlobal.removeEtre(self)
        if self.typeObjet()=="sheep":
            print("un sheep est mort")
        elif self.typeObjet()=="human":
            print("un humain est mort")
        elif self.typeObjet()=="wolf":
            print("un wolf est mort")
        else:
            print("ET est mort")
    def canGo(self,pos):
        i,j=pos
        canGo=False
        if (((i>0)&(j>0)&(i<len(iamap.matrixglobal))&(j<len(iamap.matrixglobal)))):
               canGo=((iamap.matrixglobal[i][j].cell_type=="beach")|(iamap.matrixglobal[i][j].cell_type=="land"))
        return canGo
