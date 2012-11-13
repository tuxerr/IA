#!/usr/bin/python
# -*- coding: utf-8 -*-

# fichier définissant l'interface générale
import sys
from interface import *
from configuration import *
from iamap import *
from etre import *
from Gaia import *
def main():
    #dictionnaire contenant les informations de configuration de la simulation
    conf = conf_defaults()

    iamap = IAMap(300,300)
    iamap.generate_map(conf)

    #handle gérant l'interface qt de la simulation
    inter = Interface(conf,iamap)

    (cost,chemin)=iamap.A_start([75,75], [76,76])
    print(chemin)
    print(cost)
    
    waterCarrier = Etre("resources/worker_water.jpg",(0,0))
    iamap.desMoutonsDePartout()
    # exit quand l'interface s'est coupée (fermeture du programme)
    Sheep([50,50])
    sheep=Sheep((50,50))
    sheep.start()
    Sheep((75,75))
    mouton=Sheep((75,75))
    mouton.start()
    sys.exit(inter.getAppHandle().exec_())
    
    
if __name__ == '__main__':
    main() 
