import random
from etre import *
from lifeExpectancy import *
from iamap import *

class Human(Etre):
    """Un humain est defini par :
    - position
    - age
    - jauge de nourriture
    - jauge de fatigue
    - genre
    - % de chance de tuer un animal sauvage lors d'un combat
    - memoire forme (ressource, x, y)
    la ressource pouvant etre "batFood", "batWood", "forum", "abri" 
    """

    lifeStep = 0.02 # arbitraire a changer (test avec 0.5)
    currentLife = 0

    def __init__(self, position):
        self.position = position     
        self.age = 0
        self.jaugeNourriture = 100 # max=100 arbitraire
        self.fatigueGauge = 100 # idem
        self.chanceToKill = 0 # nom pas top, init a 0
        self.role = 'enfant'
        self.memory = [] # (ressource,x,y) infini (plus simple)
        self.isIn = False
        self.target = ('none', 0, 0)
        self.listeTarget = [] # liste de (x,y)
        self.chemin = []
        self.food = 0
        self.wood = 0
        super().__init__("resources/worker_water.jpg",position)

    def resetTarget(self):
        self.target = ('none', 0, 0)
        self.listeTarget = []
        self.chemin = []

    def vieilli(self):
        Human.currentLife += Human.lifeStep
        if Human.currentLife == 1:
            self.age +=1
            Human.currentLife = 0

    def mortNaturelle(self, lifeE):
        d100 = random.randint(1, 100)
        if d100 < lifeE.currentMortality(self.age):
            res = True
        else:
            res = False
        return res
        
    def mortDeFaim(self):
        return (self.jaugeNourriture <= 0)

    def move(self,movement):
        super().move(movement)

    def randomExplo(self):
        d8 = random.randrange(1,8)
        if d8 == 1:
            self.move((0,1))
        elif d8 == 2:
            self.move((1,1))
        elif d8 == 3:
            self.move((1,0))
        elif d8 == 4:
            self.move((1,-1))
        elif d8 == 5:
            self.move((0,-1))
        elif d8 == 6:
            self.move((-1,-1))
        elif d8 == 7:
            self.move((-1,0))
        else:
            self.move((-1,1))

    # ressource = baies, tree, batiment (immobile)
    def rechercheRessource(self, ressource):
        matrix = iamap.matrixglobal
        i = self.position[0]
        j = self.position[1]
        for k in range(0,40): #arbitraire
            for x in range(i-k,i+k):
                for y in range(j-k,j+k):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        if(matrix[x][y].has_property(ressource)):
                            return (x,y)
        return(-1,-1)
