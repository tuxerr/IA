#!/usr/bin/python
# -*- coding: utf-8 -*-

# fichier définissant l'interface générale
import sys
from interface import *
from configuration import *
from iamap import *
from etre import *
from human import *
from Gaia import *
from manager import *

def main():
    #dictionnaire contenant les informations de configuration de la simulation
    conf = conf_defaults()

    iamap = IAMap(300,300)
    iamap.generate_map(conf)

    manager = Manager()

    #handle gérant l'interface qt de la simulation
    inter = Interface(conf,iamap,manager)

    (cost,chemin)=iamap.A_start([75,75], [76,76])
    print(chemin)
    print(cost)
    
    waterCarrier = Human((120,120))
    manager.addEtre(waterCarrier)
#    iamap.desMoutonsDePartout()

    sheep=Sheep((100,100))
    manager.addEtre(sheep)
#    sheep.start()
    mouton=Sheep((150,150))
    manager.addEtre(mouton)
#    mouton.start()

    # exit quand l'interface s'est coupée (fermeture du programme)
    sys.exit(inter.getAppHandle().exec_())
    
    
if __name__ == '__main__':
    main() 
