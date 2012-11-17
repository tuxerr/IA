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
    
    def __init__(self,position):
        #self.position=position     
        self.gender=random.choice(['femelle','male'])
        self.jaugeNourriture=200
        self.vitesse=42
        self.etat='vivant'
        super().__init__("resources/Sheep.png",position)
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
        typeAnimal="animaux"#self.typeAnimal()
        isConjoint=True
        distance=0
        i=self.position[0]
        j=self.position[1]
        pointInteressant=[]
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
                        
                
        
#soit il se nourrit, soit il se deplace

class Sheep(Animal,threading.Thread) :
    
    def __init__(self,position):
        Animal.__init__(self,position)
        threading.Thread.__init__(self)
        self.feeding=50
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
            
    def enfanter(self,sheep):
        if sheep.typeAnimal()=='Sheep':
            if ((self.gender=='femelle') & (sheep.gender=='male')):
                if(self.position==sheep.position):
                    if ((self.isFecond()) & (sheep.isFecond())):
                        print("encoure")
                        self.jaugeNourriture=self.jaugeNourriture-200
                        sheep.jaugeNourriture=sheep.jaugeNourriture-200
                        newSheep=Sheep((self.position[0],self.position[1]))
                        #newSheep=Sheep((200,200))
                        iamap.matrixglobal[newSheep.position[0]][newSheep.position[1]].set_have(newSheep)
                        iamap.matrixglobal[newSheep.position[0]][newSheep.position[1]].set_property("animaux")
                        manager.managerGlobal.addEtre(newSheep)
                        print("un bebe est né")
                    else:
                        print("non fecond",self.jaugeNourriture,sheep.jaugeNourriture)
                else:
                    print("probleme de position")    
            else:
                print("probleme de genre")
        else:
            print("on a pas deux moutons")
                    
    def nourrir(self):
        self.jaugeNourriture=self.jaugeNourriture+self.feeding
        
    def choix(self):
        rand=random.randint(1,100)
        if (rand>((500-self.jaugeNourriture)/5))|(len(iamap.iamapglobal.matrix[self.position[0]][self.position[1]].have)>1):
            rand1=random.choice([-1,0,1])
            rand2=random.choice([-1,0,1])
            move=self.move((rand1,rand2))
            while move==0|(rand1==0 & rand2==0):
                move=self.move((random.choice(-1,0,1),random.choice(-1,0,1)))
        else:           
            self.nourrir()
            
    def run(self):
        
        if self.target== 0:
            if self.jaugeNourriture<300:
                self.choix()
            else:
                self.target=self.rechercheDeConjoint()
        else:
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
        self.jaugeNourriture=self.jaugeNourriture-1
        if self.jaugeNourriture<=0:
            print("sheep dead")
                    
#Le loup se nourri d'homme et de sheep
class Wolf(Animal):
    #http://dehais.perso.enseeiht.fr/tsi-ogl
    def __init__(self,position):
        super().__init__(position)
        #A voir avec les humains
        self.force=random.choice([1,2,3])
        self.distanceDeRecherche=10
    def typeAnimal(self):
        return 'Wolf'
    
    def chercheNourriture(self):
        matrix=iamap.matrixglobal
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
            

