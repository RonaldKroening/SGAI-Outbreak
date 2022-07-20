import pygame
from Board import Board
import PygameFunctions as PF
import random as rd
from constants import *

SELF_PLAY = True  # whether or not a human will be playing
player_role = "Zombie"  # Valid options are "Government" and "Zombie"
# Create the game board
GameBoard = Board((ROWS, COLUMNS), player_role)
GameBoard.populate()

# Self play variables
alpha = 0.1
gamma = 0.6
epsilon = 0.1
epochs = 1000
epochs_ran = 0
Original_Board = GameBoard.clone(GameBoard.States, GameBoard.player_role)


# Initialize variables
running = True
take_action = []
playerMoved = False
font = pygame.font.SysFont("Comic Sans", 20)


while running:
    P = PF.run(GameBoard)

    if SELF_PLAY:
        if not GameBoard.containsPerson(False):
            PF.display_lose_screen()
            running = False
            continue
        # Event Handling
        for event in P:
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                action = PF.get_action(GameBoard, x, y)
                if action == "heal" or action == "bite":
                    # only allow healing by itself (prevents things like ['move', (4, 1), 'heal'])
                    if len(take_action) == 0:
                        take_action.append(action)
                elif action == "reset move":
                    take_action = []
                elif action is not None:
                    idx = GameBoard.toIndex(action)
                    # action is a coordinate
                    if idx < (GameBoard.rows * GameBoard.columns) and idx > -1:
                        if "move" not in take_action and len(take_action) == 0:
                            # make sure that the space is not an empty space or a space of the opposite team
                            # since cannot start a move from those invalid spaces
                            if (
                                GameBoard.States[idx].person is not None
                                and GameBoard.States[idx].person.isZombie
                                == ROLE_TO_ROLE_BOOLEAN[player_role]
                            ):
                                take_action.append("move")
                            else:
                                continue

                        # don't allow duplicate cells
                        if action not in take_action:
                            take_action.append(action)
            if event.type == pygame.QUIT:
                running = False

        # Display the current action
        PF.screen.blit(
            font.render("Your move is currently:", True, PF.WHITE),
            (800, 400),
        )
        PF.screen.blit(font.render(f"{take_action}", True, PF.WHITE), (800, 450))

        # Action handling
        if len(take_action) > 1:
            if take_action[0] == "move":
                if len(take_action) > 2:
                    directionToMove = PF.direction(take_action[1], take_action[2])
                    result = GameBoard.actionToFunction[directionToMove](take_action[1])
                    if result[0] is not False:
                        playerMoved = True
                    take_action = []

            elif take_action[0] == "heal" or take_action[0] == "bite":
                result = GameBoard.actionToFunction[take_action[0]](take_action[1])
                if result[0] is not False:
                    playerMoved = True
                take_action = []

        # Computer turn
        if playerMoved:
            playerMoved = False
            take_action = []

            # Make a list of all possible actions that the computer can take
            possible_actions = [
                ACTION_SPACE[i]
                for i in range(6)
                if (i != 4 and player_role == "Government")
                or (i != 5 and player_role == "Zombie")
            ]
            possible_move_coords = []
            while len(possible_move_coords) == 0 and len(possible_actions) != 0:
                action = possible_actions.pop(rd.randint(0, len(possible_actions) - 1))
                possible_move_coords = GameBoard.get_possible_moves(
                    action, "Government" if player_role == "Zombie" else "Zombie"
                )

            # no valid moves, player wins
            if len(possible_actions) == 0 and len(possible_move_coords) == 0:
                PF.display_win_screen()
                running = False
                continue

            # Select the destination coordinates
            move_coord = rd.choice(possible_move_coords)

            # Implement the selected action
            GameBoard.actionToFunction[action](move_coord)

            # update the board's states
            GameBoard.update()

        # Update the display
        pygame.display.update()

    else:
        if epochs_ran % 100 == 0:
            print("Board Reset!")
            GameBoard = Original_Board  # reset environment
        for event in P:
            i = 0
            r = rd.uniform(0.0, 1.0)
            st = rd.randint(0, len(GameBoard.States) - 1)
            state = GameBoard.QTable[st]

            if r < gamma:
                while GameBoard.States[st].person is None:
                    st = rd.randint(0, len(GameBoard.States) - 1)
            else:
                biggest = None
                for x in range(len(GameBoard.States)):
                    arr = GameBoard.QTable[x]
                    exp = sum(arr) / len(arr)
                    if biggest is None:
                        biggest = exp
                        i = x
                    elif biggest < exp and player_role == "Government":
                        biggest = exp
                        i = x
                    elif biggest > exp and player_role != "Government":
                        biggest = exp
                        i = x
                state = GameBoard.QTable[i]
            b = 0
            j = 0
            ind = 0
            for v in state:
                if v > b and player_role == "Government":
                    b = v
                    ind = j
                elif v < b and player_role != "Government":
                    b = v
                    ind = j
                j += 1
            action_to_take = ACTION_SPACE[ind]
            old_qval = b
            old_state = i

            # Update
            # Q(S, A) = Q(S, A) + alpha[R + gamma * max_a Q(S', A) - Q(S, A)]
            reward = GameBoard.act(old_state, action_to_take)
            ns = reward[1]
            NewStateAct = GameBoard.QGreedyat(ns)
            NS = GameBoard.QTable[ns][NewStateAct[0]]
            # GameBoard.QTable[i] = GameBoard.QTable[i] + alpha * (reward[0] + gamma * NS) - GameBoard.QTable[i]
            if GameBoard.num_zombies() == 0:
                print("winCase")

            take_action = []
            print("Enemy turn")
            ta = ""
            if player_role == "Government":
                r = rd.randint(0, 5)
                while r == 4:
                    r = rd.randint(0, 5)
                ta = ACTION_SPACE[r]
            else:
                r = rd.randint(0, 4)
                ta = ACTION_SPACE[r]
            poss = GameBoard.get_possible_moves(ta, "Zombie")

            if len(poss) > 0:
                r = rd.randint(0, len(poss) - 1)
                a = poss[r]
                GameBoard.actionToFunction[ta](a)
            if GameBoard.num_zombies() == GameBoard.population:
                print("loseCase")
            if event.type == pygame.QUIT:
                running = False
