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
        self.jaugeNourriture = 100 # max=100 arbitraire
        self.fatigueGauge = 100 # idem
        self.chanceToKill = 0 # nom pas top, init a 0
        self.role = 'enfant'
        self.memory = [] # (ressource,x,y) infini for now
        self.isIn = False
        super().__init__("resources/worker_water.jpg",position)

    def vieilli(self):
        Human.currentLife += Human.lifeStep
        if Human.currentLife == 1:
            self.age +=1
            Human.currentLife = 0

    def mortNaturelle(self, lifeE):
        d100 = random.randint(1, 100)
        if d100 < lifeE.currentMortality(self.age):
            res = True
        else:
            res = False
        return res
        
    def mortDeFaim(self):
        return (self.jaugeNourriture <= 0)

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
#
# TODO ajouter les element dans la memoire
#

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
                        if(matrix[x][y].has_property('human')):
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
    def memoireBatiment(self, contentType):
        for (typeMem, x, y) in self.memory:
            matrix = iamap.matrixglobal
            distMin = float("inf")
            if (contentType == 'food'):
                if (typeMem == 'stockageNourriture' or typeMem == 'forum'):
                    (cout, chemin) = self.cheminCibleCout((x,y))
                    if (cost < distMin):
                        distMin = cost
                        cheminMin = chemin
            elif (contentType == 'wood'):
                if (typeMem == 'stockageBois' or typeMem == 'forum'):
                    (cout, chemin) = self.cheminCibleCout((x,y))
            elif (contentType == 'human'):
                if (typeMem == 'forum' or typeMem == 'abri'):
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
        self.runSurvie()
        role = self.role
        if role == 'enfant':
            self.runEnfant()
        elif role == 'chef':
            self.runChef()
        elif role == 'cultivateur':
            self.runCultivateur()
        elif role == 'eleveur':
            self.runEleveur()
        elif role == 'chasseurLoup':
            self.runChasseurLoup()
        elif role == 'chasseurMouton':
            self.runChasseurMouton()
        elif role == 'cueilleur':
            self.runCueilleur()
        elif role == 'bucheron':
            self.runBucheron()
        elif role == 'porteurEau':
            self.runPorteurEau()
        elif role == 'constructeur':
            self.runConstructeur()
        else:
            self.runCuisinier()
        self.vieilli()
        self.jaugeNourriture = self.jaugeNourriture - 1
        if (self.mortNaturelle() or self.mortDeFaim()):
            self.mort()
            print("human dead")

    """ cuisinier (en plus de surveiller ses jauges)
    la premiere fois : 
    - le chef indique l'emplacement d'un chaudron sans cuisinier
    - target pour le cuisinier chaudron
    description lineaire :
    - va chercher au stockage le plus proche dans sa mémoire
    - vide ou pas de stockage en mémoire -> recherche nouveau
    - prendre nourriture (indiff)
    - retourner au centre ville (ou case adjacente ?)
    - cuisiner pendant n tours
    - distribuer
    - cest vide ? on recommence
    description a chaque etape :
    - soit il sait ou aller
    -- chercher bouffe
    -- aller voir le chef (forum, pour savoir ou chercher bouffe)
    -- retourner au forum pour cuisiner avec la bouffe
    - soit il sert a manger/cuisine
    -- donc reste sur place
    -- verifie qu'il reste de la nourriture dans le chaudron
    """ 

#TODO memoireCuisine
#TODO improve memoire batiment (a voir en fonction de memoire cuisine)

    def runCuisinier(self):
        matrix = iamap.matrixglobal
        x = self.position[0]
        y = self.position[1]
        # si on se trouve sur le forum on partage la mémoire du chef
        # le partage de la mémoire est instantannee et relatif au role
        if matrix[x][y].has_property('forum'):
            monChef = matrix[x][y].getHumanByRole('chef')
            self.memoireCuisine(monChef)
        if (hasTarget): # sait ou aller, qu'il doit se reposer
            if (self.position == self.target.position):
#TODO avancer                
        else: # cuisine-sert/verifie (obligatoirement a son chaudron)
            monChaudron = matrix[x][y].getBatiment('chaudron')
            if (monChaudron.fillinFood == 0):
                chemin = self.memoireBatiment('food') 
                # au moins un res le forum
                # donc a une target pour le tour prochain
        
