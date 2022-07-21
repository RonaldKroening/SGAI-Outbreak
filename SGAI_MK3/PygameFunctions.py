import pygame
import random as rd

BACKGROUND = "#DDC2A1"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CELL_COLOR = (40, 40, 40)
LINE_WIDTH = 1

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Outbreak!")
pygame.font.init()
font = pygame.font.SysFont("Comic Sans", 20)
screen.fill(BACKGROUND)

# Load images
img_player_govt = None
img_player_healthy = None
img_player_vaccinated = None
img_player_infected = None

def load_images(GameBoard):
    """
    Load all of the game image assets once
    Only blit these on refresh, instead of loading them each time
    TODO: find a way to implement this without using the global method here...
    """
    global img_player_govt
    global img_player_healthy
    global img_player_vaccinated
    global img_player_infected
    img_player_size = (0.8 * GameBoard.cell_size / 2, 0.8 * GameBoard.cell_size)
    img_player_govt = pygame.image.load("Assets/person_govt.png").convert_alpha()
    img_player_govt = pygame.transform.scale(img_player_govt, img_player_size)
    img_player_healthy = pygame.image.load("Assets/person_normal.png").convert_alpha()
    img_player_healthy = pygame.transform.scale(img_player_healthy, img_player_size)
    img_player_vaccinated = pygame.image.load("Assets/person_vax.png").convert_alpha()
    img_player_vaccinated = pygame.transform.scale(img_player_vaccinated, img_player_size)
    img_player_infected = pygame.image.load("Assets/person_infect.png").convert_alpha()
    img_player_infected = pygame.transform.scale(img_player_infected, img_player_size)

def get_grid_clicked(GameBoard, pixel_x, pixel_y):
    """
    Get the action that the click represents.
    If the click was on the heal button, returns "heal"
    Else, returns the board coordinates of the click (board_x, board_y) if valid
    Return False otherwise
    """
    # Get the grid (x,y) where the user clicked
    if pixel_x > GameBoard.offset and pixel_y > GameBoard.offset:   # Make sure the click is not to the left or top of the grid
        board_x = int((pixel_x - GameBoard.offset) / GameBoard.cell_size)
        board_y = int((pixel_y - GameBoard.offset) / GameBoard.cell_size)
        # Return the grid position if it is a valid position on the board
        if (board_x >= 0 and board_x < GameBoard.columns and board_y >= 0 and board_y < GameBoard.rows):
            return (board_x, board_y)
    return False

def get_possible_moves(GameBoard, player_coor, include_vaccinate):
    """
    Return a list of all possible moves that the player is allowed to take from the current position.
    Check if the move direction is in bounds
    If so, check if the space is empty.
    If the space is empty, then add the ["move",direction] to the list.
    If include_vaccinate is True, then also check if vaccination is an option. If the space is not empty AND the person is not vaccinated, then add the ["vaccinate",direction] to the list.
    """
    possible_moves = []
    if player_coor[0] > 0:
        if GameBoard.state[GameBoard.toIndex([player_coor[0] - 1, player_coor[1]])] == None:
            possible_moves.append(["move","left"])
        elif include_vaccinate:
            if not GameBoard.state[GameBoard.toIndex([player_coor[0] - 1, player_coor[1]])].isVaccinated:
                possible_moves.append(["vaccinate","left"])
    if player_coor[0] < (GameBoard.columns - 1):
        if GameBoard.state[GameBoard.toIndex([player_coor[0] + 1, player_coor[1]])] == None:
            possible_moves.append(["move","right"])
        elif include_vaccinate:
            if not GameBoard.state[GameBoard.toIndex([player_coor[0] + 1, player_coor[1]])].isVaccinated:
                possible_moves.append(["vaccinate","right"])
    if player_coor[1] > 0:
        if GameBoard.state[GameBoard.toIndex([player_coor[0], player_coor[1] - 1])] == None:
            possible_moves.append(["move","up"])
        elif include_vaccinate:
            if not GameBoard.state[GameBoard.toIndex([player_coor[0], player_coor[1] - 1])].isVaccinated:
                possible_moves.append(["vaccinate","up"])
    if player_coor[1] < (GameBoard.rows - 1):
        if GameBoard.state[GameBoard.toIndex([player_coor[0], player_coor[1] + 1])] == None:
            possible_moves.append(["move","down"])
        elif include_vaccinate:
            if not GameBoard.state[GameBoard.toIndex([player_coor[0], player_coor[1] + 1])].isVaccinated:
                possible_moves.append(["vaccinate","down"])
    return possible_moves

def run(GameBoard):
    """
    Draw the screen and return any events.
    """
    screen.fill(BACKGROUND)
    build_grid(GameBoard) # Draw the grid
    display_people(GameBoard)
    display_stats(GameBoard)
    
