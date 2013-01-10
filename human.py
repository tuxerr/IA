import random
import iamap
import manager
import Gaia
from iamap import *
from manager import *
from Gaia import *
global chef

class Human(Etre):

    def __init__(self,position,role):
        if role=="chef":
            global chef
            self.role=role
            self.memoireChef=[]
#on enregistre l'ensemble des informations qui peuvent posé des problémes
            self.memoireMort=[]
#on suppose que 2 fois le temps de scout permet d'être sur de pas avoir de probleme
            self.reset=100
            self.forum=position
            self.forumObjet=iamap.matrixglobal[self.forum[0]][self.forum[1]].getBatiment("forum")
            super().__init__("resources/water_carrier.png",0.4,position)
            chef=self
        else:
        #Pour nourrire les Loups
            self.jaugeNourriture=100
            self.position=position
            self.role=role
        #Le but du voyage
            self.but=[]
        #direction pour le scout
            self.direction=[]
        #chemin pour le deplacement de tout le monde vers un point precis
            self.chemin=[]
        #position du forum
            self.forum=position
        #survie dés que ça atteint 0 on rentre à la maision
            self.constSurvie=50
            self.survie=self.constSurvie
        #mermoir des vilagoies et autre
        #La memoire est une liste de [type,position]
            self.memoire=[]
        #c'est le champ de vision pour la collecte d'information uniquement
            self.distanceDeRecherche=10
        #C'est le nombre de ressource qu'il possaide, en général 1
            self.ressource=0
        #force du peon
            self.force=random.choice(range(40,90))
            super().__init__("resources/water_carrier.png",0.4,position)
    
###############################Pas utilisé et pas testé##############################            
    def isCorrespond(self, human):
        return((human.isFecond())&(self.gender!=human.gender)&(human.age >15))
    
    def typeObjet(self):
        return 'human'
    
    # plus specifique que ressource specifiquement pour humain
    def rechercheConjoint(self):
        matrix = iamap.matrixglobal
        i = self.position[0]
        j = self.position[1]
        target = 0
        distance = 0
        distanceMax = 40 #arbitraire
        isSearching = True 
        while(isSearching&(distance<distanceMax)):
            for x in range(i-distance,i+distance):
                for y in range(j-distance,j+distance):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        if(matrix[x][y].has_property('human')):
                            for human in matrix[x][y].getHuman():
                                if(self.isCorrespond(human)):
                                    target = human
                                    isSearching = False
            distance=distance+1
        return target

    def cheminCible(self, target):
        matrix = iamap.matrixglobal
        (cout, chemin) = iamap.iamapglobal.A_star(self.position, target)
        return chemin

    def cheminCibleCout(self, target):
        return iamap.iamapglobal.A_star(self.position, target)

    def cheminCibleMouvante(self, target):
        matrix = iamap.matrixglobal
        (cout, chemin) = iamap.iamapglobal.A_star(self.position, target.position)
        return chemin

    """trouver le batiment le plus proche contenant/pouvant contenir
    la type de "ressources" suivant (food, wood, human)"""
    def memoireBatiment(self, contentType):
        for (typeMem, x, y) in self.memory:
            matrix = iamap.matrixglobal
            distMin = float("inf")
            if (contentType == 'food'):
                if (typeMem == 'stockageNourriture' or typeMem == 'forum'):
                    (cout, chemin) = self.cheminCibleCout((x,y))
                    if (cout < distMin):
                        distMin = cout
                        cheminMin = chemin
            elif (contentType == 'wood'):
                if (typeMem == 'stockageBois' or typeMem == 'forum'):
                    (cout, chemin) = self.cheminCibleCout((x,y))
            elif (contentType == 'human'):
                if (typeMem == 'forum' or typeMem == 'abri'):
                    (cout, chemin) = self.cheminCibleCout((x,y))
            if (cout < distMin):
                distMin = cout
                cheminMin = chemin
        if (distMin == float("inf")): 
            res = [(-1,-1)]
        else:
            res = cheminMin
        return res
###################################Fin du non testé############################
###################################Testé utilisé et fonctionne#################

