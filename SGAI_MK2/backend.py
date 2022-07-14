import random as rd
import math
import Board
import numpy as np

class Engine():
    role = -1
    learningRate = 0
    alpha = 0
 
    def __init__(self, role, learning, al) -> None:
        self.role = role
        self.learningRate = learning
        self.alpha = al
        pass
    


actionSpace = ["moveUp","moveDown","moveLeft","moveRight","bite","heal"]

def duplicate_board(BO):
    B = Board(BO.width, BO.height)
    B.Census = BO.Census
    B.population = BO.population
    B.QTable = BO.QTable
    return B

def possible_boards(BOARD):
    possible_boards = []
    for action in actionSpace:
        i=0
        for person in BOARD.Census:
            if(person != None):
                coordinates = BOARD.toCoord(i)
                N = BOARD.act(action,coordinates)
                chance = 1
                if(action == "bite"):
                    if(person.isVaccinated):
                        chance = 0
                    elif(person.wasCured != person.wasVaccinated):
                        chance = .75
                    elif(person.wasCured and person.wasVaccinated):
                        chance = .5
                N.append(action)
                N.append(chance)
                possible_boards.append(N)
            i+=1
        reward = reward(N)
        #N: board, action, chance
    return possible_boards

def f(x):
    return int((-3*x)+9)
def Q(state, action,i):
    a = (1-alpha)*QTable[action][i]
    b = learningRate * (state.evaluate() + learningRate * np.max(Q[action]))


def update_q_table(action, index, value):
    Arr = QTable[action].clone()
    Arr[index] = value
    QTable[action] = Arr
def reward(group):
    #role is -1 if govt, 1 if zombie
    BOARD, valid, role, action, chance = group
    i=0
    reward = 0
    if(valid == False):
        return 999*role
    else:
        for person in BOARD.Census: #Reward on person's proximity to zombie
            zombies = BOARD.all_zombies()
            for zombieID in zombies:
                a = BOARD.toCoord(i)
                b = BOARD.toCoord(zombieID)
                dist = BOARD.distance(a,b)
                reward = reward + (2*f(dist))
            i+=1
        reward = reward - (5*len(BOARD.all_zombies())) #Reward on total Zombies
        for person in BOARD.Census:
            if(person.isVaccinated):
                reward = reward + 5
            elif(person.isCured or person.wasVaccinated):
                reward = reward + 2
            elif(person.isZombie == False):
                reward = reward + 1
        if(action == "bite"):
            reward = reward * chance
        return reward
        
        
    