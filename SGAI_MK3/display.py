from hashlib import new
import math
from random import *
from pygame.locals import *
import backend
import random as rd
import pygame
import time
from Board import Board
import matplotlib.pyplot as plt
import numpy as np
def current_milli_time():
    return round(time.time() * 1000)
def build_grid(screen, margin, cell_side, start):
    grid_width = 600
    grid_height = 600
    pygame.draw.rect(screen,BLACK, [start-5,start-5,5,grid_height+10])#left
    pygame.draw.rect(screen,BLACK, [start+grid_width,start-5,5,grid_height+10])#right
    pygame.draw.rect(screen,BLACK, [start-5,start+grid_height,grid_width+10,5])#bottom
    pygame.draw.rect(screen,BLACK, [start-5,start-5,grid_width + 10,5]) #top
    pygame.draw.rect(screen,CELL_COLOR, [start,start,grid_width,grid_height])
    i = start+cell_side
    while(i < start + grid_width):
        pygame.draw.rect(screen,BLACK, [i,start,5,grid_height])
        i += cell_side
    i = start+cell_side
    while(i < start + grid_height):
        pygame.draw.rect(screen,BLACK, [start,i,grid_width,5])
        i += cell_side

def display_image(screen, itemStr, dimensions, position):
    v = pygame.image.load(itemStr).convert_alpha()
    v = pygame.transform.scale(v, dimensions)
    screen.blit(v,position)
    
def display_board(screen, Board, cell_dimensions, grid_start):
    dif = cell_dimensions[0] / 3
    ydif = cell_dimensions[1] / 4
    margin = 5
    i = 0
    for person in Board.Census:
        icon = image_assets[0]
        if(person != None):
            if(person.isZombie):
                icon = image_assets[2]
            elif(person.isVaccinated):
                icon = image_assets[1]
            position = Board.toCoord(i)
            x_start = (position[0] * cell_dimensions[0])+grid_start[0]+(cell_dimensions[0]/3)
            y_pos = (position[1] * cell_dimensions[1])+grid_start[1]+(cell_dimensions[1]/4)
            display_image(screen, icon, (35,60),(x_start,y_pos))
        i += 1
        
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BACKGROUND = "#DDC2A1"
CELL_COLOR = (233,222,188)
boardWidth = 6
boardHeight = 6
BOARD = Board(boardWidth,boardHeight)
BOARD.populate_random()
background_color = "#DDC2A1"
dimensions = (1400, 800)
cell_dimensions = (100,100)
width = dimensions[0]
cell_width = cell_dimensions[0]
cell_height = cell_dimensions[1]
height = dimensions[1]
running = True

image_assets = [
    ("Assets/person_normal.png"),
    ("Assets/person_vax.png"),
    ("Assets/person_zombie.png")
]
player_menu_assets = [
    ("Assets/cure.jpeg")
]

person_image_dimensions = [25,60]
# running = True
# screen = pygame.display.set_mode(dimensions)
# pygame.display.set_caption('Outbreak!')
# pygame.font.init()
# my_font = pygame.font.SysFont('Impact', 30)
# screen.fill(background_color)
# pygame.display.flip()

alpha  = .05
learningRate = .6
QTable = []
grid_start = (150,150)
actionSpace = ["moveUp","moveDown","moveLeft","moveRight","bite","heal"]
def get_action(x,y):
    a = x-grid_start[0]
    b = y-grid_start[1]
    a = a / cell_dimensions[0]
    b = b / cell_dimensions[1]
    if(x > 799 and x < 901 and y > 299 and y < 401):
        return ["heal"]
    elif(a >= 0 and a < Board.width and b >= 0 and b < Board.height):
        return ["move",(a,b)]
    else:
        return None
def duplicate_board(BO):
    B = Board(BO.width, BO.height)
    B.Census = BO.Census
    B.population = BO.population
    B.QTable = BO.QTable
    return B

def possible_boards(BOARD):
    actionSpace = ["moveUp","moveDown","moveLeft","moveRight","bite","heal"]
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
        reward = backend.reward(N)
        #N: board, viability, action, chance
        add_to_q = [N[0], action]
        QTable.append(add_to_q)
    return possible_boards
role = -1 #-1 = govt, 1 = zombie
alpha = 0.1
gamma = 0.6
epsilon = 0.1

# For plotting metrics
all_epochs = []
all_penalties = []

start_cell = 0
while(BOARD.Census[start_cell] == None):
    start_cell = rd.randint(0,len(BOARD.Census)-1)
first_zombie = 0
while(BOARD.Census[first_zombie] == None):
    first_zombie = rd.randint(0,len(BOARD.Census)-1)
nep = BOARD.duplicate_person(BOARD.Census[first_zombie])
nep.isZombie = True
BOARD.Census[first_zombie] = nep
original_board = duplicate_board(BOARD)
xs = []
ys = []
print("People at ",BOARD.all_people())
for i in range(1, 100):
    QTable = BOARD.QTable
    BOARD = original_board
    BOARD.turns = 0
    state = start_cell

    epochs, penalties, reward, = 0, 0, 0
    done = False
    # print("Episode ",i)
    while (done == False):
        print("Turn ",BOARD.turns," Total Zombies: ",len(BOARD.all_zombies()))
        x_val = ((i-1)*100) +epochs 
        xs.append(x_val)
        state = rd.randint(0,35)
        if rd.uniform(0, 1) < (1-gamma):#.35
            action = rd.randint(0,5)
            action = actionSpace[action]
        else:
            action = np.argmax(QTable[state]) # Exploit learned values
            action = actionSpace[action]
        action_make = [action,BOARD.toCoord(state), role]
        start = current_milli_time()
        next_state, reward, done = BOARD.step(action_make) #cell moved to
        print("done: ",done)
        NZ = BOARD.best_zombie_act()
        end = current_milli_time()
        BOARD.act(NZ[0], BOARD.toCoord(NZ[1]))
        if(len(BOARD.all_zombies()) < 2 and BOARD.turns > 5):
            print("you win!")
        print("Zombie decided to ",NZ[0]," the cell at ",BOARD.toCoord(NZ[1]))
        print("Completed step in ",(end-start) / 1000)," seconds. Reward is ",reward
        acti = actionSpace.index(action)
        old_value = QTable[state][acti]
        # print("r:",reward)
        ys.append(reward)
        next_max = np.max(QTable[next_state])
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        QTable[state][acti] = new_value
        BOARD.QTable = QTable
        state = next_state
        epochs += 1
        
    if i % 100 == 0:
        print(f"Episode: {i}")

print("Training finished.\n")

if(len(xs) > len(ys)):
    xs = xs[0:len(ys)]

plt.plot(xs, ys)
  
# naming the x axis
plt.xlabel('Epoch')
# naming the y axis
plt.ylabel('Reward')
  
# giving a title to my graph
plt.title('Q-Learning!')
  
# function to show the plot
plt.show()
# pygame.display.flip()
    
# display_board(screen, BOARD, cell_dimensions, grid_start)
# build_grid(screen,5,cell_width,150)
# pygame.display.update()
# show_menu(screen)

