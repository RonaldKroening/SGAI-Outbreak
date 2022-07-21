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
        self.wasCured = False

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
    """
    def nearest_zombie(self, GameBoard):
        smallest_dist = 100
        for state in GameBoard.state:
            if state.person != None:
                if state.person.isZombie:
                    d = self.distance(state.id)
                    if d < smallest_dist:
                        smallest_dist = d
        return smallest_dist

    def evaluate(self, action, Board):
        reward = 0
        reward += self.nearest_zombie() - 3
        if action == "heal":
            reward += 5
        elif action == "bite" and self.person.isZombie:
            chance = 0
            if self.person.wasVaccinated != self.person.wasCured:
                chance = 0.25
            if self.person.wasVaccinated and self.person.wasCured:
                chance = 0.5
            reward = reward + int(5 * (2 + chance))
        return reward
    
    def adjacent(self, Board):
        newCoord = Board.toCoord(self.location)
        print(newCoord)
        moves = [
            (newCoord[0], newCoord[1] - 1),
            (newCoord[0], newCoord[1] + 1),
            (newCoord[0] - 1, newCoord[1]),
            (newCoord[0] + 1, newCoord[1]),
        ]
        remove = []
        for i in range(4):
            move = moves[i]
            if (
                move[0] < 0
                or move[0] > Board.columns
                or move[1] < 0
                or move[1] > Board.rows
            ):
                remove.append(i)
        remove.reverse()
        for r in remove:
            moves.pop(r)
        return moves
    """