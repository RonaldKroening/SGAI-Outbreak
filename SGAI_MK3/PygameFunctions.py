import pygame

BACKGROUND = "#DDC2A1"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CELL_COLOR = (233, 222, 188)
LINE_WIDTH = 1
IMAGE_ASSETS = [
    "person_normal.png",
    "person_vax.png",
    "person_infect.png",
]

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Outbreak!")
pygame.font.init()
screen.fill(BACKGROUND)

# Load images
img_player_govt = None
img_player_healthy = None
img_player_vaccinated = None
img_player_infected = None
img_vaccinate_icon = None

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
    global img_vaccinate_icon
    img_player_size = (0.8 * GameBoard.cell_size / 2, 0.8 * GameBoard.cell_size)
    img_player_govt = pygame.image.load("Assets/person_govt.png").convert_alpha()
    img_player_govt = pygame.transform.scale(img_player_govt, img_player_size)
    img_player_healthy = pygame.image.load("Assets/person_normal.png").convert_alpha()
    img_player_healthy = pygame.transform.scale(img_player_healthy, img_player_size)
    img_player_vaccinated = pygame.image.load("Assets/person_vax.png").convert_alpha()
    img_player_vaccinated = pygame.transform.scale(img_player_vaccinated, img_player_size)
    img_player_infected = pygame.image.load("Assets/person_infect.png").convert_alpha()
    img_player_infected = pygame.transform.scale(img_player_infected, img_player_size)
    img_vaccinate_icon = pygame.image.load("Assets/cure.jpeg").convert_alpha()
    img_vaccinate_icon = pygame.transform.scale(img_vaccinate_icon, (100,100))

def get_action(GameBoard, pixel_x, pixel_y):
    """
    Get the action that the click represents.
    If the click was on the heal button, returns "heal"
    Else, returns the board coordinates of the click (board_x, board_y) if valid
    Return None otherwise
    """
    # Check if the user clicked on the "heal" icon, return "heal" if so
    heal_check = pixel_x >= 900 and pixel_x <= 1100 and pixel_y > 199 and pixel_y < 301
    if heal_check:
        return "heal"
    else:
        # Get the grid (x,y) where the user clicked
        if pixel_x > GameBoard.offset and pixel_y > GameBoard.offset:   # Clicking to the top or left of the border will result in a grid value of 0, which is valid
            board_x = int((pixel_x - GameBoard.offset) / GameBoard.cell_size)
            board_y = int((pixel_y - GameBoard.offset) / GameBoard.cell_size)
            # Return the grid position if it is a valid position on the board
            if (board_x >= 0 and board_x < GameBoard.columns and board_y >= 0 and board_y < GameBoard.rows):
                return (board_x, board_y)
    return None

def run(GameBoard):
    """
    Draw the screen and return any events.
    """
    screen.fill(BACKGROUND)
    build_grid(GameBoard) # Draw the grid
    screen.blit(img_vaccinate_icon, (950, 200))
    display_people(GameBoard)
    
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
        coords = (
            int(person.location % GameBoard.rows) * GameBoard.cell_size + GameBoard.offset + 0.3 * GameBoard.cell_size,
            int(person.location / GameBoard.columns) * GameBoard.cell_size + GameBoard.offset + 0.1 * GameBoard.cell_size,
        )
        if person.isGovt:
            screen.blit(img_player_govt, coords)
        elif person.condition == "Healthy":
            screen.blit(img_player_healthy, coords)
        elif person.condition == "Cured":
            screen.blit(img_player_vaccinated, coords)
        else: # only infected people right now
            screen.blit(img_player_infected, coords)

def display_current_action(take_action):
    font = pygame.font.SysFont("Comic Sans", 20)
    screen.blit(
        font.render("Your move is currently:", True, WHITE),
        (800, 400),
    )
    screen.blit(font.render(f"{take_action}", True, WHITE), (800, 430))

def display_win_screen():
    screen.fill(BACKGROUND)
    screen.blit(
        pygame.font.SysFont("Comic Sans", 32).render("You win!", True, WHITE),
        (500, 400),
    )
    pygame.display.update()

    # catch quit event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

def display_lose_screen():
    screen.fill(BACKGROUND)
    screen.blit(
        pygame.font.SysFont("Comic Sans", 32).render("You lose lol!", True, WHITE),
        (500, 500),
    )
    pygame.display.update()

    # catch quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return

def direction(coord1, coord2):
    if coord2[1] > coord1[1]:
        return "moveDown"
    elif coord2[1] < coord1[1]:
        return "moveUp"
    elif coord2[0] > coord1[0]:
        return "moveRight"
    elif coord2[0] < coord1[0]:
        return "moveLeft"