import random
from etre import *
from lifeExpectancy import *

class Human(Etre):
    """A human is defined by the following characteristics:
    -age
    -life gauge
    -fatigue gauge
    -gender
    -% of chance to kill a wild animal
    -memory"""

    lifeStep = 0.02 # arbitraire a changer (test avec 0.5)
    currentLife = 0
    fogOfWar = 4 # arbitraire

    def __init__(self):
        self.age = 0
        self.lifeGauge = 100 # max=100 arbitraire, a changer si besoin
        self.fatigueGauge = 100 # idem
        self.isMale = random.choice([True, False])
        self.chanceToKill = 0 # nom pas top, init a 0
        self.fogOfWar
        self.memory = [] # structure, a voir

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
        etre.move(movement)

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
    

            

personne = Human()
lE = LifeExpectancy(40,25,6,10)
personne.ages()
personne.dies(lE)
personne.ages()
personne.dies(lE)
personne.ages()
personne.dies(lE)
personne.ages()
personne.dies(lE)
personne.ages()
personne.dies(lE)
personne.ages()
personne.dies(lE)
personne.ages()
personne.dies(lE)
personne.ages()
personne.dies(lE)
personne.ages()
personne.dies(lE)
personne.ages()




