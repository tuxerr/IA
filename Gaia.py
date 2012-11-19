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
import time
import iamap
from iamap import *
import manager
from manager import *

class Animal(Etre):
    
    def __init__(self,sprite,scale,position):
        #self.position=position     
        self.gender=random.choice(['femelle','male'])
        self.jaugeNourriture=200
        self.vitesse=42
        self.etat='vivant'
        super().__init__(sprite,scale,position)
        self.target=0
        self.chemin=[]
        
    def isCorrespond(self,animal):
        return((animal.isFecond())&(self.isFecond())&(self.gender!=animal.gender))
    
    #a redéfinir pour les animaux en cage
    def isFecond(self):
        return((self.etat=='vivant')&(self.jaugeNourriture>=300))

    #getAnimal et isAnimal à implementer pour les celulles
    #getAnimal doit revoyer une liste
    def rechercheDeConjoint(self):
        matrix=iamap.matrixglobal
        typeAnimal=self.typeAnimal()
        isConjoint=True
        distance=0
        i=self.position[0]
        j=self.position[1]
        target=0
        distanceMax=40
        while(isConjoint&(distance<distanceMax)):
            for x in range(i-distance,i+distance):
                for y in range(j-distance,j+distance):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        if(matrix[x][y].has_property(typeAnimal)):
                            for animal in matrix[x][y].getAnimal(typeAnimal):
                                if(self.isCorrespond(animal)):
                                    target=animal
                                    isConjoint=False
            distance=distance+1
        return target

    def cheminConjoint(self,target):
        (cost,chemin)=iamap.iamapglobal.A_star(self.position,target.position)
        return (cost,chemin)
    
    def rejoindreConjoint(self,target):
        matrix=iamap.matrixglobal
        (cost,chemin)=self.cheminConjoint(target)
        finChemin=[]
        if cost>=2:
            currentCost=0
            i=0;
            while((currentCost<(cost/2))&(i<len(chemin))):
                if(abs(chemin[i][0]-self.position[0])+abs(chemin[i][1]-self.position[1]))==2:
                    currentCost=currentCost+1.4
                else:
                    currentCost=currentCost+1
                finChemin.append(chemin[i])
                i=i+1
        else:
            finChemin=chemin
        return finChemin
                        
    def enfanter(self,animal):
        if animal.typeAnimal()==self.typeAnimal():
            if ((self.gender=='femelle') & (animal.gender=='male')):
                if(self.position==animal.position):
                    if ((self.isFecond()) & (animal.isFecond())):
                        self.jaugeNourriture=self.jaugeNourriture-200
                        animal.jaugeNourriture=animal.jaugeNourriture-200
                        if self.typeAnimal()=='sheep':
                            animalNew=Sheep((self.position[0],self.position[1]))
                        else:
                            animalNew=Wolf((self.position[0],self.position[1]))
                        #newSheep=Sheep((200,200))
                        iamap.matrixglobal[animalNew.position[0]][animalNew.position[1]].set_have(animalNew)
                        iamap.matrixglobal[animalNew.position[0]][animalNew.position[1]].set_property(animalNew.typeAnimal())
                        manager.managerGlobal.addEtre(animalNew)
                        print("un bebe est né",self.typeAnimal())
                    else:
                        print("non fecond",self.jaugeNourriture,animal.jaugeNourriture)
                else:
                    print("probleme de position")    
            else:
                print("probleme de genre")
        else:
            print("on a pas deux moutons")

        
#soit il se nourrit, soit il se deplace

class Sheep(Animal) :
    
    def __init__(self,position):
        Animal.__init__(self,"resources/Sheep.png",0.4,position)
        self.feeding=100
        #A voir avec les humains
        self.escape=random.choice(range(25,75)) 
        
    def printCoord(self):
        print(self.position)
    
    def typeAnimal(self):
        return 'sheep'
