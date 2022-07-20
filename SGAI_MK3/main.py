import pygame
from Board import Board
import PygameFunctions as PF
import random as rd

# Constants
SELF_PLAY = False
ROWS = 20
COLUMNS = 20
OFFSET = 50                    # Number of pixels to offset grid to the top-left side
CELL_DIMENSIONS = 30           # Number of pixels for each cell
ACTION_SPACE = ["moveUp", "moveDown", "moveLeft", "moveRight", "heal", "bite"]

# Player role variables
player_role = "Government"      # Valid options are "Government" and "Zombie"
roleToRoleNum = {"Government": 1, "Zombie": -1}
roleToRoleBoolean = {"Government": False, "Zombie": True}

# Create the game board
GameBoard = Board((ROWS,COLUMNS), OFFSET, CELL_DIMENSIONS, roleToRoleNum[player_role])
GameBoard.populate()

# Self play variables
alpha = 0.1
gamma = 0.6
epsilon = 0.1
epochs = 1000
epochs_ran = 0
Original_Board = GameBoard.clone()

# Initialize variables
running = True
take_action = []
playerMoved = False

# Load images
PF.load_images(GameBoard)

while running:
    PF.run(GameBoard)

    if not SELF_PLAY:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                action = PF.get_action(GameBoard, x, y)
                if action == "heal":                                        # Process a "heal" intention if take_action is currently empty
                    if take_action == []:
                        take_action.append("heal")
                elif action != None:                                        # Otherwise, get the coordinate of a valid grid cell that was clicked
                    index = GameBoard.toIndex(action)                       # Get the corresponding 1D index from the 2D grid location that was clicked
                    if "move" not in take_action and take_action == []:     # Check that the click corresponds to an intention to move a player
                        # Make sure that the space is not an empty space or a space of the opposite team
                        if GameBoard.state[index] is not None:
                            if GameBoard.state[index].isInfected == roleToRoleBoolean[player_role]:
                                take_action.append("move")
                    if take_action != []:                                   # Only append a coordinate if there is a pending "heal" or "move" intention
                        take_action.append(action)
            if event.type == pygame.QUIT:
                running = False
        
        # Display the current action
        PF.display_current_action(take_action)

        # Action handling
        if len(take_action) > 1:
            if take_action[0] == "move":
                if len(take_action) > 2:
                    directionToMove = PF.direction(take_action[1], take_action[2])
                    result = [False, None]
                    if directionToMove == "moveUp":
                        result = GameBoard.moveUp(take_action[1], True)
                    elif directionToMove == "moveDown":
                        result = GameBoard.moveDown(take_action[1], True)
                    elif directionToMove == "moveLeft":
                        result = GameBoard.moveLeft(take_action[1], True)
                    elif directionToMove == "moveRight":
                        result = GameBoard.moveRight(take_action[1], True)
                    if result[0] != False:
                        playerMoved = True
                    take_action = []
            elif take_action[0] == "heal":
                result = GameBoard.heal(take_action[1])
                if result[0] != False:
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
                if (i != 4 and player_role == "Government") or (i != 5 and player_role == "Zombie")
            ]
            
            # Figure out all possible moves and select an action
            possible_move_coords = []
            while len(possible_move_coords) == 0 and len(possible_actions) != 0:
                action = rd.choice(possible_actions)
                possible_move_coords = GameBoard.get_possible_moves(action, "Government" if player_role == "Zombie" else "Zombie")
                possible_actions.remove(action)
            
            # No valid moves, player wins
            if len(possible_actions) == 0 and len(possible_move_coords) == 0:
                PF.display_win_screen()
                running = False
                continue
            
            # Select the destination coordinates
            move_coord = rd.choice(possible_move_coords)
            
            # Implement the selected action
            if action == "moveUp":
                GameBoard.moveUp(move_coord, True)
            elif action == "moveDown":
                GameBoard.moveDown(move_coord, True)
            elif action == "moveLeft":
                GameBoard.moveLeft(move_coord, True)
            elif action == "moveRight":
                GameBoard.moveRight(move_coord, True)
            elif action == "bite":
                GameBoard.bite(move_coord)
            elif action == "heal":
                GameBoard.heal(move_coord)

        # Update the display
        pygame.display.update()
    
    else:
        # Simulate gameplay without player input
        # Use a reinforcement learning approach
        pass
        
    """
    else:
        pass
        if epochs_ran % 100 == 0:
            print("Board Reset!")
            GameBoard = Original_Board  # reset environment
        for event in pygame.event.get():
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
            #GameBoard.QTable[i] = GameBoard.QTable[i] + alpha * (reward[0] + gamma * NS) - GameBoard.QTable[i]
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
                if ta == "moveUp":
                    GameBoard.moveUp(a)
                elif ta == "moveDown":
                    GameBoard.moveDown(a)
                elif ta == "moveLeft":
                    GameBoard.moveLeft(a)
                elif ta == "moveRight":
                    GameBoard.moveRight(a)
                elif ta == "bite":
                    GameBoard.bite(a)
                elif ta == "heal":
                    GameBoard.heal(a)
            if GameBoard.num_zombies() == GameBoard.population:
                print("loseCase")
            if event.type == pygame.QUIT:
                running = False
        """