def build_grid(GameBoard):
    """
    Draw the grid on the screen.
    """
    grid_width = GameBoard.columns * GameBoard.cell_size
    grid_height = GameBoard.rows * GameBoard.cell_size
    pygame.draw.rect(screen, BLACK, [GameBoard.offset - LINE_WIDTH, GameBoard.offset - LINE_WIDTH, LINE_WIDTH, grid_height + (2 * LINE_WIDTH)])  # left
    pygame.draw.rect(screen, BLACK, [GameBoard.offset + grid_width, GameBoard.offset - LINE_WIDTH, LINE_WIDTH, grid_height + (2 * LINE_WIDTH)])  # right
    pygame.draw.rect(screen, BLACK, [GameBoard.offset - LINE_WIDTH, GameBoard.offset + grid_height, grid_width + (2 * LINE_WIDTH), LINE_WIDTH])  # bottom
    pygame.draw.rect(screen, BLACK, [GameBoard.offset - LINE_WIDTH, GameBoard.offset - LINE_WIDTH, grid_width + (2 * LINE_WIDTH), LINE_WIDTH])   # top
    pygame.draw.rect(screen, CELL_COLOR, [GameBoard.offset, GameBoard.offset, grid_width, grid_height]) # Fill the inside wioth the cell color
    # Draw the vertical lines
    i = GameBoard.offset + GameBoard.cell_size
    while i < GameBoard.offset + grid_width:
        pygame.draw.rect(screen, BLACK, [i, GameBoard.offset, LINE_WIDTH, grid_height])
        i += GameBoard.cell_size
    # Draw the horizontal lines
    i = GameBoard.offset + GameBoard.cell_size
    while i < GameBoard.offset + grid_height:
        pygame.draw.rect(screen, BLACK, [GameBoard.offset, i, grid_width, LINE_WIDTH])
        i += GameBoard.cell_size

def display_people(GameBoard):
    """
    Draw the people on the screen.
    """
    for person in GameBoard.people:
        if person != None:
            coords = (
                GameBoard.toCoord(person.location)[0] * GameBoard.cell_size + GameBoard.offset + 0.3 * GameBoard.cell_size,
                GameBoard.toCoord(person.location)[1] * GameBoard.cell_size + GameBoard.offset + 0.1 * GameBoard.cell_size
            )
            if person.isGovt:
                screen.blit(img_player_govt, coords)
            elif person.condition == "Healthy":
                screen.blit(img_player_healthy, coords)
            elif person.condition == "Cured":
                screen.blit(img_player_vaccinated, coords)
            else: # only infected people right now
                screen.blit(img_player_infected, coords)

def simulate(GameBoard):
    """
    Allow all the non-government people in the simulation to take a turn.
    """
    for person in GameBoard.people:
        if person != None:
            if not person.isGovt:
                # Get the person's location
                player_loc = GameBoard.toCoord(person.location)
                
                # If the person is infected, then potentially infect any adjact people
                if person.isInfected:
                    uninfected_index = GameBoard.adjacent_noninfected_index(player_loc)
                    for uninfected_person in uninfected_index:
                        if rd.randint(0,100) < person.infectiousAmount:
                            GameBoard.state[uninfected_person].infect_person()
                
                # Choose a possible move and perform it
                possible_moves = get_possible_moves(GameBoard, player_loc, False)
                if len(possible_moves) > 0:
                    this_move = rd.choice(possible_moves)
                    if this_move[0] == "move":
                        GameBoard.move(this_move[1], player_loc, False)

def progress_infection(GameBoard, days_to_death):
    """
    Progress infection counts on infected people.
    Some people will die as infection continues.
    """
    for person in GameBoard.people:
        if person != None:
            if person.isInfected:
                person.daysInfected += 1
                chance = int( (rd.randint(0,100) * (1 - (person.daysInfected / days_to_death))) )
                if chance < 1:
                    GameBoard.death(person.location, person.index)
    
def display_stats(GameBoard):
    screen.blit(font.render("Initial population:", True, WHITE), (800, 400))
    screen.blit(font.render(f"{GameBoard.population_initial}", True, WHITE), (1000, 400))
    screen.blit(font.render("Current population:", True, WHITE), (800, 425))
    screen.blit(font.render(f"{GameBoard.population}", True, WHITE), (1000, 425))
    screen.blit(font.render("Total infected:", True, WHITE), (800, 450))
    screen.blit(font.render(f"{GameBoard.num_infected()}", True, WHITE), (1000, 450))
    screen.blit(font.render("Total vaccinated:", True, WHITE), (800, 475))
    screen.blit(font.render(f"{GameBoard.num_vaccinated()}", True, WHITE), (1000, 475))

def display_finish_screen():
    screen.blit(font.render("SIMULATION OVER.", True, WHITE), (800, 300))
    pygame.display.update()