#!/usr/bin/python
# -*- coding: utf-8 -*-

# fichier définissant l'interface générale
import sys
from interface import *
        
def main():
    inter = Interface()

    # exit quand l'interface s'est coupée (fermeture du programme)
    sys.exit(inter.getAppHandle().exec_())

if __name__ == '__main__':
    main() 
