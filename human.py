import random
from etre import *
from lifeExpectancy import *
from iamap import *

class Human(Etre):
    """Un humain est defini par :
    - position
    - age
    - jauge de nourriture
    - jauge de fatigue
    - genre
    - % de chance de tuer un animal sauvage lors d'un combat
    - memoire forme (ressource, x, y)
    la ressource pouvant etre "batFood", "batWood", "forum", "abri" 
    """

    lifeStep = 0.02 # arbitraire a changer (test avec 0.5)
    currentLife = 0

    def __init__(self, position):
        self.position = position     
        self.age = 0
        self.foodGauge = 100 # max=100 arbitraire, a changer si besoin
        self.fatigueGauge = 100 # idem
        self.chanceToKill = 0 # nom pas top, init a 0
        self.role = "enfant"
        self.memory = [] # (ressource,x,y)
        self.isIn = False
        super().__init__("resources/worker_water.jpg",position)

    def ages(self):
        Human.currentLife += Human.lifeStep
        if Human.currentLife == 1:
            self.age +=1
            Human.currentLife = 0

    def dies(self, lifeE):
        d100 = random.randint(1, 100)
        if d100 < lifeE.currentMortality(self.age):
            return(True)
        else:
            return(False)

    def move(self,movement):
        super().move(movement)

    def randomExplo(self):
        d8 = random.randrange(1,8)
        if d8 == 1:
            self.move((0,1))
        elif d8 == 2:
            self.move((1,1))
        elif d8 == 3:
            self.move((1,0))
        elif d8 == 4:
            self.move((1,-1))
        elif d8 == 5:
            self.move((0,-1))
        elif d8 == 6:
            self.move((-1,-1))
        elif d8 == 7:
            self.move((-1,0))
        else:
            self.move((-1,1))

    # ressource = baies, tree, batiment (immobile)
    def rechercheRessource(self, ressource):
        matrix = iamap.matrixglobal
        i = self.position[0]
        j = self.position[1]
        for k in range(0,40): #arbitraire
            for x in range(i-k,i+k):
                for y in range(j-k,j+k):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        if(matrix[x][y].has_property(ressource)):
                            return (x,y)
        return(-1,-1)

    # ressource mouvante = mouton, loup
    def rechercheRessourceMouvante(self, typeAnimal):
        matrix = iamap.matrixglobal
        i = self.position[0]
        j = self.position[1]
        target = 0
        distance = 0
        distanceMax = 40 #arbitraire
        isSearching = True 
        while(isSearching&(distance<distanceMax)):
            for x in range(i-distance,i+distance):
                for y in range(j-distance,j+distance):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        if(matrix[x][y].has_property(typeAnimal)):
                            target =  matrix[x][y].getAnimal(typeAnimal)
                            isSearching = False
            distance=distance+1
        return target

    
    # terrain = land, beach, mountain, water, salwater (immobile)
    def rechercheTerrain(self, terrain):
        matrix = iamap.matrixglobal
        i = self.position[0]
        j = self.position[1]
        for k in range(0,40): #arbitraire
            for x in range(i-k,i+k):
                for y in range(j-k,j+k):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        if(matrix[x][y].cell_type == terrain):
                            return (x,y)
        return(-1,-1)

    def isCorrespond(self, human):
        return((human.isFecond())&(self.gender!=human.gender)&(human.age >15))

    # plus specifique que ressource specifiquement pour humain
    def rechercheConjoint(self):
        matrix = iamap.matrixglobal
        i = self.position[0]
        j = self.position[1]
        target = 0
        distance = 0
        distanceMax = 40 #arbitraire
        isSearching = True 
        while(isSearching&(distance<distanceMax)):
            for x in range(i-distance,i+distance):
                for y in range(j-distance,j+distance):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        if(matrix[x][y].has_property("human")):
                            for human in matrix[x][y].getHuman():
                                if(self.isCorrespond(human)):
                                    target = human
                                    isSearching = False
            distance=distance+1
        return target

    def cheminCible(self, target):
        matrix = iamap.matrixglobal
        (cout, chemin) = iamap.iamapglobal.A_star(self.position, target)
        return chemin

    def cheminCibleCout(self, target):
        return iamap.iamapglobal.A_star(self.position, target)

    def cheminCibleMouvante(self, target):
        matrix = iamap.matrixglobal
        (cout, chemin) = iamap.iamapglobal.A_star(self.position, target.position)
        return chemin

    """trouver le batiment le plus proche contenant/pouvant contenir
    la type de "ressources" suivant (food, wood, human)"""
    def memoireBat(self, contentType):
        for (typeMem, x, y) in self.memory:
            matrix = iamap.matrixglobal
            distMin = float("inf")
            if (contentType == "food"):
                if (typeMem=="batFood" or typeMem=="forum"):
                    (cout, chemin) = self.cheminCibleCout((x,y))
                    if (cost < distMin):
                        distMin = cost
                        cheminMin = chemin
            elif (contentType == "wood"):
                if (typeMem=="batWood" or typeMem=="forum"):
                    (cout, chemin) = self.cheminCibleCout((x,y))
            elif (contentType == "human"):
                if (typeMem=="forum" or typeMem=="abri"):
                    (cout, chemin) = self.cheminCibleCout((x,y))
            if (cout < distMin):
                distMin = cout
                cheminMin = chemin
        if (distMin == float("inf")): 
            res = [(-1,-1)]
        else:
            res = cheminMin
        return res
          
    def run(self):
        role = self.role
        if role == "enfant":
            self.runEnfant()
        elif role == "chef":
            self.runChef()
        elif role == "cultivateur":
            self.runCultivateur()
        elif role == "eleveur":
            self.runEleveur()
        elif role == "chasseurLoup":
            self.runChasseurLoup()
        elif role == "chasseurMouton":
            self.runChasseurMouton()
        elif role == "cueilleur":
            self.runCueilleur()
        elif role == "bucheron":
            self.runBucheron()
        elif role == "porteurEau":
            self.runPorteurEau()
        elif role == "constructeur":
            self.runConstructeur()
        else:
            self.runCuisinier()

    """ cuisinier (en plus de surveiller ses jauges) :
    - va chercher au stockage le plus proche dans sa mémoire
    - vide ou pas de stockage en mémoire -> recherche nouveau
    - prendre nourriture (indiff)
    - retourner au centre ville (ou case adjacente ?)
    - cuisiner pendant n tours
    - distribuer
    - cest vide ? on recommence (ou partiellement vide ?)""" 

    def runCuisinier(self):        
        self.runSurvie()
        chemin = self.memoireBat("food")
        if (chemin == [(-1,-1)]): #fail pas d'endroit a food en memoire

