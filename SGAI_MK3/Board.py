import random as rd
from Person import Person

class Board:
    """
    Stores the game board.
    """
    
    def __init__(self, dimensions, offset, cell_size, role):
        self.rows = dimensions[0]
        self.columns = dimensions[1]
        self.offset = offset
        self.cell_size = cell_size
        self.player_role = role
        self.population = 0
        self.people = []    # stores a list of all people (healthy and infected)
        self.state = []     # stores the current inhabitant of each location (in 1D index)
        self.QTable = []    # To be used for reinforcement learning
        for s in range(self.rows * self.columns):
            self.QTable.append([0] * 6)
            self.state.append(None)

    def num_infected(self):
        """
        Returns the number of infected people currently on the board.
        """
        infected_count = 0
        for person in self.people:
            if person.isInfected:
                infected_count += 1
        return infected_count
    
    def get_possible_moves(self, action, role):
        """
        Get the coordinates of people that are able to make the specified move.
        action - the action to return possibilities for (options are 'bite', 'moveUp', 'moveDown','moveLeft', 'moveRight', and 'heal')
        role - either 'Zombie' or 'Government'; helps decide whether an action is valid and which people/zombies it applies to
        """
        poss = []
        if role == "Zombie":
            for (index,state) in enumerate(self.state):
                if state is not None:
                    if action == "bite":
                        # if the current space isn't an infected person and it is adjacent a space that is an infected person
                        if not state.isInfected and self.isAdjacentTo(self.toCoord(index), True):
                            poss.append(self.toCoord(state.location))
                    else:
                        if state.isInfected:
                            if action == "moveUp":
                                if self.moveUp(self.toCoord(state.location), False)[0]:
                                    poss.append(self.toCoord(state.location))
                            elif action == "moveDown":
                                if self.moveDown(self.toCoord(state.location), False)[0]:
                                    poss.append(self.toCoord(state.location))
                            elif action == "moveLeft":
                                if self.moveLeft(self.toCoord(state.location), False)[0]:
                                    poss.append(self.toCoord(state.location))
                            elif action == "moveRight":
                                if self.moveRight(self.toCoord(state.location), False)[0]:
                                    poss.append(self.toCoord(state.location))
        """
        elif role == "Government":
            for state in self.state:
                if state.person != None:
                    if action == "heal":
                        if state.person.isZombie or state.person.isVaccinated == False:
                            poss.append(new_board.toCoord(state.location))
                    else:
                        if state.person.isZombie:
                            if action == "moveUp":
                                if new_board.moveUp(new_board.toCoord(state.location)):
                                    poss.append(new_board.toCoord(state.location))
                            elif action == "moveDown":
                                if new_board.moveDown(new_board.toCoord(state.location)):
                                    poss.append(new_board.toCoord(state.location))
                            elif action == "moveLeft":
                                if new_board.moveLeft(new_board.toCoord(state.location)):
                                    poss.append(new_board.toCoord(state.location))
                            elif action == "moveRight":
                                if new_board.moveRight(new_board.toCoord(state.location)):
                                    poss.append(new_board.toCoord(state.location))
        del new_board
        """
        return poss

    def toCoord(self, index):
        return (int(index % self.columns), int(index / self.rows))

    def toIndex(self, coordinates):
        return int(coordinates[1] * self.columns) + int(coordinates[0])

    def isValidCoordinate(self, coordinates):
        return (
            coordinates[1] < self.rows
            and coordinates[1] >= 0
            and coordinates[0] < self.columns
            and coordinates[0] >= 0)

    def clone(self):
        new_board = Board((self.rows, self.columns), self.offset, self.cell_size, self.player_role)
        new_board.state = self.people.copy()
        return new_board

    def isAdjacentTo(self, coord, is_infected: bool):
        ret = False
        vals = [
            (coord[0], coord[1] + 1),
            (coord[0], coord[1] - 1),
            (coord[0] + 1, coord[1]),
            (coord[0] - 1, coord[1]),
        ]
        for coord in vals:
            if self.isValidCoordinate(coord):
                if self.state[self.toIndex(coord)] is not None:
                    if self.state[self.toIndex(coord)].isInfected == is_infected:
                        ret = True
                        break

        return ret

    def move(self, from_coords, new_coords, real):
        """
        Check if the move is valid.
        real - If False, the person will not actually be moved. Set to True if person should be moved.
        If valid, then implement the move and return [True, destination_idx]
        If invalid, then return [False, None]
        If the space is currently occupied, then return [False, destination_idx]
        """

        # Check if the new coordinates are valid
        if not self.isValidCoordinate(new_coords):
            return [False, None]
        
        # Get the start and destination index (1D)
        start_index = self.toIndex(from_coords)
        destination_index = self.toIndex(new_coords)
        
        # Check if the destination is currently occupied
        if self.state[destination_index] is None:
            if real:
                self.state[start_index].location = destination_index    # Set the new location for this person
                self.state[start_index], self.state[destination_index] = self.state[destination_index], self.state[start_index] # Swap the state positions
            return [True, destination_index]
        
        # Return False if destination is occupied
        return [False, destination_index]

    def moveUp(self, coords, real):
        new_coords = (coords[0], coords[1] - 1)
        return self.move(coords, new_coords, real)

    def moveDown(self, coords, real):
        new_coords = (coords[0], coords[1] + 1)
        return self.move(coords, new_coords, real)

    def moveLeft(self, coords, real):
        new_coords = (coords[0] - 1, coords[1])
        return self.move(coords, new_coords, real)

    def moveRight(self, coords, real):
        new_coords = (coords[0] + 1, coords[1])
        return self.move(coords, new_coords, real)

    def bite(self, coords):
        """
        Infect a player.
        Return False if there is no player in the lcoation.
        Return [True, index] if the player has been infected.
        """
        index = self.toIndex(coords)
        
        # Return False if no person is at the location
        if self.state[index] is None:
            return False
        
        # Get odds of infecting a player
        chance = 100
        if self.state[index].isVaccinated:
            chance = 0
        elif self.state[index].wasVaccinated != self.state[index].wasCured:
            chance = 75
        elif self.state[index].wasVaccinated and self.state[index].wasCured:
            chance = 50
            
        # Check if infection will occur
        r = rd.randint(0, 100)
        if r < chance:
            self.state[index].infect_person()
        return [True, index]

    def heal(self, coords):
        """
        Heals the person at the stated coordinates.
        If no person is selected, then return [False, None]
        If person is already cured, then return [False, None]
        if a person has now been healed, then return [True, index]
        If there is no bordering healthy person to the target it will return [False, None]
        """
        index = self.toIndex(coords)
        
        # Return False if no person is at the location
        if self.state[index] is None:
            return [False, None]
        
        # Return False if the person is already cured
        if self.state[index].wasCured:
            return [False, None]

        bordering = False
        for people in self.people:
            if people.distance(index, self) == 1 and not people.isInfected:
                bordering = True
                break
        if not bordering:
            return [False, None]
        # Heal the person
        self.state[index].heal_person()
        return [True, index]

    def populate(self):
        """
        Populate the board with people.
        Clears the existing state list and people list
        """
        
        # Clear the board and player list
        self.state = []
        for s in range(self.rows * self.columns):
            self.state.append(None)
        self.people = []
        
        # Determine how many people to create
        target_population_size = rd.randint(7, int((self.rows * self.columns) / 3))
        
        # Make a list of unique positions to add healthy people
        location_healthy_set = set()    # Use a set for placing people because duplicates will automatically be deleted.
        while len(location_healthy_set) < target_population_size:
            selected_index = rd.randint(0, int(self.rows * self.columns) - 1)
            location_healthy_set.add(selected_index)
        
        # Add healthy people to each of the unique positions
        for index in location_healthy_set:
            this_healthy_person = Person(len(self.people), "Healthy", index)
            self.people.append( this_healthy_person )
            self.state[index] = this_healthy_person
        
        # Set the population attribute
        self.population = len(location_healthy_set)

        # Make a list of some of the created people to change them to "Infected" at random
        location_infected_set = set()
        while len(location_infected_set) < 4:    # Four is an arbitrary number
            selected_index = rd.choice(list(location_healthy_set))  # Have to convert the set to a list in order to select with rd.choice
            location_infected_set.add(selected_index)
        
        # Change the person to infected
        for index in location_infected_set:
            self.state[index].infect_person()
        
    """
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
        reward = self.states[oldstate].evaluate(givenAction, self)
        if f[0] == False:
            reward = 0
        return [reward, f[1]]
        
    def QGreedyat(self, state_id):
        biggest = self.QTable[state_id][0] * self.player_role
        ind = 0
        A = self.QTable[state_id]
        i = 0
        for qval in A:
            if (qval * self.Plplayer_roleayer_Role) > biggest:
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
            if self.player_role == 1:  # Player is Govt
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
            for x in range(len(self.state)):
                if self.state[x].person != None:
                    q = self.QGreedyat(x)
                    if biggest is None:
                        biggest = q[1]
                        sid = x
                    elif q[1] > biggest:
                        biggest = q[1]
                        sid = x
            return self.QGreedyat(sid)
        else:
            if self.player_role == -1:  # Player is Govt
                d = rd.randint(0, len(self.state))
                while self.state[d].person is None or self.state[d].person.isZombie:
                    d = rd.randint(0, len(self.state))
            else:
                d = rd.randint(0, len(self.state))
                while (
                    self.state[d].person is None
                    or self.state[d].person.isZombie == False
                ):
                    d = rd.randint(0, len(self.state))
            return d
    
    def get_possible_states(self, rn):
        indexes = []
        i = 0
        for state in self.state:
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
            rs = rd.randrange(0, len(self.state) - 1)
            if role_number == 1:
                while (
                    self.state[rs].person is not None
                    and self.state[rs].person.isZombie
                ):
                    rs = rd.randrange(0, len(self.state) - 1)
            else:
                while (
                    self.state[rs].person is not None
                    and self.state[rs].person.isZombie == False
                ):
                    rs = rd.randrange(0, len(self.state) - 1)

            # random state and value
        # old_value = QTable[state][acti]
        # next_max = np.max(QTable[next_state])
        # new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        # QTable[state][acti] = new_value
        
    def is_person(self, index):
        # This function loops through all the people and sees if any of them are on the square it seems bad.
        # But, it is a improvement over looping across all tiles if you have a quicker way fix this!
        for people in self.people:
            if people.location == index:
                return people
        return False
    """