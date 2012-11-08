#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from iamap import *
from main import *
import interface

class Etre:
    
    def __init__(self,sprite,position):
        self.qitem = interface.overviewWidgetGlobal.addItemToScene(sprite,position)

    def move(self,movement):
        overviewWidgetGlobal.moveItem(self.qitem,movement)

    def setPos(self,pos):
        overviewWidgetGlobal.setItemPos(self.qitem,pos)
