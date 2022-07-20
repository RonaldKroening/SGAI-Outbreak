import pygame

BACKGROUND = "#DDC2A1"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CELL_COLOR = (233, 222, 188)
LINE_WIDTH = 5

image_assets = [
    "person_normal.png",
    "person_vax.png",
    "person_zombie.png",
]

# Initialize pygame
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Outbreak!")
pygame.font.init()
my_font = pygame.font.SysFont("Impact", 30)
game_window_dimensions = (1400, 800)
person_dimensions = (20, 60)
pygame.display.set_caption("Outbreak!")
screen.fill(BACKGROUND)

def get_action(GameBoard, pixel_x, pixel_y):
    """
    Get the action that the click represents.
    If the click was on the heal button, returns "heal"
    Else, returns the board coordinates of the click (board_x, board_y) if valid
    Return None otherwise
    """
    # Check if the user clicked on the "heal" icon, return "heal" if so
    if heal_check:
        return "heal"
    else:
        # Get the grid (x,y) where the user clicked
        if pixel_x > GameBoard.offset and pixel_y > GameBoard.offset:   # Clicking to the top or left of the border will result in a grid value of 0, which is valid
            board_x = int((pixel_x - GameBoard.offset) / GameBoard.cellsize)
            board_y = int((pixel_y - GameBoard.offset) / GameBoard.cellsize)
            # Return the grid position if it is a valid position on the board
            if (board_x >= 0 and board_x < GameBoard.columns and board_y >= 0 and board_y < GameBoard.rows):
                return (board_x, board_y)
    return None

def run(GameBoard, bd):
    """
    Draw the screen and return any events.
    """
    screen.fill(BACKGROUND)
    build_grid(GameBoard) # Draw the grid
    display_image(screen, "Assets/cure.jpeg", (GameBoard.cellsize, GameBoard.cellsize), (950, 200)) # Draw the heal icon
    display_people(GameBoard)

def display_image(screen, itemStr, dimensions, position):
    """
    Draw an image on the screen at the indicated position.
    """
    v = pygame.image.load(itemStr).convert_alpha()
    v = pygame.transform.scale(v, dimensions)
    screen.blit(v, position)
    
def build_grid(GameBoard):
    """
    Draw the grid on the screen.
    """
    grid_width = GameBoard.columns * GameBoard.cellsize
    grid_height = GameBoard.rows * GameBoard.cellsize
    pygame.draw.rect(screen, BLACK, [GameBoard.offset - LINE_WIDTH, GameBoard.offset - LINE_WIDTH, LINE_WIDTH, grid_height + (2 * LINE_WIDTH)])  # left
    pygame.draw.rect(screen, BLACK, [GameBoard.offset + grid_width, GameBoard.offset - LINE_WIDTH, LINE_WIDTH, grid_height + (2 * LINE_WIDTH)])  # right
    pygame.draw.rect(screen, BLACK, [GameBoard.offset - LINE_WIDTH, GameBoard.offset + grid_height, grid_width + (2 * LINE_WIDTH), LINE_WIDTH])  # bottom
    pygame.draw.rect(screen, BLACK, [GameBoard.offset - LINE_WIDTH, GameBoard.offset - LINE_WIDTH, grid_width + (2 * LINE_WIDTH), LINE_WIDTH])   # top
    pygame.draw.rect(screen, CELL_COLOR, [GameBoard.offset, GameBoard.offset, grid_width, grid_height]) # Fill the inside wioth the cell color
    # Draw the vertical lines
    i = GameBoard.offset + GameBoard.cellsize
    while i < GameBoard.offset + grid_width:
        pygame.draw.rect(screen, BLACK, [i, GameBoard.offset, LINE_WIDTH, grid_height])
        i += GameBoard.cellsize
    # Draw the horizontal lines
    i = GameBoard.offset + GameBoard.cellsize
    while i < GameBoard.offset + grid_height:
        pygame.draw.rect(screen, BLACK, [GameBoard.offset, i, grid_width, LINE_WIDTH])
        i += GameBoard.cellsize

def display_people(GameBoard):
    for Person in GameBoard.People:
        if Person.id == "Human":
            char = "Assets/" + image_assets[0]
        elif Person.id == "Cured":
            char = "Assets/" + image_assets[1]
        else: # only zombies right now
            char = "Assets/" + image_assets[2]
        coords = (
            int(Person.location % GameBoard.rows) * GameBoard.cellsize + GameBoard.offset + 35,
            int(Person.location / GameBoard.columns) * GameBoard.cellsize + GameBoard.offset + 20,
            )
        display_image(screen, char, (35, 60), coords)

def display_board(screen, Board):
    screen.fill(BACKGROUND)
    dif = cell_dimensions[0] / 3
    ydif = cell_dimensions[1] / 4
    margin = 5
    i = 0
    for State in Board.States:
        person = State.person
        if person is not None:
            icon = "Assets/" + image_assets[0]
            if person.isZombie:
                icon = "Assets/" + image_assets[2]
            elif person.isVaccinated:
                icon = "Assets/" + image_assets[1]
            position = Board.toCoord(i)
            x_start = (
                (position[0] * cell_dimensions[0])
                + grid_start[0]
                + (cell_dimensions[0] / 3)
            )
            y_pos = (
                (position[1] * cell_dimensions[1])
                + grid_start[1]
                + (cell_dimensions[1] / 4)
            )
            display_image(screen, icon, (35, 60), (x_start, y_pos))
        i += 1
    build_grid(screen, 5, cell_dimensions[0], 150)
    pygame.display.update()

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