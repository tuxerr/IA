
class Batiment:
    # Un batiment est defini par sa position

    def __init__(self, position):
        self.position = position


class CentreVille(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.type = "centreVille"
        self.fillinFood = 0
        self.capacityFood = 20 #arbitraire
        self.fillinWood = 0
        self.capacityWood = 20 #arbitraire
        self.fillinHuman = 0
        self.capacityHuman = 10 #arbitraire


class StockageBois(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.type = "stockageBois"
        self.fillin = 0
        self.capacity = 30 #arbitraire


class StockageNourriture(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.type = "stockageNourriture"
        self.fillin = 0
        self.capacity = 30 #arbitraire


class Abri(Batiment):

    def __init__(self, position):
        Batiment.__init__(self, position)
        self.type = "abri"
        self.fillin = 0
        self.capacity = 10 #arbitraire
