'''
Created on Nov 8, 2012

@author: jason
'''
#les animaux peuvent se reproduire et doivent se nourrir
#atributs des animaux:
#leur position sur la carte.
#leur sexe
#une jauge de nourriture
#pas d'eau, sinon ils vont t'endre a être tous au niveau de l'eau ..à voir
#je dirais une base de nourriture sur /500, commence avec 200, peut se reproduire à partire de 400 et repasse a 200
import random
import math
from etre import *
import threading

class Animal(Etre):
    
    def __init__(self,position):
        self.position=position     
        self.jaugeNourriture=200
        self.vitesse=42
        self.etat='vivant'
        super().__init__("resources/Sheep.png",position)
            
    def isCorrespond(self,animal):
        return(animal.isFecond()&self.isFecond()(self.gender!=animal.gender))
    
    #a redéfinir pour les animaux en cage
    def isFecond(self):
        return((self.etat=='vivant')&(self.jaugeNourriture>=400))

    #getAnimal et isAnimal à implementer pour les celulles
    #getAnimal doit revoyer une liste
    def rechercheDeConjoint(self,matrix):
        typeAnimal=self.typeAnimal()
        isConjoint=False
        distance=0
        i=self.position[0]
        j=self.position[1]
        pointInteressant=[]
        target=0
        while(isConjoint&(distance<matrix.width)):
            for x in range(0,distance):
                for y in range(0,distance):
                    if(math.floor(math.sqrt(math.pow(x-i,2)+math.pow(y-j,2)))<distance):
                        pointInteressant.append([x,y])
            for potentialAnimal in pointInteressant:
                x=potentialAnimal[0]
                y=potentialAnimal[1]
                if((0<x)&(x<matrix.width)&(0<y)&(y<matrix.height)):
                    if(matrix[x][y].isAnimal(typeAnimal)):
                        for animal in matrix[x][y].getAnimal(typeAnimal):
                            if(self.isCorrespond(animal)):
                                target=animal
                                isConjoint=True
            distance=distance+1
        return target

        
#soit il se nourrit, soit il se deplace

class Sheep(Animal,threading.Thread) :
    
    def __init__(self,position):
        Animal.__init__(self,position)
        threading.Thread.__init__(self)
        self.feeding=3
        #A voir avec les humains
        self.escape=random.choice(range(25,75)) 
        
    def printCoord(self):
        print(self.position)
    
    def typeAnimal(self):
        return 'Sheep'
#un hunter peut être soit un loup qui a loupé son coup soit un humain
    def fuir(self,hunter): #JASON ON DIT FUIR PAS FUIRE, DYSLEXIQUE DE MERDE <3
        fromHunter=[self.position[0]-hunter.position[0],self.position[1]-hunter.position[1]]
        directionDeFuite=[-fromHunter[0],-fromHunter[1]]
               
    def run(self):
        print("running sheep")
        i=0
        while(i<10):
            self.move((1,1))
            i=i+1
            print(self.position)
        
#Le loup se nourri d'homme et de sheep
class Wolf(Animal):
    
    def __init__(self,position):
        super().__init__(position)
        #A voir avec les humains
        self.force=random.choice([1,2,3])
        self.distanceDeRecherche=10
    def typeAnimal(self):
        return 'Wolf'
    
    def chercheNourriture(self,matrix):
        isNourriture=False
        distance=0
        i=self.position[0]
        j=self.position[1]
        pointInteressant=[]
        target=0
        while(isNourriture&(distance<self.distanceDeRecherche)):
            for x in range(0,distance):
                for y in range(0,distance):
                    if(math.floor(math.sqrt(math.pow(x-i,2)+math.pow(y-j,2)))<distance):
                        pointInteressant.append([x,y])
            for potentialNourriture in pointInteressant:
                x=potentialNourriture[0]
                y=potentialNourriture[1]
                if((0<x)&(x<matrix.width)&(0<y)&(y<matrix.height)):
                    if(matrix[x][y].isAnimal('Sheep'|'Humain')):
                        for nourriture in matrix[x][y].getAnimal('Sheep'|'Humain'):
                            if(nourriture.typeAnimal()=='Sheep'):#a revoir
                                target=nourriture
                                isNourriture=True
            distance=distance+1
        return target
            