# On ajoute des informations dans la mémoir des villagoies
# On doit donner une liste de recherche
# Scout = [baies,tree,water]
# Bucherons = [tree]
# CueilleursDeBaie =[baies]
# Carrier = [water]
    def miseAjourDeLaMemoire(self,typeL):
        matrix=iamap.matrixglobal
        distance=0
        i=self.position[0]
        j=self.position[1]
        memoire=0
        distanceMax=self.distanceDeRecherche
        while(distance<distanceMax):
            for x in range(i-distance,i+distance):
                for y in range(j-distance,j+distance):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        for typeR in typeL:
                            if(matrix[x][y].has_property(typeR)):
                                memoire=[typeR,[x,y]]
                                if self.memoire.count(memoire)==0:
                                    self.memoire.append(memoire)
            distance=distance+1
#Mise a jour de la mémoir avec le chef
    def appendMemoireChef(self):
        self.utilisationMemoireMort()
        for memoire in self.memoire:
            if chef.memoireChef.count(memoire) == 0:
                chef.memoireChef.append(memoire)

    def utilisationMemoireMort(self):
        for memoire in chef.memoireMort:
            if self.memoire.count(memoire[0]):
                self.memoire.remove(memoire[0])
            
        

    def choixScout(self):
        rand1=random.choice([-1,0,1])
        rand2=random.choice([-1,0,1])
        while (rand1==0)&(rand2==0):
            rand1=random.choice([-1,0,1])
            rand2=random.choice([-1,0,1])
        self.direction=[rand1,rand2]

    def runScout(self):
        if self.survie <= 0 :
            if self.chemin == []:
                (cout, self.chemin) = iamap.iamapglobal.A_star(self.position, self.forum)
            self.setPos(self.chemin[0])
            self.chemin.remove(self.chemin[0])
            if self.position == self.forum:
                self.survie = self.constSurvie
                self.appendMemoireChef()
                self.memoire=[]
                self.direction=[]
        else:
            if self.direction == [] :
                self.choixScout()
            canGo=0
            while canGo == 0:
                canGo=self.move(self.direction)
                if canGo == 0:
                    self.choixScout()
        self.miseAjourDeLaMemoire(["water","tree","baies"])
        self.survie=self.survie-1

    def landNearWater(self,position):
        [i,j]=position
        if not(iamap.matrixglobal[i+1][j+1].has_property("water")):
            res=[i+1,j+1]
        elif not(iamap.matrixglobal[i+1][j].has_property("water")):
            res=[i+1,j]
        elif not(iamap.matrixglobal[i+1][j-1].has_property("water")):
            res=[i+1,j-1]
        elif not(iamap.matrixglobal[i][j+1].has_property("water")):
            res=[i,j+1]
        elif not(iamap.matrixglobal[i][j-1].has_property("water")):
            res=[i,j-1]
        elif not(iamap.matrixglobal[i-1][j+1].has_property("water")):
            res=[i+1,j+1]
        elif not(iamap.matrixglobal[i-1][j].has_property("water")):
            res=[i,j]
        elif not(iamap.matrixglobal[i-1][j-1].has_property("water")):
            res=[i-1,j-1]
        else:
            res=-1
        return res

    def demandeOrdre(self,objet):
        listeObject=[]
        chemin=[]
        coutMin=-1
        coutCurr=0
        memoireL=chef.memoireChef
        for memoire in memoireL:
            if memoire[0]==objet:
                (coutCurr, chemin) = iamap.iamapglobal.A_star(self.position, memoire[1])
                if coutMin==-1:
                    self.chemin=chemin
                    coutMin=coutCurr
                    self.memoire=[memoire]
                    self.but=memoire[1]
                    break
                # elif min(coutMin,coutCurr)==coutCurr:
                #     self.chemin=chemin
                #     coutMin=coutCurr
                #     self.memoire=[memoire]
                #     self.but=memoire[1]
        if len(self.memoire)!=0:
            chef.memoireChef.remove(self.memoire[0])
            chef.memoireMort.append([self.memoire[0],0])
    def demandeWater(self):
        objet="water"
        listeObject=[]
        chemin=[]
        coutMin=-1
        coutCurr=0
        memoireL=chef.memoireChef
        for memoire in memoireL:
            if memoire[0]==objet:
                res=self.landNearWater(memoire[1])
                if res !=-1:
                    (coutCurr, chemin) = iamap.iamapglobal.A_star(self.position, res)
                    if coutMin==-1:
                        self.chemin=chemin
                        coutMin=coutCurr
                        self.memoire=[["water",res]]
                        self.but=res
                        break
                    # elif min(coutMin,coutCurr)==coutCurr:
                    #     self.chemin=chemin
                    #     coutMin=coutCurr
                    #     self.memoire=[["water",res]]
                    #     self.but=res
    def runCueilleur(self):
        if self.memoire != []:
            if self.ressource == 1:
                if self.chemin == []:
                    (cout, self.chemin) = iamap.iamapglobal.A_star(self.position, self.forum)
                self.setPos(self.chemin[0])
                self.chemin.remove(self.chemin[0])
                if self.position == self.forum:
                    self.appendMemoireChef()
                    self.memoire=[]
                    self.ressource=0
                    iamap.matrixglobal[self.forum[0]][self.forum[1]].getBatiment("forum").rentrerRessource("food",1)
                    # chef.memoireChef.remove(["baies",self.but])
                    # chef.memoireMort.append([["baies",self.but],0])
                else:
                    self.miseAjourDeLaMemoire(["baies"])
            else:
                if self.chemin==[]:
                    if self.position==self.but:
                        self.ressource=1
                        #iamap.matrixglobal[self.but[0]][self.but[1]].remove_property("baies")
                        Gaia.gaia.addBaies(self.but)
                    else:
                        print("Erreur dans run Cueilleur")
                else:
                    self.setPos(self.chemin[0])
                    self.chemin.remove(self.chemin[0])
                self.miseAjourDeLaMemoire(["baies"])
        else:
            self.demandeOrdre("baies")

    def runBucheron(self):
        if self.memoire != []:
            if self.ressource == 1:
                if self.chemin == []:
                    (cout, self.chemin) = iamap.iamapglobal.A_star(self.position, self.forum)
                self.setPos(self.chemin[0])
                self.chemin.remove(self.chemin[0])
                if self.position == self.forum:
                    self.appendMemoireChef()
                    self.memoire=[]
                    self.ressource=0
                    iamap.matrixglobal[self.forum[0]][self.forum[1]].getBatiment("forum").rentrerRessource("wood",1)
                    # chef.memoireChef.remove(["tree",self.but])
                    # chef.memoireMort.append([["tree",self.but],0])
                else:
                    self.miseAjourDeLaMemoire(["tree"])
            else:
                if self.chemin==[]:
                    if self.position==self.but:
                        self.ressource=1
                        #iamap.matrixglobal[self.but[0]][self.but[1]].remove_property("tree")
                        Gaia.gaia.addArbres(self.but)
                    else:
                        print("Erreur dans run Bucheron")
                else:
                    self.setPos(self.chemin[0])
                    self.chemin.remove(self.chemin[0])
                self.miseAjourDeLaMemoire(["tree"])
        else:
            self.demandeOrdre("tree")

    def runPorteurEau(self):
        if self.memoire != []:
            if self.ressource == 1:
                if self.chemin == []:
                    (cout, self.chemin) = iamap.iamapglobal.A_star(self.position, self.forum)
                self.setPos(self.chemin[0])
                self.chemin.remove(self.chemin[0])
                if self.position == self.forum:
                    self.ressource=0
                    iamap.matrixglobal[self.forum[0]][self.forum[1]].getBatiment("forum").rentrerRessource("water",1)
                    (cout,self.chemin) = iamap.iamapglobal.A_star(self.position, self.memoire[0][1])
            else:
                if self.chemin==[]:
                    if self.position==self.but:
                        self.ressource=1
                    else:
                        print("Erreur dans run Porteur d'eau")
                else:
                    self.setPos(self.chemin[0])
                    self.chemin.remove(self.chemin[0])
        else:
            self.demandeWater()

    def incMemoireMort(self):
        for memoire in self.memoireMort:
            memoire[1]=memoire[1]+1

    def removeMemoireMort(self):
        for memoire in self.memoireMort:
            if memoire[1]>=self.reset:
                self.memoireMort.remove(memoire)
            

    def runChef(self):
        #Il n'a strictement rien a faire.
        #Il est juste une memoire sur pate
        #print(self.memoireChef)
        self.incMemoireMort()
        self.removeMemoireMort()
        i,j=self.forum
        if self.forumObjet.fillinFood>=3:
            self.forumObjet.videNourriture()
            role=random.choice(['scout','scout','cueilleur','cueilleur','cueilleur','bucheron','porteurEau'])
            human=Human([i,j],role)
            iamap.matrixglobal[self.forum[0]][self.forum[1]].set_have(human)
            iamap.matrixglobal[self.forum[0]][self.forum[1]].set_property("human")
            manager.managerGlobal.addEtre(human)
            print("un ",role,"est né")