#un hunter peut être soit un loup qui a loupé son coup soit un humain
    def fuir(self,hunter): 
        fromHunter=[self.position[0]-hunter.position[0],self.position[1]-hunter.position[1]]
        directionDeFuite=[-fromHunter[0],-fromHunter[1]]
            
                    
    def nourrir(self):
        self.jaugeNourriture=self.jaugeNourriture+self.feeding
        
    def choix(self):
        rand=random.randint(1,100)
        if (rand>((500-self.jaugeNourriture)/5)):
            #|(len(iamap.iamapglobal.matrix[self.position[0]][self.position[1]].have)>1):
            rand1=random.choice([-1,0,1])
            rand2=random.choice([-1,0,1])
            move=self.move((rand1,rand2))
            while (move==0)&(rand1==0 & rand2==0):
                rand1=random.choice([-1,0,1])
                rand2=random.choice([-1,0,1])
                move=self.move((rand1,rand2))
        else:           
            self.nourrir()
            
    def run(self):
        if self.target== 0:
            if self.jaugeNourriture<300:
                self.choix()
            else:
                self.target=self.rechercheDeConjoint()
        else:
            if (self.isFecond())&(self.target.isFecond()):
                if self.position==self.target.position:
                    if self.gender=="femelle":
                        self.enfanter(self.target)
                    else:
                        self.nourrir()
                    self.target=0
                    self.chemin=[]
                else:
                    if self.chemin==[]:
                        self.chemin=self.rejoindreConjoint(self.target)
                    if self.chemin != []:
                        self.setPos(self.chemin[0])
                        self.chemin.remove(self.chemin[0])
            else:
                self.target=0
                self.chemin=[]
        self.jaugeNourriture=self.jaugeNourriture-1
        if self.jaugeNourriture<=0:
            self.mort()
            print("sheep dead")
                    
#Le loup se nourri d'homme et de sheep
class Wolf(Animal):
    #http://dehais.perso.enseeiht.fr/tsi-ogl
    def __init__(self,position):
        Animal.__init__(self,"resources/Wolf.png",0.4,position)
        #A voir avec les humains
        self.force=random.choice([1,2,3])
        self.distanceDeRecherche=10
        self.nourriture=0
        self.cheminNourriture=[]
        
    def typeAnimal(self):
        return 'wolf'
    
    def chercheNourriture(self):
        matrix=iamap.matrixglobal
        typeAnimal='sheep'
        isConjoint=True
        distance=0
        i=self.position[0]
        j=self.position[1]
        target=0
        distanceMax=self.distanceDeRecherche
        while(isConjoint&(distance<distanceMax)):
            for x in range(i-distance,i+distance):
                for y in range(j-distance,j+distance):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        if(matrix[x][y].has_property(typeAnimal)):
                            jaugeMax=0
                            for animal in matrix[x][y].getAnimal(typeAnimal):
                                if(animal.jaugeNourriture>jaugeMax):
                                    target=animal
                                    jaugeMax=target.jaugeNourriture
                                    isConjoint=False
            distance=distance+1
        return target        
    def rode(self):
        #if (len(iamap.iamapglobal.matrix[self.position[0]][self.position[1]].have)>1):
        rand1=random.choice([-1,0,1])
        rand2=random.choice([-1,0,1])
        move=self.move((rand1,rand2))
        while move==0&(rand1==0 & rand2==0):
            move=self.move((random.choice(-1,0,1),random.choice(-1,0,1)))
            
    def nourrir(self,nourriture):
        if (nourriture.etat=='vivant')&(self.position==nourriture.position):
            nourriture.mort()
            self.jaugeNourriture=self.jaugeNourriture+nourriture.jaugeNourriture
            print("un sheep est mort")
    def run(self):
        if self.target==0:
            if self.nourriture==0:
                rand=random.randint(1,100)
                if rand>42:
                    self.nourriture=self.chercheNourriture()
                else:
                    if self.jaugeNourriture<300:
                        self.rode()
                    else:
                        self.target=self.rechercheDeConjoint()
            else:
                if self.position==self.nourriture.position:
                    self.nourrir(self.nourriture)
                    self.cheminNourriture=[]
                    self.nourriture=0
                else:
                    if self.cheminNourriture==[]:
                        self.cheminNourriture=self.rejoindreConjoint(self.nourriture)
                    if self.cheminNourriture != []:
                        self.setPos(self.cheminNourriture[0])
                        self.cheminNourriture.remove(self.cheminNourriture[0])
        else:
            if (self.isFecond())&(self.target.isFecond()):
                if self.position==self.target.position:
                    if self.gender=="femelle":
                        self.enfanter(self.target)
                    self.target=0
                    self.chemin=[]
                else:
                    if self.chemin==[]:
                        self.chemin=self.rejoindreConjoint(self.target)
                    if self.chemin != []:
                        self.setPos(self.chemin[0])
                        self.chemin.remove(self.chemin[0])
            else:
                self.target=0
                self.chemin=[]
        self.jaugeNourriture=self.jaugeNourriture-1
        if self.jaugeNourriture<=0:
            self.mort()
            print("wolf dead")
