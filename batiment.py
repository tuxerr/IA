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

    def peutContenir(self, ressource):
        res = False
        if (ressource == "food"):
            res = (self.capacityFood != 0)
        elif (ressource == "wood"):
            res = (self.capacityWood != 0)
        elif (ressource == "human"):
            res = (self.capacityHuman != 0)
        else:
            print("peutContenir : ressource inconnue")
        return res

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
        

class Forum(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.capacityFood = 20 #arbitraire
        self.capacityWood = 20 #arbitraire
        self.capacityHuman = 10 #arbitraire

    def typeBatiment(self):
        return 'forum'


class StockageBois(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.capacityWood = 30 #arbitraire

    def typeBatiment(self):
        return 'stockageBois'


class StockageNourriture(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.capacityFood = 30 #arbitraire

    def typeBatiment(self):
        return 'stockageNourriture'


class Abri(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.capacityHuman = 10 # arbitraire

    def typeBatiment(self):
        return 'abri'


class Chaudron(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.capacityFood = 10 # arbitraire
        
    def typeBatiment(self):
        return 'chaudron'

class Ferme(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.capacityFood = 10 # arbitraire
        self.tour = 0
        self.tourMax = 9 # arbitraire

    def typeBatiment(self):
        return 'ferme'

    def cultive(self):
        self.tour += 1
        if (self.tour > tourMax):
            self.fillinFood += 1
            self.tour = 0
            
    def recolte(self):
        res = self.fillinFood 
        self.fillinFood = 0
        return res