#Role utilisé:
#chef scout cueilleur bucheron porteurEau
    def run(self):
        if not(self.notMove):
         #self.runSurvie()
            role = self.role
            if role == 'enfant':
                self.runEnfant()
            elif role == 'chef':
                self.runChef()
            elif role == 'scout':
                self.runScout()
            elif role == 'cultivateur':
                self.runCultivateur()
            elif role == 'eleveur':
                self.runEleveur()
            elif role == 'chasseurLoup':
                self.runChasseurLoup()
            elif role == 'chasseurMouton':
                self.runChasseurMouton()
            elif role == 'cueilleur':
                self.runCueilleur()
            elif role == 'bucheron':
                self.runBucheron()
            elif role == 'porteurEau':
                self.runPorteurEau()
            elif role == 'constructeur':
                self.runConstructeur()
            else:
                self.runCuisinier()
                #        self.vieilli()
                #        self.jaugeNourriture = self.jaugeNourriture - 1
                #        if (self.mortNaturelle() or self.mortDeFaim()):
                #           self.mort()
                #            print("human dead")


    """ cuisinier (en plus de surveiller ses jauges)
    la premiere fois : 
    - le chef indique l'emplacement d'un chaudron sans cuisinier
    - target pour le cuisinier chaudron
    description lineaire :
    - va chercher au stockage le plus proche dans sa mémoire
    - vide ou pas de stockage en mémoire -> recherche nouveau
    - prendre nourriture (indiff)
    - retourner au centre ville (ou case adjacente ?)
    - cuisiner pendant n tours
    - distribuer
    - cest vide ? on recommence
    description a chaque etape :
    - soit il sait ou aller
    -- chercher bouffe
    -- aller voir le chef (forum, pour savoir ou chercher bouffe)
    -- retourner au forum pour cuisiner avec la bouffe
    - soit il sert a manger/cuisine
    -- donc reste sur place
    -- verifie qu'il reste de la nourriture dans le chaudron
    """ 

#TODO memoireCuisine
#TODO improve memoire batiment (a voir en fonction de memoire cuisine)

"""   def runCuisinier(self):
        matrix = iamap.matrixglobal
        x = self.position[0]
        y = self.position[1]
        # si on se trouve sur le forum on partage la mémoire du chef
        # le partage de la mémoire est instantannee et relatif au role
        if matrix[x][y].has_property('forum'):
            monChef = matrix[x][y].getHumanByRole('chef')
            self.memoireCuisine(monChef)
        if (hasTarget): # sait ou aller, qu'il doit se reposer
            if (self.position == self.target.position):
#TODO avancer                
                    
        else: # cuisine-sert/verifie (obligatoirement a son chaudron)
            monChaudron = matrix[x][y].getBatiment('chaudron')
            if (monChaudron.fillinFood == 0):
                chemin = self.memoireBatiment('food') 
                # au moins un res le forum
                # donc a une target pour le tour prochain
"""
#    def run(self):
#        print("run")
