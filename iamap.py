from perlin import *

class IAMap:
    
    def __init__(self,width,height):
        self.width,self.height=width,height

        #matrix is a [lines][height] matrix, where [0][0] is bottom left
        self.matrix = [ [ 0 for col in range(height) ] for row in range(width) ]
        #Liste de coordonnée des cellules calculées pour A*
        self.cellAnalyse = []
        #Liste de coordonnée des cellues non calculées pour A*
        self.cellNoAnalyse =[]
    def generate_map(self,conf):
        terrainNoise = SimplexNoise(2000)
        treeNoise = SimplexNoise(2000)

        scale=self.width/5
        scaleForest=scale/2

        for i in range(0,self.width):
            for j in range(0,self.height):

                rawValue = terrainNoise.noise2(float(i)/scale,float(j)/scale)
                rawValue=rawValue/2+0.5

                treeValue = treeNoise.noise2(float(i)/scaleForest,float(j)/scaleForest)
                treeValue=treeValue/2+0.5
             
                distanceFromMiddle=sqrt(pow((i-self.width/2),2)+pow((j-self.height/2),2))/(sqrt(self.width*self.width+self.height*self.height)) #distance between 0 and 1
                rawValue=rawValue*pow(1-distanceFromMiddle,8)
                
                cellType = self.value_to_celltype(rawValue)

                newCell = IAMapCell(cellType)
                
                if (treeValue<=conf["taux_arbres"]/100 and newCell.cell_type=="land"):
                    newCell.set_property("tree")

                self.matrix[i][j] = newCell

    def value_to_celltype(self,rawValue):
        if(rawValue<0.05):
            cell_type="water"
        elif(rawValue<0.07):
            cell_type="beach"
        elif(rawValue>0.4):
            cell_type="mountain"
        else:
            cell_type="land"
        
        return cell_type
#Prend en entré le début et l'arrivé du chemin à créer et renvoie un chemin (liste de coordonée
#l'arrivé et le départ sont de la forme [x,y]
    def A_start(self,start,stop):
        print(self.matrix[start[0]][start[1]].cell_type)
        print(self.matrix[stop[0]][stop[1]].cell_type)
        self.matrix[start[0]][start[1]].parent=-1
        self.cellNoAnalyse.append(start)
        currentcell=start
        noEnd=True
        while ((currentcell != stop) & noEnd):
            self.cellNoAnalyse.remove(currentcell)
            self.cellAnalyse.append(currentcell)
            self.voisins(currentcell, stop)
            if (self.cellNoAnalyse.__len__()!=0):
                currentcell = self.cellDistanceMin()
            else:
                noEnd=False
        if (noEnd):    
            chemin=self.pathCreation(stop)
        else:
            chemin=[]
        return chemin
#Calcul les voisins du point, vérifie s'ils sont dans les listes
#Modifie les distances
    def voisins(self,point,stop):
        i=point[0]
        j=point[1]
        cost=10
        if (i > 0):
            self.traitementPoint(point, [i-1,j], stop, cost)    
        if (i < self.height-1):
            self.traitementPoint(point, [i+1,j], stop, cost)
        if (j > 0):
            self.traitementPoint(point, [i,j-1], stop, cost)
        if (j < self.width-1):
            self.traitementPoint(point, [i,j+1], stop, cost)
        cost =14
        if ((i > 0 & j > 0)):
            self.traitementPoint(point, [i-1,j-1], stop, cost)
        if ((i > 0) & (j < self.width-1)):
            self.traitementPoint(point, [i-1,j+1], stop, cost)
        if ((i < self.height-1) & (j > 0)):
            self.traitementPoint(point, [i+1,j-1], stop, cost)
        if ((i < self.height-1) & (j < self.width)):
            self.traitementPoint(point, [i+1,j+1], stop, cost)

#Calcul heuristique
    def manahattan(self,point1,point2):
        distance=0
        distX=abs(point1[0]-point2[0])
        distY=abs(point1[1]-point2[1])
        if (distX>distY):
            distance=distY*14+(distX-distY)*10
        else:
            distance=distX*14+(distY-distX)*10
            
        return distance
    
#Renvoie si le point est déjà Analysé, 1 ou 0
    def isAnalyse(self,point):
        return self.cellAnalyse.count(point)
    
#Renvoie si le point est déjà non Analysé, 1 ou 0
    def isNoAnalyse(self,point):
        return self.cellNoAnalyse.count(point)
    
#Renvoie si le point est connue ou pas
    def isKnow(self,point):
        return (self.isNoAnalyse(point)| self.isAnalyse(point))
    
#Traitement des points du voisinage
#Cost valant 10 si c(c'est en ligne droite, 14 sinon
    def traitementPoint(self,parent,point,stop,cost):
        cellpoint=self.matrix[point[0]][point[1]]
#land/beach
        if ((not self.isKnow(point)) & ((cellpoint.cell_type=="land") |(cellpoint.cell_type=="beach"))):
            cellpoint.parent = parent
            cellpoint.costH = self.manahattan(point, stop)
            cellpoint.costR = self.matrix[parent[0]][parent[1]].costR+cost
            self.cellNoAnalyse.append(point)

#retourne la cellule avec le cout minimum parmis les cellNoAnalyse
#On démontre avant son utilisation le fait que la liste est non vide
    def cellDistanceMin(self):
        cellmin=self.cellNoAnalyse[0]
        minCost=self.matrix[cellmin[0]][cellmin[1]].costF()
        for cell in self.cellNoAnalyse:
            cost=self.matrix[cell[0]][cell[1]].costF()
            if(cost<minCost):
                cellmin=cell
                minCost=cost
        return cellmin
#création du chemin
#il y a pas le start dans le chemin
    def pathCreation(self,stop):
        point=stop
        chemin=[]
        currentParent=self.matrix[point[0]][point[1]].parent
        while (currentParent != -1):
            chemin.append(point)
            currentParent=self.matrix[point[0]][point[1]].parent
            point=currentParent
        chemin.reverse();
        return chemin

class IAMapCell:
    
    def __init__(self,cell_type):
        self.cell_type = cell_type
        self.parent=0 #le parent pour A*, en coordonée  
        self.costH=0  #le coût heuristique pour A*
        self.costR=0  #le coût réel pour A*
        self.properties = [];

    def costF(self):
        return self.costH + self.costR
    
    def set_property(self,new_property):
        self.properties.append(new_property)
    
    def remove_property(self,property_to_remove):
        self.properties.remove(property_to_remove)

    def has_property(self,property_to_test):
        return (property_to_test in self.properties)

    def __str__(self):
        if self.cell_type=="water":
            return "W"
        elif self.cell_type=="land":
            return "L"

    def __repr__(self):
        return self.__str__()

