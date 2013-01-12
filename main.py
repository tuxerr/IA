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
    gaia = Nature()
    inter = Interface(conf,iamap,manager)
    manager.addEtre(gaia)
    iamap.desMoutonsDePartout()
    iamap.desLoupsDePartout()
    iamap.unForum()

    # exit quand l'interface s'est coupée (fermeture du programme)
    sys.exit(inter.getAppHandle().exec_())
    
if __name__ == '__main__':
    main() 
