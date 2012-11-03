from perlin import *

class IAMap:
    
    def __init__(self,width,height):
        self.width,self.height=width,height

        #matrix is a [lines][height] matrix, where [0][0] is bottom left
        self.matrix = [ [ 0 for col in range(height) ] for row in range(width) ]

    def generate_map(self,conf):
        simplexNoise = SimplexNoise(2000)
        scaleX,scaleY=10,10

        for i in range(0,self.width):
            for j in range(0,self.height):

                rawValue = simplexNoise.noise2(float(i)/scaleX,float(j)/scaleY)
                
                cellType = self.value_to_celltype(rawValue)
                newCell = IAMapCell(cellType)
                self.matrix[i][j] = newCell

    def value_to_celltype(self,rawValue):
        if(rawValue<0):
            cell_type="water"
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

    def __str__(self):
        if self.cell_type=="water":
            return "W"
        elif self.cell_type=="land":
            return "L"

    def __repr__(self):
        return self.__str__()

