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
    iamap.desMoutonsDePartout()
    iamap.desLoupsDePartout()
    iamap.desHumains()
    iamap.unForum()

    #print(iamap.A_star((75,75),(150,150)))
    # exit quand l'interface s'est coupée (fermeture du programme)
    #sheep=Sheep((175,175))
    #mouton=Sheep((175,175))
    #manager.addEtre(sheep)
    #manager.addEtre(mouton)
    #iamap.matrix[sheep.position[0]][sheep.position[1]].set_have(sheep)
    #iamap.matrix[sheep.position[0]][sheep.position[1]].set_property(sheep.typeAnimal())
    #iamap.matrix[mouton.position[0]][mouton.position[1]].set_have(mouton)
    #iamap.matrix[mouton.position[0]][mouton.position[1]].set_property(mouton.typeAnimal())

    # exit quand l'interface s'est coupée (fermeture du programme)
    sys.exit(inter.getAppHandle().exec_())
    
if __name__ == '__main__':
    main() 
