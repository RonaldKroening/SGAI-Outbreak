from State import State
import random as rd
from Person import Person
class Board():
    States = [] 
    QTable = []
    rows = 0
    columns = 0
    population = 0
    Player_Role = 0
    action_space = ["moveUp","moveDown","moveLeft","moveRight","heal","bite"]
    def __init__(self, dimensions, pr):
        self.rows = dimensions[0]
        self.columns = dimensions[1]
        self.Player_Role = pr
        for s in range(dimensions[0] * dimensions[1]):
            self.States.append(State(None,s))
            self.QTable.append(
                [0]*6
            )
    def num_zombies(self):
        r = 0
        for state in self.States:
            if(state.person != None):
                if(state.person.isZombie):
                    r+=1
        return r
    def act(self,oldstate, givenAction):
        cell = self.toCoord(oldstate)
        f = []
        if(givenAction == "moveUp"):
            f = self.moveUp(cell)
        elif(givenAction == "moveDown"):
            f = self.moveDown(cell)
        elif(givenAction == "moveLeft"):
            f = self.moveLeft(cell)
        elif(givenAction == "moveRight"):
            f = self.moveRight(cell)
        elif(givenAction == "heal"):
            f = self.heal(cell)
        elif(givenAction == "bite"):
            f = self.bite(cell)
        reward = self.States[oldstate].evaluate(givenAction, self)
        if(f[0] == False):
            reward = reward * 0
        return [reward,f[1]]
    def get_possible_moves(self,action, role):
        poss = []
        B = self.clone(self.States, self.Player_Role)
        if(role == "Zombie"):
            for state in self.States:
                if(state.person != None):
                    if(action == "bite"):
                        if(state.person.isZombie == False):
                            poss.append(B.toCoord(state.location))
                    else:
                        if(state.person.isZombie):
                            if(action == "moveUp"):
                                if(B.moveUp(B.toCoord(state.location))):
                                    poss.append(B.toCoord(state.location))
                            elif(action == "moveDown"):
                                if(B.moveDown(B.toCoord(state.location))):
                                    poss.append(B.toCoord(state.location))
                            elif(action == "moveLeft"):
                                if(B.moveLeft(B.toCoord(state.location))):
                                    poss.append(B.toCoord(state.location))
                            elif(action == "moveRight"):
                                if(B.moveRight(B.toCoord(state.location))):
                                    poss.append(B.toCoord(state.location))
        elif(role == "Government"):
            for state in self.States:
                if(state.person != None):
                    if(action == "heal"):
                        if(state.person.isZombie or state.person.isVaccinated == False):
                            poss.append(B.toCoord(state.location))
                    else:
                        if(state.person.isZombie):
                            if(action == "moveUp"):
                                if(B.moveUp(B.toCoord(state.location))):
                                    poss.append(B.toCoord(state.location))
                            elif(action == "moveDown"):
                                if(B.moveDown(B.toCoord(state.location))):
                                    poss.append(B.toCoord(state.location))
                            elif(action == "moveLeft"):
                                if(B.moveLeft(B.toCoord(state.location))):
                                    print("validLe")
                                    poss.append(B.toCoord(state.location))
                            elif(action == "moveRight"):
                                if(B.moveRight(B.toCoord(state.location))):
                                    print("validRi")
                                    poss.append(B.toCoord(state.location))
        print("possible: ",poss)
        return poss
    def toCoord(self,i):
        return (int(i % self.columns), int(i/self.rows))

    def toIndex(self,coordinates):
        return int(coordinates[1] *self.rows) + int(coordinates[0])

    def clone(self,L, role):
        NB = Board( (self.rows,self.columns), role )
        NB.States = L
        NB.Player_Role = role
    def moveUp(self, coords):
        i = self.toIndex(coords)
        n = (coords[0],coords[1]-1)
        print("new coords ",n)
        j = int(n[0] % self.columns) + int(n[1] * self.rows)
        try:
            self.States[j].person = self.States[i].person
            self.States[i].person = None
            return [True, j]
        except:
            return [False, j]
    def moveDown(self, coords):
        i = self.toIndex(coords)
        n = (coords[0],coords[1]+1)
        print("new coords ",n)
        j = int(n[0] % self.columns) + int(n[1] * self.rows)
        try:
            self.States[j].person = self.States[i].person
            self.States[i].person = None
            return [True, j]
        except:
            return [False, j]
    def moveLeft(self, coords):
        i = self.toIndex(coords)
        n = (coords[0]-1,coords[1])
        print("new coords ",n)
        j = int(n[0] % self.columns) + int(n[1] * self.rows)
        try:
            self.States[j].person = self.States[i].person
            self.States[i].person = None
            return [True, j]
        except:
            return [False, j]
    def moveRight(self, coords):
        print("moving right")
        i = self.toIndex(coords)
        n = (coords[0]+1,coords[1])
        print("new coords ",n)
        j = int(n[0] % self.columns) + int(n[1] * self.rows)
        print("moving to ",n," index ",j)
        print("person at new index: ",self.States[j].person)
        try:
            self.States[j].person = self.States[i].person
            self.States[i].person = None
            return [True, j]
        except:
            return [False, j]
    
    def QGreedyat(self, state_id):
        biggest = self.QTable[state_id][0]* self.Player_Role
        ind = 0
        A = self.QTable[state_id]
        i = 0
        for qval in A:
            if( (qval * self.Player_Role) > self.biggest):
                biggest = qval
                ind = i
            i+=1
        return [ind, self.QTable[ind]] #action_index, qvalue
    
    def choose_action(self, state_id, lr):
        L = lr * 100
        r = rd.randint(0,100)
        if(r < L):
            return self.QGreedyat(state_id)
        else:
            if(self.Player_Role == 1):# Player is Govt
                d = rd.randint(0,4)
            else:
                d = rd.randint(0,5)
                while(d != 4):
                    d = rd.randint(0,4)
            return d
    
    def choose_state(self, lr):
        L = lr * 100
        r = rd.randint(0,100)
        if(r < L):
            biggest = None
            sid = None
            for x in range(len(self.States)):
                if(self.States[x].person != None):
                    q = self.QGreedyat(x)
                    if(biggest is None):
                        biggest = q[1]
                        sid = x
                    elif(q[1] > biggest):
                        biggest = q[1]
                        sid = x
            return self.QGreedyat(sid)
        else:
            if(self.Player_Role == -1):# Player is Govt
                d = rd.randint(0,len(self.States))
                while(self.States[d].person is None or self.States[d].person.isZombie):
                    d = rd.randint(0,len(self.States))
            else:
                d = rd.randint(0,len(self.States))
                while(self.States[d].person is None or self.States[d].person.isZombie ==  False):
                    d = rd.randint(0,len(self.States))
            return d
    def bite(self,coords):
        i = self.toIndex(coords)
        if(self.States[i] is None):
            return False
        chance = 100
        p = self.States[i].person
        if(p.isVaccinated):
            chance = 0
        elif(p.wasVaccinated != p.wasCured):
            chance = 75
        elif(p.wasVaccinated and p.wasCured):
            chance = 50
        r = rd.randint(0,100)
        if(r < chance):
            newP = p.clone()
            newP.isZombie = True
            self.States[i].person = newP
        return [True, i]
    def heal(self,coords):
        i = self.toIndex(coords)
        if(self.States[i] is None):
            return False
        p = self.States[i].person
        newP = p.clone()
        newP.isZombie = False
        if(newP.wasCured == False):
            newP.wasCured = True
        if(newP.isVaccinated == False):
            newP.isVaccinated = True
            newP.turnsVaccinated = 1
        self.States[i].person = newP
        return [True, i]
    def get_possible_states(self,rn):
        indexes = []
        i=0
        for state in self.States:
            if(state.person != None):
                if(rn == 1 and state.person.isZombie == False):
                    indexes.append(i)
                elif(rn == -1 and state.person.isZombie):
                    indexes.append(i)
            i+=1
        return indexes
    def step(self,role_number, learningRate):
        P = self.get_possible_states(role_number)
        r = rd.uniform(0, 1)
        if(r < learningRate):
            rs = rd.randrange(0,len(self.States)-1)
            if(role_number == 1):
                while(self.States[rs].person is not None and self.States[rs].person.isZombie):
                    rs = rd.randrange(0,len(self.States)-1)
            else:
                while(self.States[rs].person is not None and self.States[rs].person.isZombie == False):
                    rs = rd.randrange(0,len(self.States)-1)
                    
            #random state and value
        # old_value = QTable[state][acti]
        # next_max = np.max(QTable[next_state])
        # new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        # QTable[state][acti] = new_value
    def populate(self):
        total = rd.randint(7,((self.rows * self.columns) / 3))
        poss = []
        for x in range(len(self.States)):
            r = rd.randint(0,100)
            if(r < 60 and self.population < total):
                p = Person(False)
                self.States[x].person = p
                self.population =  self.population + 1
                poss.append(x)
            else:
                self.States[x].person = None
        print("people at ",poss)
        used = []
        for x in range(4):
            s = rd.randint(0,len(poss)-1)
            while(s not in used):
                s = rd.randint(0,len(poss)-1)
            self.States[poss[s]].person.isZombie = True
            used.append(s)