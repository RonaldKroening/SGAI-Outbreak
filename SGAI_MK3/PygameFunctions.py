import pygame
<<<<<<< Updated upstream

BACKGROUND = "#DDC2A1"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CELL_COLOR = (233, 222, 188)
LINE_WIDTH = 5
cell_dimensions = [100,100]
grid_start = [150,150]

image_assets = [
    "person_normal.png",
    "person_vax.png",
    "person_zombie.png",
]

=======
from constants import *
from Board import Board
import os
>>>>>>> Stashed changes

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
    heal_check = pixel_x >= 900 and pixel_x <= 1100 and pixel_y > 199 and pixel_y < 301
    if heal_check:
        return "heal"
    else:
        # Get the grid (x,y) where the user clicked
        if pixel_x > GameBoard.display_border and pixel_y > GameBoard.display_border:   # Clicking to the top or left of the border will result in a grid value of 0, which is valid
            board_x = int((pixel_x - GameBoard.display_border) / GameBoard.display_cell_dimensions[0])
            board_y = int((pixel_y - GameBoard.display_border) / GameBoard.display_cell_dimensions[1])
            # Return the grid position if it is a valid position on the board
            if (board_x >= 0 and board_x < GameBoard.columns and board_y >= 0 and board_y < GameBoard.rows):
                return (board_x, board_y)
    return None

def run(GameBoard):
    """
    Draw the screen and return any events.
    """
    screen.fill(BACKGROUND)
<<<<<<< Updated upstream
    build_grid(GameBoard) # Draw the grid
    display_image(screen, "Assets/cure.jpeg", GameBoard.display_cell_dimensions, (950, 200)) # Draw the heal icon
=======
    build_grid(GameBoard)  # Draw the grid
    # Draw the heal icon
    if GameBoard.player_role == "Government":
        display_image(screen, "SGAI_MK3/Assets/cure.jpeg", CURE_BITE_DIMS, CURE_BITE_COORDS)
    else:
        display_image(screen, "SGAI_MK3/Assets/bite.png", CURE_BITE_DIMS, CURE_BITE_COORDS)
>>>>>>> Stashed changes
    display_people(GameBoard)
    return pygame.event.get()

def display_image(screen, itemStr, dimensions, position):
    """
    Draw an image on the screen of size dimensions at the indicated position.
    """

    v = pygame.image.load(itemStr).convert_alpha()
    v = pygame.transform.scale(v, dimensions)
    screen.blit(v, position)

def build_grid(GameBoard):
    """
    Draw the grid on the screen.
    """
    grid_width = GameBoard.columns * GameBoard.display_cell_dimensions[0]
    grid_height = GameBoard.rows * GameBoard.display_cell_dimensions[1]
    pygame.draw.rect(screen, BLACK, [GameBoard.display_border - LINE_WIDTH, GameBoard.display_border - LINE_WIDTH, LINE_WIDTH, grid_height + (2 * LINE_WIDTH)])  # left
    pygame.draw.rect(screen, BLACK, [GameBoard.display_border + grid_width, GameBoard.display_border - LINE_WIDTH, LINE_WIDTH, grid_height + (2 * LINE_WIDTH)])  # right
    pygame.draw.rect(screen, BLACK, [GameBoard.display_border - LINE_WIDTH, GameBoard.display_border + grid_height, grid_width + (2 * LINE_WIDTH), LINE_WIDTH])  # bottom
    pygame.draw.rect(screen, BLACK, [GameBoard.display_border - LINE_WIDTH, GameBoard.display_border - LINE_WIDTH, grid_width + (2 * LINE_WIDTH), LINE_WIDTH])   # top
    pygame.draw.rect(screen, CELL_COLOR, [GameBoard.display_border, GameBoard.display_border, grid_width, grid_height]) # Fill the inside wioth the cell color
    # Draw the vertical lines
    i = GameBoard.display_border + GameBoard.display_cell_dimensions[0]
    while i < GameBoard.display_border + grid_width:
        pygame.draw.rect(screen, BLACK, [i, GameBoard.display_border, LINE_WIDTH, grid_height])
        i += GameBoard.display_cell_dimensions[0]
    # Draw the horizontal lines
    i = GameBoard.display_border + GameBoard.display_cell_dimensions[1]
    while i < GameBoard.display_border + grid_height:
        pygame.draw.rect(screen, BLACK, [GameBoard.display_border, i, grid_width, LINE_WIDTH])
        i += GameBoard.display_cell_dimensions[1]

def display_people(GameBoard):
    """
    Draw the people (government, vaccinated, and zombies) on the grid.
    """
    for x in range(len(GameBoard.States)):
        if GameBoard.States[x].person != None:
            p = GameBoard.States[x].person
<<<<<<< Updated upstream
            char = "Assets/" + image_assets[0]
            if p.isVaccinated:
                char = "Assets/" + image_assets[1]
            elif p.isZombie:
                char = "Assets/" + image_assets[2]
=======
            char = "SGAI_MK3/Assets/" + IMAGE_ASSETS[0]
            if p.isVaccinated:
                char = "SGAI_MK3/Assets/" + IMAGE_ASSETS[1]
            elif p.isZombie:
                char = "SGAI_MK3/Assets/" + IMAGE_ASSETS[2]
>>>>>>> Stashed changes
            coords = (
                int(x % GameBoard.rows) * GameBoard.display_cell_dimensions[0] + GameBoard.display_border + 35,
                int(x / GameBoard.columns) * GameBoard.display_cell_dimensions[1] + GameBoard.display_border + 20,
            )
            display_image(screen, char, (35, 60), coords)


def run(GameBoard):
    screen.fill(BACKGROUND)
    build_grid(screen, 5, 100, 150)
    display_image(screen, "Assets/cure.jpeg", cell_dimensions, (950, 200))
    # pygame.display.flip()
    display_people(GameBoard)
    display_board(screen,GameBoard)
    
    return pygame.event.get()


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


def display_image(screen, itemStr, dimensions, position):
    v = pygame.image.load(itemStr).convert_alpha()
    v = pygame.transform.scale(v, dimensions)
    screen.blit(v, position)


def build_grid(screen, margin, cell_side, start):
    grid_width = 600
    grid_height = 600
    pygame.draw.rect(screen, BLACK, [start - 5, start - 5, 5, grid_height + 10])  # left
    pygame.draw.rect(
        screen, BLACK, [start + grid_width, start - 5, 5, grid_height + 10]
    )  # right
    pygame.draw.rect(
        screen, BLACK, [start - 5, start + grid_height, grid_width + 10, 5]
    )  # bottom
    pygame.draw.rect(screen, BLACK, [start - 5, start - 5, grid_width + 10, 5])  # top
    pygame.draw.rect(screen, CELL_COLOR, [start, start, grid_width, grid_height])
    i = start + cell_side
    while i < start + grid_width:
        pygame.draw.rect(screen, BLACK, [i, start, 5, grid_height])
        i += cell_side
    i = start + cell_side
    while i < start + grid_height:
        pygame.draw.rect(screen, BLACK, [start, i, grid_width, 5])
        i += cell_side


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

    '''
    Remove lines 185-191. This is not needed bc program will loop. Unless changing to new screen, which is not needed.
    '''
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
    elif coord1[0] == coord2[0] and coord2[1] == coord1[1]:
        return "same"
