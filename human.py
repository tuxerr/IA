import random
import iamap
import manager
from iamap import *
from manager import *

class Human(Etre):

    def __init__(self, position):
        super().__init__("resources/water_carrier.png",0.4,position)

    def run(self):
        print("run")