#
# TODO ajouter les element dans la memoire
#

    # ressource mouvante = mouton, loup
    def rechercheRessourceMouvante(self, typeAnimal):
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
                        if(matrix[x][y].has_property(typeAnimal)):
                            target =  matrix[x][y].getAnimal(typeAnimal)
                            isSearching = False
            distance=distance+1
        return target

    
    # terrain = land, beach, mountain, water, salwater (immobile)
    def rechercheTerrain(self, terrain):
        matrix = iamap.matrixglobal
        i = self.position[0]
        j = self.position[1]
        for k in range(0,40): #arbitraire
            for x in range(i-k,i+k):
                for y in range(j-k,j+k):
                    if((0<x)&(x<len(matrix))&(0<y)&(y<len(matrix))):
                        if(matrix[x][y].cell_type == terrain):
                            return (x,y)
        return(-1,-1)

    def isCorrespond(self, human):
        return((human.isFecond())&(self.gender!=human.gender)&(human.age >15))

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

    """renvoie l'intégralité des batiments correspondants a la demande
    dans une liste non triee (pour le moment plus simple sinon il 
    faudrait d'abord trié par rapport au point actuel puis par 
    rapport au premier de la liste etc...) => amelioration possible
    on trie quand meme le premier"""
    def memoireBatiment(self, batType):
        for (typeMem, x, y) in self.memory:
            matrix = iamap.matrixglobal
            distMin = float("inf")
            cheminMin = []
            if (typeMem == batType):
                (cost, chemin) = self.cheminCibleCout((x,y))
            if (cost < distMin):
                distMin = cost
                cheminMin = chemin
                self.listeTarget.insert(0,(x,y))
            else:
                self.listeTarget.append((x,y))
            self.chemin = cheminMin
        self.target = listeTarget.pop(0)

    def partageMemoire(self, chef, typePartage):
        for (typeMem, x, y) in chef.memory:
            if (typeMem == typePartage):
                if (self.memory.count((typeMem,x,y)) == 0):
                    self.memory.append((typeMem,x,y))
                    
    def supprimeMemoire(self, typeSupprime):
        for (typeMem, x, y) in self.memory:
            if (typeMem == typeSupprime):
                self.memory.remove((typeMem, x, y))
          
    def run(self):
        self.runSurvie()
        role = self.role
        if role == 'enfant':
            self.runEnfant()
        elif role == 'chef':
            self.runChef()
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
        elif role == 'cuisinier':
            self.runCuisinier()
        else:
             print("role inconnu !")
        self.vieilli()
        self.jaugeNourriture = self.jaugeNourriture - 1
        if (self.mortNaturelle() or self.mortDeFaim()):
            self.mort()
            print("human dead")

    """ cuisinier (en plus de surveiller ses jauges)
    la premiere fois : 
    - le chef indique l'emplacement d'un chaudron sans cuisinier
    - target pour le cuisinier chaudron
    description lineaire :
    - va chercher au stockage le plus proche dans sa mémoire
    - vide ou pas de stockage en mémoire -> recherche nouveau
    - prendre nourriture (indiff)
    - retourner chaudron
    - cuisiner pendant n tours (NON FAIT)
    - distribuer
    - cest vide ? on recommence
    description a chaque etape :
    - soit il sait ou aller
    -- chaudron
    -- chercher bouffe
    -- aller voir le chef (forum, pour savoir ou chercher bouffe)
    - soit il sert a manger/cuisine
    -- donc reste sur place
    -- verifie qu'il reste de la nourriture dans le chaudron
    """ 

    # TODO pour l'instant le cuisinier cuisine indéfiniement
    # voir la frequence/ ou demander au chef a chaque remplissage si
    # on continue
    def runCuisinier(self):
        matrix = iamap.matrixglobal
        x = self.position[0]
        y = self.position[1]
        # si on se trouve sur le forum on partage la mémoire du chef
        # le partage de la mémoire est instantannee et relatif au role
        if matrix[x][y].has_property('forum'):
            monChef = matrix[x][y].getHumanByRole('chef')
            self.partageMemoire(monChef, 'stockageNourriture')
            self.memoireBatiment('stockageNourriture')
        (maTarget, x, y) = self.target
        if (maTarget != 'none'): # sait ou aller 
            if (self.position == (x, y)): # il y est
                if (maTarget == 'stockageNourriture'):
                    # tester si il y a bien de la nourriture presente
                    monBatiment = (matrix[x][y].getBatiment())[0]
                    nbSorti = monBatiment.sortirRessource('food', 10-self.food)
                    self.food += nbSorti
                    if (nbSorti > 0): # il y en a on retourne chaudron
                        # tant pis si on est pas "a plein"
                        self.memoireBatiment('MonChaudron')
                    else: # il n'y en a pas on cherche ailleurs
                        if (listeTarget == []):
                            self.memoireBatiment('forum')
                        else:
                            self.target = self.listeTarget.pop(0)
                elif (maTarget == 'MonChaudron'):
                    monBatiment = (matrix[x][y].getBatiment())[0]
                    nbRentre = monBatiment.rentrerRessource('food', self.food)
                    self.food -= nbRentre
                    self.resetTarget()
            else: # il y va
                self.setPos(self.chemin.pop(0))               
        else: # cuisine-sert/verifie (obligatoirement a son chaudron)
            monChaudron = matrix[x][y].getBatiment('chaudron')
            if (monChaudron.fillinFood == 0):
                self.memoireBatiment('stockageNourriture')

    """ cultivateur (en plus de surveiller ses jauges)
    la premiere fois : 
    - le chef indique l'emplacement d'une ferme sans cultivateur
    - target pour le cuisinier ferme
    description lineaire :
    - cultive
    - une fois fini => stockage
    - va chercher au stockage le plus proche dans sa mémoire
    - plein ou pas de stockage en mémoire -> recherche nouveau
    - poser nourriture (indiff)
    - retourner a la ferme
    description a chaque etape :
    - soit il sait ou aller
    -- ferme
    -- poser bouffe
    -- aller voir le chef (forum, pour savoir ou poser bouffe)
    - soit il cultive
    -- donc reste sur place
    -- verifie que le champ n'est pas "plein"
    """ 
     
    def runCultivateur(self):
        matrix = iamap.matrixglobal
        x = self.position[0]
        y = self.position[1]
        # si on se trouve sur le forum on partage la mémoire du chef
        # le partage de la mémoire est instantannee et relatif au role
        if matrix[x][y].has_property('forum'):
            monChef = matrix[x][y].getHumanByRole('chef')
            self.partageMemoire(monChef, 'stockageNourriture')
            self.memoireBatiment('stockageNourriture')
        (maTarget, x, y) = self.target
        if (maTarget != 'none'): # sait ou aller
            if (self.position == (x,y)): #il y est
                if (maTarget == 'stockageNourriture'):
                    # tester si il y a bien de la place
                    monBatiment = (matrix[x][y].getBatiment())[0]
                    nbRentre = monBatiment.rentrerRessource('food', self.food)
                    self.food -= nbRentre
                    if (self.food = 0): # tout est rentre
                        self.memoireBatiment('MonChamp')
                    else: # il n'y en a pas on cherche ailleurs
                        if (listeTarget == []):
                            self.memoireBatiment('forum')
                        else:
                            self.target = self.listeTarget.pop(0)
                elif (maTarget == 'MonChamp'):
                    monBatiment = (matrix[x][y].getBatiment())[0]
                    self.resetTarget()
            else: #il y va
                self.setPos(self.chemin.pop(0))
        else: # cultive son lopin de terre
            monChamp = matrix[x][y].getBatiment('champ')
            if (monChamp.estPlein()):
                self.food += monChamp.recolte()
                self.memoireBatiment('stockageNourriture')
            else:
                monChamp.cultive()


    # a priori methodes qui seront appelées par le chef quand il existera

    def devientCuisinier(self, monChaudron):
        self.role = 'cuisinier'
        self.supprimeMemoire('monChaudron')
        self.memory.append(monChaudron)
        self.target = monChaudron
        (nom, x, y) = monChaudron
        self.chemin = cheminCible((x,y)) 

    def devientCultivateur(self, maFerme):
        self.role = 'cultivateur'
        self.supprimeMemoire('maFerme')
        self.memory.append(maFerme)
        self.target = maFerme
        (nom, x, y) = maFerme
        self.chemin = cheminCible((x,y)) 
