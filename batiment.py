from human import *
from interface import *
from iamap import *

class Batiment:

    def __init__(self, position):
        self.position = position
        self.fillinFood = 0
        self.fillinWood = 0
        self.fillinHuman = 0
        self.capacityFood = 0
        self.capacityWood = 0
        self.capacityHuman = 0
        self.tourConstruction = 0
        self.tourConsructionMax = 24 # arbitraire
        
    def construit(self):
        res = False
        self.tourConstruction += 1
        if (self.tourConstruction > tourConstructionMax):
            res = True 
        return res

    def placer(self, sprite, scale):
        interface.overviewWidgetGlobal.addItemToScene(sprite, self.position, scale)
        iamap.matrixglobal[self.position[0]][self.position[1]].set_property(self.typeBatiment()) 
    # je ne sais pas si ca marche correctment typeBatiment() 
        
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

    def pleinNourriture(self):
        res = False
        if (self.fillinFood == self.capacityFood):
            res = True
        return res

    def pleinBois(self):
        res = False
        if (self.fillinWood == self.capacityWood):
            res = True
        return res

    def pleinHumain(self):
        res = False
        if (self.fillinHuman == self.capacityHuman):
            res = True
        return res
        
    def videNourriture(self):
        return (self.fillinFood == 0)

    def videBois(self):
        return (self.fillinWood == 0)

    def videHumain(self):
        return (self.fillinHuman == 0)

class Forum(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.capacityFood = 20 #arbitraire
        self.capacityWood = 20 #arbitraire
        self.capacityHuman = 10 #arbitraire
        self.placer("resources/forum.png",0.4)

    def typeBatiment(self):
        return 'forum'


class StockageBois(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.capacityWood = 30 #arbitraire

    def typeBatiment(self):
        return 'stockageBois'

    def estVide(self):
        return self.videBois()

    def estPlein(self):
        return self.pleinBois()

    def toucheFinale(self):
        self.placer("resources/woodStock.jpg", 0.5) #TODO


class Abri(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.capacityHuman = 10 # arbitraire

    def typeBatiment(self):
        return 'abri'

    def estVide(self):
        return self.videHumain()

    def estPlein(self):
        return self.pleinHumain()

    def toucheFinale(self):
        self.placer("resources/abri.jpg", 0.5) #TODO


class BatimentNourriture(Batiment):

    def __init__(self, position):
        Batiment.__init__(self,position)

    def estVide(self):
        return self.videNourriture()

    def estPlein(self):
        return self.pleinNourriture()


class StockageNourriture(BatimentNourriture):

    def __init__(self, position):
        BatimentNourriture.__init__(self, position)
        self.capacityFood = 30 #arbitraire

    def typeBatiment(self):
        return 'stockageNourriture'

    def toucheFinale(self):
        self.placer("resources/foodStock.jpg", 0.5) #TODO
    
class Chaudron(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.capacityFood = 10 # arbitraire
        
    def typeBatiment(self):
        return 'chaudron'

    def toucheFinale(self):
        self.placer("resources/chaudron.jpg", 0.5) #TODO

class Champ(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.capacityFood = 10 # arbitraire
        self.tour = 0
        self.tourMax = 9 # arbitraire

    def typeBatiment(self):
        return 'champ'

    def cultive(self):
        self.tour += 1
        if (self.tour > tourMax):
            self.fillinFood += 1
            self.tour = 0
            
    def recolte(self):
        res = self.fillinFood 
        self.fillinFood = 0
        return res
 
    def toucheFinale(self):
        self.placer("resources/champ.jpg", 0.5) #TODO
