#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import interface
import iamap
from iamap import *
from main import *
from interface import *

class Etre:
    def __init__(self,sprite,position):
        self.qitem = interface.overviewWidgetGlobal.addItemToScene(sprite,position)
        self.position=position
        
    def move(self,movement):
        i,j=self.position
        x,y=movement
        if self.canGo((i+x,j+y)):
            interface.overviewWidgetGlobal.moveItem(self.qitem,movement)
            self.position=(i+x,j+y)
            iamap.matrixglobal[i][j].remove_have(self)
            iamap.matrixglobal[i][j].remove_property("animaux")
            iamap.matrixglobal[i+x][j+y].set_have(self)
            iamap.matrixglobal[i+x][j+y].set_property("animaux")
            
    def setPos(self,pos):
        i,j=self.position
        x,y=pos
        if self.canGo(pos):
            interface.overviewWidgetGlobal.setItemPos(self.qitem,pos)
            self.position=pos
            iamap.matrixglobal[i][j].remove_have(self)
            iamap.matrixglobal[i][j].remove_property("animaux")
            iamap.matrixglobal[x][y].set_have(self)
            iamap.matrixglobal[x][y].set_property("animaux")
    def canGo(self,pos):
        i,j=pos
        canGo=False
        if (((i>0)&(j>0)&(i<len(iamap.matrixglobal))&(j<len(iamap.matrixglobal)))):
               canGo=((iamap.matrixglobal[i][j].cell_type=="beach")|(iamap.matrixglobal[i][j].cell_type=="land"))
        return canGo
