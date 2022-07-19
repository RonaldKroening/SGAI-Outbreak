class Person:
    wasVaccinated = False
    turnsVaccinated = 0
    isVaccinated = False
    isZombie = False
    wasCured = False

    def __init__(self, iz):
        self.isZombie = iz

#    def clone(self):
#        ret = Person(self.isZombie)
#        ret.wasVaccinated = self.wasVaccinated
#        ret.turnsVaccinated = self.turnsVaccinated
#        ret.isVaccinated = self.isVaccinated
#        ret.wasCured = self.wasCured
#        return ret

    def __str__(self) -> str:
        return f"Person who is a zombie? {self.isZombie}"

    def __repr__(self) -> str:
        return str(self)
