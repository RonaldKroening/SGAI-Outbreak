class Person:
    def __init__(self, iz):
        self.isZombie = iz
        self.wasVaccinated = False
        self.turnsVaccinated = 0
        self.isVaccinated = False
        self.wasCured = False

    def clone(self):
        ret = Person(self.isZombie)
        ret.wasVaccinated = self.wasVaccinated
        ret.turnsVaccinated = self.turnsVaccinated
        ret.isVaccinated = self.isVaccinated
        ret.wasCured = self.wasCured
        return ret

    def __str__(self) -> str:
        return f"Person who is a zombie? {self.isZombie}"

    def __repr__(self) -> str:
        return str(self)
