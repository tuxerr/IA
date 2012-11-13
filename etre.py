#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import interface
from iamap import *
from main import *
from interface import *

class Etre:
    def __init__(self,sprite,position):
        self.qitem = interface.overviewWidgetGlobal.addItemToScene(sprite,position)
        self.position=position
    def move(self,movement):
        interface.overviewWidgetGlobal.moveItem(self.qitem,movement)
        self.position[0]=self.position[0]+movement[0]
        self.position[1]=self.position[1]+movement[1]
    
    def setPos(self,pos):
        interface.overviewWidgetGlobal.setItemPos(self.qitem,pos)
        self.position=pos