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

    lifeStep = 0.5 # arbitraire a changer (test avec 0.5)
    currentLife = 0

    def __init__(self):
        self.age = 0
        self.lifeGauge = 100 # max=100 arbitraire, a changer si besoin
        self.fatigueGauge = 100 # idem
        self.isMale = random.choice([True, False])
        self.chanceToKill = 0 # nom pas top
        self.memory = [] # strucure, a voir

    def ages(self):
        Human.currentLife += Human.lifeStep
        if Human.currentLife == 1:
            self.age +=1
            Human.currentLife = 0

    def dies(self, lifeE):
        d100 = random.randrange(0, 100)
        if d100 < lifeE.currentMortality(self.age):
            return(True)
        else:
            return(False)

            

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




