from tracemalloc import start
from State import State
import random as rd
from Person import Person
from typing import Tuple


class Board:
    def __init__(self, dimensions, offset, cellsize, role):
        self.rows = dimensions[0]
        self.columns = dimensions[1]
        self.offset = offset
        self.cellsize = cellsize
        self.Player_Role = role
        self.population = 0
        self.States = []
        self.QTable = []
        self.People = []
        for s in range(dimensions[0] * dimensions[1]):
            self.QTable.append([0] * 6)

    def num_zombies(self):
        r = 0
        for state in self.States:
            if state.person != None:
                if state.person.isZombie:
                    r += 1
        return r

    def act(self, oldstate, givenAction):
        cell = self.toCoord(oldstate)
        f = []
        if givenAction == "moveUp":
            f = self.moveUp(cell)
        elif givenAction == "moveDown":
            f = self.moveDown(cell)
        elif givenAction == "moveLeft":
            f = self.moveLeft(cell)
        elif givenAction == "moveRight":
            f = self.moveRight(cell)
        elif givenAction == "heal":
            f = self.heal(cell)
        elif givenAction == "bite":
            f = self.bite(cell)
        reward = self.States[oldstate].evaluate(givenAction, self)
        if f[0] == False:
            reward = 0
        return [reward, f[1]]

    def get_possible_moves(self, action, role):
        """
        Get the coordinates of people (or zombies) that are able
        to make the specified move.
        @param action - the action to return possibilities for (options are 'bite', 'moveUp', 'moveDown','moveLeft', 'moveRight', and 'heal')
        @param role - either 'Zombie' or 'Government'; helps decide whether an action
        is valid and which people/zombies it applies to
        """
        poss = []
        B = self.clone()


        if role == "Zombie":
            for idx in range(len(self.States)):
                B.States = [self.States[i].clone() for i in range(len(self.States))]
                state = self.States[idx]
                if state.person is not None:
                    if action == "bite":
                        # if the current space isn't a zombie and it is adjacent
                        # a space that is a zombie
                        if not state.person.isZombie and self.isAdjacentTo(self.toCoord(idx), True):
                            poss.append(B.toCoord(state.location))
                    else:
                        if state.person.isZombie:
                            if action == "moveUp":
                                if B.moveUp(B.toCoord(state.location))[0]:
                                    poss.append(B.toCoord(state.location))
                            elif action == "moveDown":
                                if B.moveDown(B.toCoord(state.location))[0]:
                                    poss.append(B.toCoord(state.location))
                            elif action == "moveLeft":
                                if B.moveLeft(B.toCoord(state.location))[0]:
                                    poss.append(B.toCoord(state.location))
                            elif action == "moveRight":
                                if B.moveRight(B.toCoord(state.location))[0]:
                                    poss.append(B.toCoord(state.location))

        elif role == "Government":
            for state in self.States:
                if state.person != None:
                    if action == "heal":
                        if state.person.isZombie or state.person.isVaccinated == False:
                            poss.append(B.toCoord(state.location))
                    else:
                        if state.person.isZombie:
                            if action == "moveUp":
                                if B.moveUp(B.toCoord(state.location)):
                                    poss.append(B.toCoord(state.location))
                            elif action == "moveDown":
                                if B.moveDown(B.toCoord(state.location)):
                                    poss.append(B.toCoord(state.location))
                            elif action == "moveLeft":
                                if B.moveLeft(B.toCoord(state.location)):
                                    poss.append(B.toCoord(state.location))
                            elif action == "moveRight":
                                if B.moveRight(B.toCoord(state.location)):
                                    poss.append(B.toCoord(state.location))
        del B
        return poss

    def toCoord(self, i):
        return (int(i % self.columns), int(i / self.rows))

    def toIndex(self, coordinates):
        return int(coordinates[1] * self.columns) + int(coordinates[0])

    def isValidCoordinate(self, coordinates):
        return (
            coordinates[1] < self.rows
            and coordinates[1] >= 0
            and coordinates[0] < self.columns
            and coordinates[0] >= 0)

    def clone(self):
        NB = Board((self.rows, self.columns), self.offset, self.cellsize, self.Player_Role)
        NB.States = self.People.copy()
        NB.Player_Role = self.Player_Role
        return NB

    def isAdjacentTo(self, coord, is_zombie: bool) -> bool:
        ret = False
        vals = [
            (coord[0], coord[1] + 1),
            (coord[0], coord[1] - 1),
            (coord[0] + 1, coord[1]),
            (coord[0] - 1, coord[1]),
        ]
        for coord in vals:
            if (
                self.isValidCoordinate(coord)
                and self.States[self.toIndex(coord)].person is not None
                and self.States[self.toIndex(coord)].person.isZombie == is_zombie
            ):
                ret = True
                break

        return ret

    def move(self, from_coords, new_coords) -> Tuple[bool, int]:
        """
        Check if the move is valid.
        If valid, then implement the move and return [True, destination_idx]
        If invalid, then return [False, None]
        If the space is currently occupied, then return [False, destination_idx]
        """
        # Get the start and destination index (1D)
        start_idx = self.toIndex(from_coords)
        destination_idx = self.toIndex(new_coords)
        
        # Check if the new coordinates are valid
        if not self.isValidCoordinate(new_coords):
            return [False, destination_idx]
        
        # Check if the destination is currently occupied
        if self.States[destination_idx].person is None:
            self.States[destination_idx].person = self.States[start_idx].person
            self.States[start_idx].person = None
            return [True, destination_idx]
        return [False, destination_idx]

    def moveUp(self, coords) -> Tuple[bool, int]:
        new_coords = (coords[0], coords[1] - 1)
        return self.move(coords, new_coords)

    def moveDown(self, coords) -> Tuple[bool, int]:
        new_coords = (coords[0], coords[1] + 1)
        return self.move(coords, new_coords)

    def moveLeft(self, coords) -> Tuple[bool, int]:
        new_coords = (coords[0] - 1, coords[1])
        return self.move(coords, new_coords)

    def moveRight(self, coords) -> Tuple[bool, int]:
        new_coords = (coords[0] + 1, coords[1])
        return self.move(coords, new_coords)

    def QGreedyat(self, state_id):
        biggest = self.QTable[state_id][0] * self.Player_Role
        ind = 0
        A = self.QTable[state_id]
        i = 0
        for qval in A:
            if (qval * self.Player_Role) > biggest:
                biggest = qval
                ind = i
            i += 1
        return [ind, self.QTable[ind]]  # action_index, qvalue

    def choose_action(self, state_id, lr):
        L = lr * 100
        r = rd.randint(0, 100)
        if r < L:
            return self.QGreedyat(state_id)
        else:
            if self.Player_Role == 1:  # Player is Govt
                d = rd.randint(0, 4)
            else:
                d = rd.randint(0, 5)
                while d != 4:
                    d = rd.randint(0, 4)
            return d

    def choose_state(self, lr):
        L = lr * 100
        r = rd.randint(0, 100)
        if r < L:
            biggest = None
            sid = None
            for x in range(len(self.States)):
                if self.States[x].person != None:
                    q = self.QGreedyat(x)
                    if biggest is None:
                        biggest = q[1]
                        sid = x
                    elif q[1] > biggest:
                        biggest = q[1]
                        sid = x
            return self.QGreedyat(sid)
        else:
            if self.Player_Role == -1:  # Player is Govt
                d = rd.randint(0, len(self.States))
                while self.States[d].person is None or self.States[d].person.isZombie:
                    d = rd.randint(0, len(self.States))
            else:
                d = rd.randint(0, len(self.States))
                while (
                    self.States[d].person is None
                    or self.States[d].person.isZombie == False
                ):
                    d = rd.randint(0, len(self.States))
            return d

    def bite(self, coords):
        i = self.toIndex(coords)
        if self.States[i] is None:
            return False
        chance = 100
        p = self.States[i].person
        if p.isVaccinated:
            chance = 0
        elif p.wasVaccinated != p.wasCured:
            chance = 75
        elif p.wasVaccinated and p.wasCured:
            chance = 50
        r = rd.randint(0, 100)
        if r < chance:
            p.isZombie = True
            self.States[i].person = p
        return [True, i]

    def heal(self, coords):
        """
        Heals the person at the stated coordinates
        If no person is selected, then return [False, None]
        if a person is vaccined, then return [True, index]
        """
        i = self.toIndex(coords)
        if self.States[i].person is None:
            return [False, None]
        p = self.States[i].person
        p.isZombie = False
        if p.wasCured == False:
            p.wasCured = True
        if p.isVaccinated == False:
            p.isVaccinated = True
            p.turnsVaccinated = 1
        self.States[i].person = p
        return [True, i]

    def get_possible_states(self, rn):
        indexes = []
        i = 0
        for state in self.States:
            if state.person != None:
                if rn == 1 and state.person.isZombie == False:
                    indexes.append(i)
                elif rn == -1 and state.person.isZombie:
                    indexes.append(i)
            i += 1
        return indexes

    def step(self, role_number, learningRate):
        P = self.get_possible_states(role_number)
        r = rd.uniform(0, 1)
        if r < learningRate:
            rs = rd.randrange(0, len(self.States) - 1)
            if role_number == 1:
                while (
                    self.States[rs].person is not None
                    and self.States[rs].person.isZombie
                ):
                    rs = rd.randrange(0, len(self.States) - 1)
            else:
                while (
                    self.States[rs].person is not None
                    and self.States[rs].person.isZombie == False
                ):
                    rs = rd.randrange(0, len(self.States) - 1)

            # random state and value
        # old_value = QTable[state][acti]
        # next_max = np.max(QTable[next_state])
        # new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        # QTable[state][acti] = new_value

    def populate(self):
        targetpopulation = rd.randint(7, int((self.rows * self.columns) / 3))
        # using a set for placing people as then duplicates will automatically be deleted.
        poss = set()
        while len(poss) < targetpopulation:
            selected = rd.randint(0, int(self.rows * self.columns))
            newperson = Person("Human", selected)
            self.People.append(newperson)
            poss.add(selected)
            
        self.population = len(poss)
        used = set()
        # Four is a arbitrary number that just specified starting amount of zombies
        while len(used) < 4:
            s = rd.randint(0, len(poss) - 1)
            used.add(s)
        for i in used:
            self.People[i].isZombie = True
            self.People[i].id = "Zombie"

    def is_person(self, index):
        # This function loops through all the people and sees if any of them are on the square it seems bad.
        # But, it is a improvement over looping across all tiles if you have a quicker way fix this!
        for people in self.People:
            if people.location == index:
                return people
        return False
        
