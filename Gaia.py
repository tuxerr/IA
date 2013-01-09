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
import interface
from interface import *
global gaia

class Nature():
    def __init__(self):
        global gaia
        self.herbes=[]
        self.arbres=[]
        self.baies=[]
        self.herbesTime=100
        self.arbresTime=500
        self.baiesTime=350
        gaia=self
        
    def addHerbes(self,h):
        item = interface.owGlobal.itemmatrix[h[0]][h[1]]
        self.herbes.append([h,0])
        iamap.matrixglobal[h[0]][h[1]].set_property("noHerbes")
        item.setPen(QtGui.QColor(0,0,0))
        item.setBrush(QtGui.QColor(0,0,0))


    def addArbres(self,a):
        self.arbres.append([a,0])
        iamap.matrixglobal[a[0]][a[1]].set_property("noArbres")
        iamap.matrixglobal[a[0]][a[1]].remove_property("tree")
        item = interface.owGlobal.itemmatrix[a[0]][a[1]]
        item.setPen(QtGui.QColor(0,255,0))
        item.setBrush(QtGui.QColor(0,255,0))
        

    def addBaies(self,b):
        self.baies.append([b,0])
        iamap.matrixglobal[b[0]][b[1]].set_property("noBaies")
        iamap.matrixglobal[b[0]][b[1]].remove_property("baies")
        item = interface.owGlobal.itemmatrix[b[0]][b[1]]
        item.setPen(QtGui.QColor(0,255,0))
        item.setBrush(QtGui.QColor(0,255,0))
        
    def incHerbes(self):
        for h in self.herbes:
            h[1]=h[1]+1

    def incArbres(self):
        for a in self.arbres:
            a[1]=a[1]+1

    def incBaies(self):
        for b in self.baies:
            b[1]=b[1]+1

    def removeHerbes(self):
        for h in self.herbes:
            if (h[1]>=self.herbesTime):
                self.herbes.remove(h)    
                iamap.matrixglobal[h[0][0]][h[0][1]].remove_property("noHerbes")
                item = interface.owGlobal.itemmatrix[h[0][0]][h[0][1]]
                item.setPen(QtGui.QColor(0,255,0))
                item.setBrush(QtGui.QColor(0,255,0))

    def removeArbres(self):
        for a in self.arbres:
            if (a[1]>=self.arbresTime):
                self.arbres.remove(a)
                iamap.matrixglobal[a[0][0]][a[0][1]].remove_property("noArbres")
                iamap.matrixglobal[a[0][0]][a[0][1]].set_property("tree")
                item = interface.owGlobal.itemmatrix[a[0][0]][a[0][1]]
                item.setPen(QtGui.QColor(117,154,16))
                item.setBrush(QtGui.QColor(117,154,16))

    def removeBaies(self):
        for b in self.baies:
            if (b[1]>=self.baiesTime):
                self.baies.remove(b)
                iamap.matrixglobal[b[0][0]][b[0][1]].remove_property("noBaies")
                iamap.matrixglobal[b[0][0]][b[0][1]].set_property("baies")
                item = interface.owGlobal.itemmatrix[b[0][0]][b[0][1]]
                item.setPen(QtGui.QColor(255,0,0))
                item.setBrush(QtGui.QColor(255,0,0))

    def run(self):
        self.incHerbes()
        self.incArbres()
        self.incBaies()
        self.removeHerbes()
        self.removeArbres()
        self.removeBaies()

class Animal(Etre):
    
    def __init__(self,sprite,scale,position):
        #self.position=position     
        self.jaugeNourriture=200
        self.vitesse=42
        super().__init__(sprite,scale,position)
        self.target=0
        
    def isCorrespond(self,animal):
        return((animal.isFecond())&(self.isFecond())&(self.gender!=animal.gender))
    
    #a redéfinir pour les animaux en cage
    def isFecond(self):
        return((self.etat=='vivant')&(self.jaugeNourriture>=300))

    #getAnimal et isAnimal à implementer pour les celulles
    #getAnimal doit revoyer une liste
    def rechercheDeConjoint(self):
        matrix=iamap.matrixglobal
        typeObjet=self.typeObjet()
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
                        if(matrix[x][y].has_property(typeObjet)):
                            for animal in matrix[x][y].getAnimal(typeObjet):
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
        if animal.typeObjet()==self.typeObjet():
            if ((self.gender=='F') & (animal.gender=='M')):
                if(self.position==animal.position):
                    if ((self.isFecond()) & (animal.isFecond())):
                        self.jaugeNourriture=self.jaugeNourriture-200
                        animal.jaugeNourriture=animal.jaugeNourriture-200
                        if self.typeObjet()=='sheep':
                            animalNew=Sheep((self.position[0],self.position[1]))
                        else:
                            animalNew=Wolf((self.position[0],self.position[1]))
                        #newSheep=Sheep((200,200))
                        iamap.matrixglobal[animalNew.position[0]][animalNew.position[1]].set_have(animalNew)
                        iamap.matrixglobal[animalNew.position[0]][animalNew.position[1]].set_property(animalNew.typeObjet())
                        manager.managerGlobal.addEtre(animalNew)
                        print("un bebe est né",self.typeObjet())
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
        self.feeding=10
        #A voir avec les humains
        self.escape=random.choice(range(25,75)) 
        self.directionDeFuite=[]
    def printCoord(self):
        print(self.position)
    
    def typeObjet(self):
        return 'sheep'

