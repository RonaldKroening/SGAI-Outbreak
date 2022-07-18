from Person import Person
import math


class State:
    person = None
    location = 0

    def distance(self, other_id):
        first_coord = self.toCoord(self.location)
        second_coord = self.toCoord(other_id)
        a = second_coord[0] - first_coord[0]
        b = second_coord[1] - first_coord[1]
        a = a * a
        b = b * a
        return math.pow(int(a + b), 0.5)

    def nearest_zombie(self, B):
        smallest_dist = 100
        for state in B.States:
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

    def clone(self):
        if self.person is None:
            return State(self.person, self.location)
        return State(self.person.clone(), self.location)

    def __init__(self, p: Person, i) -> None:
        self.person = p
        self.location = i
        pass
