from Person import Person
import math


class State:
    def __init__(self, p: Person, i) -> None:
        self.person = p
        self.location = i
        pass
    def distance(self, other_id):
        first_coord = self.toCoord(self.location)
        second_coord = self.toCoord(other_id)
        a = second_coord[0] - first_coord[0]
        b = second_coord[1] - first_coord[1]
        
        return math.pow(int(a**2 + b**2), 0.5)

    def nearest_zombie(self, GameBoard):
        smallest_dist = 100
        for state in GameBoard.States:
            if state.person != None:
                if state.person.isZombie:
                    d = self.distance(GameBoard, state.location)
                    if d < smallest_dist:
                        smallest_dist = d
        return smallest_dist

    def evaluate(self, action, GameBoard):
        reward = 0
        reward += self.nearest_zombie(GameBoard) - 3
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

    def adjacent(self, GameBoard):
        newCoord = GameBoard.toCoord(self.location)
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
                or move[0] > GameBoard.columns
                or move[1] < 0
                or move[1] > GameBoard.rows
            ):
                remove.append(i)
        remove.reverse()
        for r in remove:
            moves.pop(r)
        return moves

    def clone(self):
        return State(self.person, self.location)
