#!/usr/bin/python
# -*- coding: utf-8 -*-

# fichier définissant l'interface générale
import sys
from interface import *
from configuration import *
from iamap import *
from etre import *
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

    
    waterCarrier = Etre("resources/worker_water.jpg",(300-1,300-1))
    iamap.desMoutonsDePartout()
    #print(iamap.A_star((75,75),(150,150)))
    # exit quand l'interface s'est coupée (fermeture du programme)
    #Sheep([175,175])
    #sheep=Sheep((175,175))
    #sheep.start()
    #Sheep((90,90))
    #mouton=Sheep((90,90))
    #mouton.start()


    # exit quand l'interface s'est coupée (fermeture du programme)
    sys.exit(inter.getAppHandle().exec_())
    
if __name__ == '__main__':
    main() 