#un hunter peut être soit un loup qui a loupé son coup soit un humain
    def fuir(self,hunter): 
        fromHunter=[self.position[0]-hunter.position[0],self.position[1]-hunter.position[1]]
        self.directionDeFuite=[-fromHunter[0],-fromHunter[1]]        
            
#    def moveFuir(self):
#        i,j=self.directionDeFuite
#        a=i
#        b=j
#        count=0
#        while self.move([a,b]):
#            if count==0:
#                a=-i
                            
    def nourrir(self):
        self.jaugeNourriture=self.jaugeNourriture+self.feeding
        gaia.addHerbes(self.position)

    def deplacement(self):
        rand1=random.choice([-1,0,1])
        rand2=random.choice([-1,0,1])
        move=self.move((rand1,rand2))
        while (move==0)&(rand1==0)&(rand2==0):
            rand1=random.choice([-1,0,1])
            rand2=random.choice([-1,0,1])
            move=self.move((rand1,rand2))

    def choix(self):
        rand=random.randint(1,100)
        if (iamap.matrixglobal[self.position[0]][self.position[1]].has_property("noHerbes")|iamap.matrixglobal[self.position[0]][self.position[1]].has_property("beach")|iamap.matrixglobal[self.position[0]][self.position[1]].has_property("baies")|iamap.matrixglobal[self.position[0]][self.position[1]].has_property("tree")):
                self.deplacement()
        else:
             
            if (rand>((500-self.jaugeNourriture)/5)):
                #|(len(iamap.iamapglobal.matrix[self.position[0]][self.position[1]].have)>1):
                self.deplacement()
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
                    if self.gender=="F":
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

    def __init__(self,position):
        Animal.__init__(self,"resources/Wolf.png",0.4,position)
        #A voir avec les humains
        self.force=random.choice(range(50,100)) 
        self.distanceDeRecherche=10
        self.nourriture=0
        self.cheminNourriture=[]
        
    def typeObjet(self):
        return 'wolf'

#On  regarde si la cible fuit ou pas.    
    def attaquer(self,target):
        i,j=self.position
        
        if (abs(i-x)+abs(j-y))<2:
            if self.force>target.escape:
                #La nourriture sur pate ne fuit pas et se laisse manger
                target.notMove()
                return True
            else:
                target.fuir(self)
                self.nourriture=0
                self.cheminNourriture=[]
                return False
        else:
            return True
 #       if (abs(i-x)+abs(j-y))<2:
              
            
        
    def chercheNourriture(self):
        matrix=iamap.matrixglobal
        typeObjet='sheep'
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
                        if(matrix[x][y].has_property(typeObjet)):
                            jaugeMax=0
                            for animal in matrix[x][y].getAnimal(typeObjet):
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
            move=self.move((random.choice([-1,0,1]),random.choice([-1,0,1])))
            
    def nourrir(self,nourriture):
        if (nourriture.etat=='vivant')&(self.position==nourriture.position):
            self.jaugeNourriture=self.jaugeNourriture+nourriture.jaugeNourriture
            nourriture.mort()
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
                #elif (self.attaquer(self.nourriture)):
                elif self.cheminNourriture==[]:
                    self.cheminNourriture=self.rejoindreConjoint(self.nourriture)
                elif self.cheminNourriture != []:
                        self.setPos(self.cheminNourriture[0])
                        self.cheminNourriture.remove(self.cheminNourriture[0])
        else:
            if (self.isFecond())&(self.target.isFecond()):
                if self.position==self.target.position:
                    if self.gender=="F":
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

