import random as rd
import math
from Person import Person
import backend
import numpy as np


class Board():
    height = 0
    width = 0
    population = 0
    Census = []
    QTable = []
    turns = 0
    #0,1,2,3,4,5,6
    def distance(self,coord1, coord2):
        a = coord2[0] - coord1[0]
        b = coord2[1] - coord1[1]
        a = a*a
        b = b*b
        return math.pow(a+b,0.5)
    def f(self, x):
        return int((-3*x)+9)
    def inverse_action(self, act):
        if(act == "moveUp"):
            return "moveDown"
        elif(act == "moveDown"):
            return "moveUp"
        elif(act == "moveLeft"):
            return "moveRight"
        elif(act == "moveRight"):
            return "moveLeft"
        elif(act == "bite"):
            return "heal"
        else:
            return "reset_vax"

    def toId (self, coord):
        x = coord[0] + (coord[1]*self.height)
        return int(x)
    def evaluate(self):
        reward = 0
        i=0
        for person in self.Census: #Reward on person's proximity to zombie
            if(person != None):
                zombies = self.all_zombies()
                for zombieID in zombies:
                    a = self.toCoord(i)
                    b = self.toCoord(zombieID)
                    dist = self.distance(a,b)
                    reward = reward + (self.f(dist))
                i+=1
                if(len(zombies) == 1 and self.turns > 5):
                    reward = reward ** 2
        reward = reward - (2*len(self.all_zombies())) #Reward on total Zombies
        for person in self.Census:
            if(person != None):
                if(person.isVaccinated):
                    reward = reward + 5
                elif(person.wasCured or person.wasVaccinated):
                    reward = reward + 2
                elif(person.isZombie == False):
                    reward = reward + 1
        return reward
    def duplicate_person(self, per):
        np = Person(per.isZombie)
        np.turnsVaccinated = per.turnsVaccinated
        np.isVaccinated = per.isVaccinated
        np.wasCured = per.wasCured
        np.wasVaccinated = per.wasVaccinated
        return np
    def best_zombie_act(self):
        Z = self.all_zombies()
        reward = 999999
        B = self.clone()
        best_id = 0
        best_act = ""
        for zom in Z:
            ret = self.get_best_action_at(zom,1)
            if(ret[1] < reward):
                best_act = ret[0]
                best_id = zom
                reward = ret[1]
        return [best_act,best_id]
    def display_q(self):
        actionSpace = ["moveUp","moveDown","moveLeft","moveRight","bite","heal"]
        r = " | ".join(actionSpace)
        top = "State |"+r
        print(r)
        for x in range(len(self.Census)):
            s = str(x) + " | "+ " | ".join(self.QTable[x])
            print(s)
    def all_people(self):
        p = []
        i = 0
        for people in self.Census:
            if(people != None):
                if(people.isZombie == False):
                    p.append(self.toCoord(i))
            i+=1
        return p
    def step(self,action):
        A = self.act(str(action[0]),action[1])
        print(A)
        # print("action is ",action[0])
        if(action[1] == True):
            self.Census = A[0].Census
        done = False
        if(len(A[0].all_zombies()) == 1 and self.turns > 5):
            done = True
        reward = self.evaluate()
        chance = 1
        person = self.Census[self.toId(action[1])]
        if(action == "bite"):
            if(person.isVaccinated or person == None):
                chance = 0
            elif(person.wasCured != person.wasVaccinated):
                chance = .75
            elif(person.wasCured and person.wasVaccinated):
                chance = .5
        elif(action == "heal" and person.isZombie and self.turns < 5):
            chance = 0
        reward = reward * chance
        best_R = 0
        best_id = 0
        for x in range(35):
            Arr = self.QTable[x].copy()
            Arr.sort()
            Arr.reverse()
            if(Arr[0] >= best_R):
                best_R = Arr[0]
                best_id = Arr.index(Arr[0])
        self.turns += 1
        return [best_id, reward, done]
    def toCoord(self,i):
        #1
        a = i / self.height
        return (int(i%self.width) , int(a) )
    
    def movement(self,coord1, coord2):
        if(coord1[0] > coord2[0]):
            return "left"
        elif(coord1[0] < coord2[0]):
            return "right"
        elif(coord1[1] > coord2[1]):
            return "up"
        elif(coord1[1] < coord2[1]):
            return "down"
    def adjacent(self, pos):
        toCheck = [(pos[0],pos[1]-1),(pos[0],pos[1]+1),(pos[0]+1,pos[1]),(pos[0]-1,pos[1]),]
        valid = []
        for p in toCheck:
            if(p[0] >-1 and p[0]< self.width and p[1] >-1 and p[1]< self.height):
                valid.append(p)
        return valid
    
    def all_zombies(self):
        ids = []
        i=0
        for p in self.Census:
            if(p != None):
                if(p.isZombie):
                    ids.append(i)
            i+=1
        return ids
    def populate_random(self):
        people = rd.randint(5,int(len(self.Census) / 4))
        i = rd.randint(0,len(self.Census))
        used = []
        self.population = people
        for x in range(people):
            p = Person(False)
            p.isVaccinated = False
            p.wasCured  = False
            p.wasVaccinated = False
            p.turnsVaccinated = 0
            while(i in used):
                i = rd.randint(0,len(self.Census)-1)
            used.append(i)
            self.Census[i] = p
            
    def validMove(self, move, coordinates):
        newC = (0,0)  
        if(move == "bite"):
            A = self.adjacent(coordinates)
            if(self.Board[self.toId(coordinates)].isZombie):
                return False
            else:
                for a in A:
                    if(self.Census[self.toId(a)].isZombie):
                        return True
                return False
        elif(move== "heal"):
            if(self.Census[self.toId(coordinates)].isVaccinated):
                return False
            return True
        else:
            try:
                i = self.toId(coordinates)
                s = self.Census[i]
                if(s != None):
                    return False #space occupied
                return True
            except:
                return False

        
    
    def moveUp(self, coordinates):
        newBoard = self.clone()
        try:
            newC= (coordinates[0],coordinates[1]-1)
            newBoard.Census[self.toId(newC)]=newBoard.Census[self.toId(coordinates)]
            newBoard.Census[self.toId(coordinates)] = None
            return [newBoard, self.validMove("moveUp",newC)]
        except:
            return [newBoard, False]
    
    def act(self,action, coordinates):
        new_board = self.clone()
        actRet = getattr(self, action)(coordinates)
        return actRet
        
    def moveDown(self, coordinates):
        newBoard = self.clone()
        try:
            newC= (coordinates[0],coordinates[1]+1)
            newBoard.Census[self.toId(newC)]=newBoard.Census[self.toId(coordinates)]
            newBoard.Census[self.toId(coordinates)] = None
            return [newBoard, self.validMove("moveDown",newC)]
        except:
            return [newBoard, False]
        
    def moveLeft(self, coordinates):
        newBoard = self.clone()
        try:
            newC= (coordinates[0]-1,coordinates[1])
            newBoard.Census[self.toId(newC)]=self.Census[newBoard.toId(coordinates)]
            newBoard.Census[newBoard.toId(coordinates)] = None
            return [newBoard, self.validMove("moveLeft",newC)]
        except:
            return [newBoard, False]
    
    def think(self,Engine, cellId):
        r = rd.randint(0,100)
        act = 0
        if(r > 50):
            act = rd.randint(0,5) # 0= moveup, 1= movedown, 2= moveleft, 3= moveright, 4= heal, 5= bite
        else:
            Arr = self.QTable[cellId].clone()
            m = max(Arr)
            i = Arr.index(m)
            act = i
        return Board.act(backend.actionSpace[act],self.toCoord(cellId))
            
    
    def update_q_table(self, actnum, l,dis, old_id, id_for_action, reward):
        self.QTable[old_id]= [actnum] = (1-l)*self.QTable[old_id]+ l*(reward+ dis*self.QTable[id_for_action][self.get_best_action_at(id_for_action,-1)])
    def get_best_action_at(self, atid,r):
        coords = self.toCoord(atid)
        actions = backend.actionSpace
        best_reward = 0
        best_action = ""
        for action in actions:
            person = self.Census[atid]
            N = self.act(action,coords)
            chance = 1
            if(action == "bite"):
                if(person.isVaccinated or person == None or r == -1 or person.isZombie):
                    chance = 0
                elif(person.wasCured != person.wasVaccinated):
                    chance = .75
                elif(person.wasCured and person.wasVaccinated):
                    chance = .5
            elif(action == "heal" and r == 1):
                chance = 0
            a = N[0].evaluate() * chance
            r = abs(a)
            if(r > abs(best_reward)):
                a = best_reward
                best_action = action
        return [best_action,best_reward]
    
    def reset_vax(self, coordinates):
        newBoard = self.clone()
        try:
            newP = self.Census[self.toId(coordinates)].clone()
            if(newP.isVaccinated):
                newP.isVaccinated = False
                newP.wasVaccinated = False
                newP.turnsVaccinated = 0
            newBoard.Census[self.toId(coordinates)] = newP
            
            return [newBoard, self.validMove("resetVax",coordinates)]
        except:
            return [newBoard, False]
    def moveRight(self, coordinates):
        newBoard = self.clone()
        try:
            newC= (coordinates[0]+1,coordinates[1])
            newBoard.Census[self.toId(newC)]=self.Census[newBoard.toId(coordinates)]
            newBoard.Census[newBoard.toId(coordinates)] = None
            return [newBoard, self.validMove("moveRight",newC)]
        except:
            return [newBoard, False]
        
    def heal(self, coordinates):
        newBoard = self.clone()
        try:
            newP = self.Census[self.toId(coordinates)].clone()
            if(newP.isZombie):
                newP.isZombie = False
                newP.wasCured = True
            if(newP.isVaccinated == False):
                newP.isVaccinated = True
                newP.wasVaccinated = True
                newP.turnsVaccinated = 1
            newBoard.Census[self.toId(coordinates)] = newP
            
            return [newBoard, self.validMove("heal",coordinates)]
        except:
            return [newBoard, False]
    
    def bite(self, coordinates):
        newBoard = self.clone()
        try:
            newP = self.Census[self.toId(coordinates)].clone()
            if(newP.isZombie == False):
                r = rd.randint(0,100)
                chance = 0
                if(newP.isVaccinated):
                    chance = 100
                elif(newP.wasCured != newP.wasVaccinated):
                    chance = 25
                elif(newP.wasCured and newP.wasVaccinated):
                    chance = 50
                if(chance < r):
                    newP.isZombie = True
            newBoard.Census[self.toId(coordinates)] = newP
            return [newBoard, self.validMove("bite",coordinates)]
        except:
            return [newBoard, False]
        
    def clone(self):
        newBoard = Board(self.width, self.height)
        newBoard.Census = self.Census.copy()
        newBoard.QTable= self.QTable
        newBoard.turns = self.turns
        return newBoard
    def __init__(self, w,h):
        self.height = h
        self.width = w
        size = h*w
        for x in range(size):
            self.Census.append(None)
            self.QTable.append(
                [0,0,0,0,0,0]
            )
        