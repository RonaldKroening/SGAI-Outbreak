import random as rd

class Person:
    """
    Stores information about a single person (any type)
    """
    
    def __init__(self, this_index, this_condition, location):
        self.index = this_index
        self.condition = this_condition     # ["Healthy", "Vaccinated", "Cured", "Infected"]
        self.location = location            # in 1D index
        self.isGovt = False
        self.wasVaccinated = False
        self.turnsVaccinated = 0
        self.isVaccinated = False
        self.isInfected = True if this_condition == "Infected" else False
        self.daysInfected = 0
        self.wasCured = False
        self.infectiousAmount = rd.randint(30,70)    # This determines the chance (0-100%) that a nearby person will also get infected

    def infect_person(self):
        """
        Infects the current person.
        """
        self.condition = "Infected"
        self.isInfected = True
    
    def heal_person(self):
        """
        Heals the current person.
        """
        self.condition = "Cured"
        self.isInfected = False
        self.wasCured = True
        self.isVaccinated = True
        self.turnsVaccinated = 1
    
    def distance(self, other_index, board):
        first_coord = board.toCoord(self.location)
        second_coord = board.toCoord(other_index)
        a = second_coord[0] - first_coord[0]
        b = second_coord[1] - first_coord[1]
        return (a**2 + b**2) ** 0.5