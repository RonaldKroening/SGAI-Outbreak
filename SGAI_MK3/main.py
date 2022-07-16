import pygame
from Board import Board
import PygameFunctions as PF
import random as rd


rows = 6
columns = 6
bd = (rows, columns)

role = "Government"
rn = 1
if role == "Zombie":
    rn = -1
GameBoard = Board(bd, rn)
GameBoard.populate()
print("Board Population: ", GameBoard.population)
action_space = ["moveUp", "moveDown", "moveLeft", "moveRight", "heal", "bite"]
running = True
QTable = []
alpha = 0.1
gamma = 0.6
epsilon = 0.1

r = rd.uniform(0.0, 1.0)

take_action = []

self_play = True  # Change to false
playerMoved = False

pygame.init()
epochs = 1000
epochs_ran = 0
Original_Board = GameBoard.clone(GameBoard.States, GameBoard.Player_Role)
while running:
    P = PF.run(GameBoard, bd)
    if self_play:
        for event in P:
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                action = PF.get_action(GameBoard, x, y)
                c = (int((x - 150) / 100), int((y - 150) / 100))
                if action == "heal":
                    if "heal" not in take_action:
                        take_action.append("heal")
                elif (
                    GameBoard.toIndex(c) < (rows * columns)
                    and GameBoard.toIndex(c) > -1
                ):
                    if "move" not in take_action and len(take_action) == 0:
                        take_action.append("move")
                        ["move", (2, 3), (2, 2)]
                    take_action.append(c)
                if len(take_action) > 1:
                    if take_action[0] == "move":
                        if len(take_action) > 2:
                            directionToMove = PF.direction(
                                take_action[1], take_action[2]
                            )
                            g = False
                            if directionToMove == "moveUp":
                                print("goin to ", directionToMove)
                                g = GameBoard.moveUp(take_action[1])
                            elif directionToMove == "moveDown":
                                print("goin to ", directionToMove)
                                g = GameBoard.moveDown(take_action[1])
                            elif directionToMove == "moveLeft":
                                print("goin to ", directionToMove)
                                g = GameBoard.moveLeft(take_action[1])
                            elif directionToMove == "moveRight":
                                print("goin to ", directionToMove)
                                g = GameBoard.moveRight(take_action[1])
                            playerMoved = True
                    elif take_action[0] == "heal":
                        print("Heal person at ", take_action[1])
                        take_action = []
                        playerMoved = True
                if playerMoved:
                    playerMoved = False
                    take_action = []
                    print("Enemy turn")
                    # Random Zombie Move
                    ta = ""
                    if role == "Government":
                        r = rd.randint(0, 5)
                        while r == 4:
                            r = rd.randint(0, 5)
                        ta = action_space[r]
                    else:
                        r = rd.randint(0, 4)
                        ta = action_space[r]
                    poss = GameBoard.get_possible_moves(ta, "Zombie")
                    r = rd.randint(0, len(poss) - 1)
                    a = poss[r]
                    G = False
                    if ta == "moveUp":
                        G = GameBoard.moveUp(a)
                    elif ta == "moveDown":
                        G = GameBoard.moveDown(a)
                    elif ta == "moveLeft":
                        G = GameBoard.moveLeft(a)
                    elif ta == "moveRight":
                        G = GameBoard.moveRight(a)
                    elif ta == "bite":
                        G = GameBoard.bite(a)
                    elif ta == "heal":
                        G = GameBoard.heal(a)
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    else:
        if epochs_ran % 100 == 0:
            print("Board Reset!")
            GameBoard = Original_Board  # reset environment
        for event in P:
            i = 0
            r = rd.uniform(0.0, 1.0)
            st = rd.randint(0, len(GameBoard.States))
            state = QTable[st]
            if r < gamma:
                while GameBoard.States[st].person is None:
                    st = rd.randint(0, len(GameBoard.States))
            else:
                biggest = None
                for x in range(len(GameBoard.States)):
                    arr = QTable[x]
                    exp = sum(arr) / len(arr)
                    if biggest is None:
                        biggest = exp
                        i = x
                    elif biggest < exp and role == "Government":
                        biggest = exp
                        i = x
                    elif biggest > exp and role != "Government":
                        biggest = exp
                        i = x
                state = QTable[i]
            b = 0
            j = 0
            ind = 0
            for v in state:
                if v > b and role == "Government":
                    b = v
                    ind = j
                elif v < b and role != "Government":
                    b = v
                    ind = j
                j += 1
            action_to_take = action_space[ind]
            old_qval = b
            old_state = i

            reward = GameBoard.act(old_state, action_to_take)
            ns = reward[1]
            NewStateAct = GameBoard.QGreedyat(ns)
            NS = QTable[ns][NewStateAct[0]]
            QTable[i] = QTable[i] + alpha * (reward[0] + gamma * NS) - QTable[i]
            if GameBoard.num_zombies() == 0:
                print("winCase")

            take_action = []
            print("Enemy turn")
            ta = ""
            if role == "Government":
                r = rd.randint(0, 5)
                while r == 4:
                    r = rd.randint(0, 5)
                ta = action_space[r]
            else:
                r = rd.randint(0, 4)
                ta = action_space[r]
            poss = GameBoard.get_possible_moves(ta, "Zombie")
            r = rd.randint(0, len(poss) - 1)
            a = poss[r]
            G = False
            if ta == "moveUp":
                G = GameBoard.moveUp(a)
            elif ta == "moveDown":
                G = GameBoard.moveDown(a)
            elif ta == "moveLeft":
                G = GameBoard.moveLeft(a)
            elif ta == "moveRight":
                G = GameBoard.moveRight(a)
            elif ta == "bite":
                G = GameBoard.bite(a)
            elif ta == "heal":
                G = GameBoard.heal(a)
            if GameBoard.num_zombies() == GameBoard.population:
                print("loseCase")
            if event.type == pygame.QUIT:
                running = False
