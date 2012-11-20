import random
from etre import *
from lifeExpectancy import *
from iamap import *


class Human(Etre):
    """A human is defined by the following characteristics:
    -age
    -food gauge
    -fatigue gauge
    -gender
    -% of chance to kill a wild animal
    -memory"""

    lifeStep = 0.02 # arbitraire a changer (test avec 0.5)
    currentLife = 0
#    fogOfWar = 4 # arbitraire

    def __init__(self, position):
        self.position=position     
        self.age = 0
        self.foodGauge = 100 # max=100 arbitraire, a changer si besoin
        self.fatigueGauge = 100 # idem
        self.chanceToKill = 0 # nom pas top, init a 0
#        self.fogOfWar
        self.memory = [] # structure, a voir
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

    # ressource = baies, tree, sheep, wolf 
    def rechercheDeRessource(self, ressource):
        matrix = iamap.matrixglobal
        i = self.position[0]
        j = self.position[1]

        for k in range(0,40): #arbitraire
            for x in range(i-distance,i+distance):
                for y in range(j-distance,j+distance):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        if(matrix[x][y].has_property(ressource)):
                            return (x,y)
        return(-1,-1)
    
    # terrain = land, beach, mountain, water, salwater
    def rechercheDeTerrain(self, terrain):
        matrix = iamap.matrixglobal
        i = self.position[0]
        j = self.position[1]

        for k in range(0,40): #arbitraire
            for x in range(i-distance,i+distance):
                for y in range(j-distance,j+distance):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        if(matrix[x][y].cell_type == terrain):
                            return (x,y)
        return(-1,-1)
        
    
    def run(self):
        print("random explo")
        self.randomExplo()
            


