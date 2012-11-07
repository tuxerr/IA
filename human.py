import random

class Human:
    """A human is defined by the following characteristics:
    -gender
    -age
    -life gauge
    -fatigue gauge
    -% of chance to kill a wild animal"""

    def __init__(self):
        self.age = 0
        self.lifeGauge = 100 # max=100 arbitraire, a changer si besoin
        self.fatigueGauge = 100 # idem
        self.isMale = random.choice([True, False])
        self.chanceToKill = 0 # nom pas top



