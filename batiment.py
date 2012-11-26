from human import *

class Batiment:

    def __init__(self, position):
        self.position = position
        self.fillinFood = 0
        self.fillinWood = 0
        self.fillinHuman = 0
        self.capacityFood = 0
        self.capacityWood = 0
        self.capacityHuman = 0

    def sortirRessource(self, aSortir, nombre):
        if (aSortir == "food"):
            res = self.fillinFood
            if (nombre > res):
                self.fillinFood = 0
            else:
                self.fillinFood = res - nombre
                res = nombre
        elif (aSortir == "wood"):
            res = self.fillinWood
            if (nombre > res):
                self.fillinWood = 0
            else:
                self.fillinWood = res - nombre
                res = nombre
        else:
            res = -1
        return res
    
   def rentrerRessource(self, aRentrer, nombre):
        if (aRentrer == "food"):
            res = self.capacityFood - self.fillinFood
            if (nombre > res):
                self.fillinFood = self.capacityFood
            else:
                self.fillinFood = self.fillinFood + nombre
                res = nombre
        elif (aSortir == "wood"):
            res = self.capacityWood - self.fillinWood
            if (nombre > res):
                self.fillinWood = self.capacityWood
            else:
                self.fillinFood = self.fillinWood + nombre
                res = nombre
        else:
            res = -1
        return res

   def sortir(self, human):
        if (human.isIn == True):
            human.isOut = False
            res = 1
        else:
            res = -1
        return res

    def rentrer(self, human):
        if (human.isIn == False):
            human.isOut = True
            res = 1
        else:
            res = -1
        return res
        
class CentreVille(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.type = "centreVille"
        self.capacityFood = 20 #arbitraire
        self.capacityWood = 20 #arbitraire
        self.capacityHuman = 10 #arbitraire


class StockageBois(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.type = "stockageBois"
        self.capacityWood = 30 #arbitraire


class StockageNourriture(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.type = "stockageNourriture"
        self.capacityFood = 30 #arbitraire


class Abri(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.type = "abri"
        self.capacityHuman = 10 #arbitraire
