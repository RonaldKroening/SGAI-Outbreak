from typing import Tuple
import pygame

from Board import Board

# constants
BACKGROUND = "#DDC2A1"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CELL_COLOR = (233, 222, 188)
LINE_WIDTH = 5
IMAGE_ASSETS = [
    "person_normal.png",
    "person_vax.png",
    "person_zombie.png",
]
GAME_WINDOW_DIMENSIONS = (1200, 800)
RESET_MOVE_COORDS = (800, 600)
RESET_MOVE_DIMS = (200, 50)

# Initialize pygame
screen = pygame.display.set_mode(GAME_WINDOW_DIMENSIONS)
pygame.display.set_caption("Outbreak!")
pygame.font.init()
font = pygame.font.SysFont("Impact", 30)
pygame.display.set_caption("Outbreak!")
screen.fill(BACKGROUND)


def get_action(GameBoard: Board, pixel_x: int, pixel_y: int):
    """
    Get the action that the click represents.
    If the click was on the heal button, returns "heal"
    Else, returns the board coordinates of the click (board_x, board_y) if valid
    Return None otherwise
    """
    # Check if the user clicked on the "heal" icon, return "heal" if so
    heal_check = pixel_x >= 900 and pixel_x <= 1100 and pixel_y > 199 and pixel_y < 301
    reset_move_check = (
        pixel_x >= RESET_MOVE_COORDS[0]
        and pixel_x <= RESET_MOVE_COORDS[0] + RESET_MOVE_DIMS[0]
        and pixel_y >= RESET_MOVE_COORDS[1]
        and pixel_y <= RESET_MOVE_COORDS[1] + RESET_MOVE_DIMS[1]
    )
    board_x = int((pixel_x - 150) / 100)
    board_y = int((pixel_y - 150) / 100)
    move_check = (
        board_x >= 0
        and board_x < GameBoard.columns
        and board_y >= 0
        and board_y < GameBoard.rows
    )
    board_coords = (int((pixel_x - 150) / 100), int((pixel_y - 150) / 100))

    if heal_check:
        return "heal"
    elif reset_move_check:
        return "reset move"
    elif move_check:
        return board_coords
    return None


def run(GameBoard: Board):
    """
    Draw the screen and return any events.
    """
    screen.fill(BACKGROUND)
    build_grid(GameBoard)  # Draw the grid
    # Draw the heal icon
    display_image(
        screen, "Assets/cure.jpeg", GameBoard.display_cell_dimensions, (950, 200)
    )
    display_people(GameBoard)
    display_reset_move_button()
    return pygame.event.get()


def display_reset_move_button():
    rect = pygame.Rect(
        RESET_MOVE_COORDS[0],
        RESET_MOVE_COORDS[1],
        RESET_MOVE_DIMS[0],
        RESET_MOVE_DIMS[1],
    )
    pygame.draw.rect(screen, BLACK, rect)
    screen.blit(font.render("Reset move?", True, WHITE), RESET_MOVE_COORDS)


def display_image(
    screen: pygame.Surface,
    itemStr: str,
    dimensions: Tuple[int, int],
    position: Tuple[int, int],
):
    """
    Draw an image on the screen at the indicated position.
    """
    v = pygame.image.load(itemStr).convert_alpha()
    v = pygame.transform.scale(v, dimensions)
    screen.blit(v, position)


def build_grid(GameBoard: Board):
    """
    Draw the grid on the screen.
    """
    grid_width = GameBoard.columns * GameBoard.display_cell_dimensions[0]
    grid_height = GameBoard.rows * GameBoard.display_cell_dimensions[1]
    # left
    pygame.draw.rect(
        screen,
        BLACK,
        [
            GameBoard.display_border - LINE_WIDTH,
            GameBoard.display_border - LINE_WIDTH,
            LINE_WIDTH,
            grid_height + (2 * LINE_WIDTH),
        ],
    )
    # right
    pygame.draw.rect(
        screen,
        BLACK,
        [
            GameBoard.display_border + grid_width,
            GameBoard.display_border - LINE_WIDTH,
            LINE_WIDTH,
            grid_height + (2 * LINE_WIDTH),
        ],
    )
    # bottom
    pygame.draw.rect(
        screen,
        BLACK,
        [
            GameBoard.display_border - LINE_WIDTH,
            GameBoard.display_border + grid_height,
            grid_width + (2 * LINE_WIDTH),
            LINE_WIDTH,
        ],
    )
    # top
    pygame.draw.rect(
        screen,
        BLACK,
        [
            GameBoard.display_border - LINE_WIDTH,
            GameBoard.display_border - LINE_WIDTH,
            grid_width + (2 * LINE_WIDTH),
            LINE_WIDTH,
        ],
    )
    # Fill the inside wioth the cell color
    pygame.draw.rect(
        screen,
        CELL_COLOR,
        [GameBoard.display_border, GameBoard.display_border, grid_width, grid_height],
    )

    # Draw the vertical lines
    i = GameBoard.display_border + GameBoard.display_cell_dimensions[0]
    while i < GameBoard.display_border + grid_width:
        pygame.draw.rect(
            screen, BLACK, [i, GameBoard.display_border, LINE_WIDTH, grid_height]
        )
        i += GameBoard.display_cell_dimensions[0]
    # Draw the horizontal lines
    i = GameBoard.display_border + GameBoard.display_cell_dimensions[1]
    while i < GameBoard.display_border + grid_height:
        pygame.draw.rect(
            screen, BLACK, [GameBoard.display_border, i, grid_width, LINE_WIDTH]
        )
        i += GameBoard.display_cell_dimensions[1]


def display_people(GameBoard: Board):
    """
    Draw the people (government, vaccinated, and zombies) on the grid.
    """
    for x in range(len(GameBoard.States)):
        if GameBoard.States[x].person != None:
            p = GameBoard.States[x].person
            char = "Assets/" + IMAGE_ASSETS[0]
            if p.isVaccinated:
                char = "Assets/" + IMAGE_ASSETS[1]
            elif p.isZombie:
                char = "Assets/" + IMAGE_ASSETS[2]
            coords = (
                int(x % GameBoard.rows) * GameBoard.display_cell_dimensions[0]
                + GameBoard.display_border
                + 35,
                int(x / GameBoard.columns) * GameBoard.display_cell_dimensions[1]
                + GameBoard.display_border
                + 20,
            )
            display_image(screen, char, (35, 60), coords)


def display_win_screen():
    screen.fill(BACKGROUND)
    screen.blit(
        font.render("You win!", True, WHITE),
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
        font.render("You lose!", True, WHITE),
        (500, 400),
    )
    pygame.display.update()

    # catch quit event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


def direction(coord1: Tuple[int, int], coord2: Tuple[int, int]):
    if coord2[1] > coord1[1]:
        return "moveDown"
    elif coord2[1] < coord1[1]:
        return "moveUp"
    elif coord2[0] > coord1[0]:
        return "moveRight"
    elif coord2[0] < coord1[0]:
        return "moveLeft"
