from perlin import *

class IAMap:
    
    def __init__(self,width,height):
        self.width,self.height=width,height

        #matrix is a [lines][height] matrix, where [0][0] is bottom left
        self.matrix = [ [ 0 for col in range(height) ] for row in range(width) ]

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

class IAMapCell:
    
    def __init__(self,cell_type):
        self.cell_type = cell_type
        self.properties = [];

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

