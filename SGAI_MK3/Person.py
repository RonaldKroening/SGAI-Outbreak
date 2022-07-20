class Person:
    def __init__(self, id, location):
        # id is Human, Cured, Zombie location is in 1D.
        self.id = id
        self.location = location
        self.wasVaccinated = False
        self.turnsVaccinated = 0
        self.isVaccinated = False
        self.isZombie = False
        self.wasCured = False

    def distance(self, other_id):
        first_coord = self.toCoord(self.location)
        second_coord = self.toCoord(other_id)
        a = second_coord[0] - first_coord[0]
        b = second_coord[1] - first_coord[1]
        return math.pow(int(a**2 + b**2), 0.5)

    def nearest_zombie(self, GameBoard):
        smallest_dist = 100
        for state in GameBoard.states:
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
        print("moves ", moves)
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
