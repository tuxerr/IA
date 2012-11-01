#!/usr/bin/python
# -*- coding: utf-8 -*-

# fichier définissant l'interface générale
import sys
from interface import *
from configuration import *
        
def main():
    #dictionnaire contenant les informations de configuration de la simulation
    conf = conf_defaults()

    #handle gérant l'interface qt de la simulation
    inter = Interface(conf)

    # exit quand l'interface s'est coupée (fermeture du programme)
    sys.exit(inter.getAppHandle().exec_())

if __name__ == '__main__':
    main() 
