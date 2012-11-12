

class LifeExpectancy:
    """modelisation de la duree de vie basee sur Weibull (la baignoire)
    http://fr.wikipedia.org/wiki/Loi_de_Weibull#Application_particuli.C3.A8re
    pour l'instant simplification par une courbe affine par morceaux :
    - mortalite infantile (decroissante)
    - constant pendant la vie "adulte"
    - mort de vieillesse (croissante)
    La courbe donne le %age de chance de mourir de mort naturelle
    Definie par les valeurs suivantes :
    - mortalite a la naissance (0-100)
    - mortalite "adulte" (0-100 et <mortalite a la naissance)
    - age de debut de "degenerescence"
    - pente de "degenerescence" 
    TODO definir des quadruplets "valables" pour faire des tests"""

    def __init__(self, infantMortality, adultMortality, adultStop, mortality):
        self.infantMortality = infantMortality
        self.adultMortality = adultMortality
        self.adultStop = adultStop
        self.mortality = mortality


    def currentMortality(self, age):
        if age < 3: # age arbitraire de fin de mortalite infantile
            return (self.infantMortality+((self.adultMortality-self.infantMortality)/3)*age)
        elif age <= self.adultStop:
            return self.adultStop
        else:
            return (self.adultMortality+(self.mortality/(age-self.adultStop))*age)
        

