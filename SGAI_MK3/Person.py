import random as rd


class Person:
    def __init__(self, iz: bool):
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

    def get_bitten(self):
        """
        Decides whether a person becomes a zombie after getting bitten
        The chance of bite infection is:
        - 100% for a person who has never been vaccinated or cured
        - 75% for a person who has been vaccinated or cured but not both
        - 50% for a person who has been vaccinated and cured
        - 0% for a person who is currently vaccinated
        """
        chance = 1
        if self.isVaccinated:
            chance = 0
        elif self.wasVaccinated and self.wasCured:
            chance = 0.50
        elif self.wasVaccinated or self.wasCured:
            chance = 0.75

        if rd.random() < chance:
            self.isZombie = True

    def get_vaccinated(self):
        self.wasVaccinated = True
        self.isVaccinated = True
        self.turnsVaccinated = 1

    def get_cured(self):
        self.isZombie = False
        self.wasCured = True

    def update(self):
        if self.isVaccinated:
            self.turnsVaccinated += 1
        if self.turnsVaccinated > 5:
            self.isVaccinated = False
            self.turnsVaccinated = 0

    def __str__(self) -> str:
        return f"Person who is a zombie? {self.isZombie}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, __o: object) -> bool:
        if type(__o) == Person:
            return (
                self.wasVaccinated == __o.wasVaccinated
                and self.turnsVaccinated == __o.turnsVaccinated
                and self.isVaccinated == __o.isVaccinated
                and self.isZombie == __o.isZombie
                and self.wasCured == __o.wasCured
            )
        return False
