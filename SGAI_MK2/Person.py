class Person():
    isVaccinated = False
    wasVaccinated = False
    wasCured = False
    isZombie = False
    turnsVaccinated = 0
    
    def clone(self):
        p = Person(self.isZombie)
        p.turnsVaccinated = self.turnsVaccinated
        p.wasCured = self.wasCured
        p.wasVaccinated = self.wasVaccinated
        p.isVaccinated = self.isVaccinated
        return p
    def display(self):
        print("Person ",self.pid, " at ",self.position)

    def vaccination_step(self):
        self.turnsVaccinated +=1
        if(self.turnsVaccinated > 5):
            self.turnsVaccinated = 0
            self.isVaccinated = False
    def __init__(self, iz) -> None:
        self.isZombie = iz
        pass