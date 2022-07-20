from typing import List, Tuple
import pygame
from constants import *
from Board import Board


# Initialize pygame
screen = pygame.display.set_mode(GAME_WINDOW_DIMENSIONS)
pygame.display.set_caption("Outbreak!")
pygame.font.init()
font = pygame.font.SysFont("Comic Sans", 20)
screen.fill(BACKGROUND)


def get_action(GameBoard: Board, pixel_x: int, pixel_y: int):
    """
    Get the action that the click represents.
    If the click was on the heal button, returns "heal"
    Else, returns the board coordinates of the click (board_x, board_y) if valid
    Return None otherwise
    """
    # Check if the user clicked on the "heal" or "bite" icon, return "heal" or "bite" if so
    heal_bite_check = (
        pixel_x >= CURE_BITE_COORDS[0]
        and pixel_x <= CURE_BITE_COORDS[0] + CURE_BITE_DIMS[0]
        and pixel_y >= CURE_BITE_COORDS[1]
        and pixel_y <= CURE_BITE_COORDS[1] + CURE_BITE_DIMS[1]
    )
    reset_move_check = (
        pixel_x >= RESET_MOVE_COORDS[0]
        and pixel_x <= RESET_MOVE_COORDS[0] + RESET_MOVE_DIMS[0]
        and pixel_y >= RESET_MOVE_COORDS[1]
        and pixel_y <= RESET_MOVE_COORDS[1] + RESET_MOVE_DIMS[1]
    )
    board_x = int((pixel_x - MARGIN) / CELL_DIMENSIONS[0])
    board_y = int((pixel_y - MARGIN) / CELL_DIMENSIONS[1])
    move_check = (
        board_x >= 0
        and board_x < GameBoard.columns
        and board_y >= 0
        and board_y < GameBoard.rows
    )

    if heal_bite_check:
        if GameBoard.player_role == "Government":
            return "heal"
        return "bite"
    elif reset_move_check:
        return "reset move"
    elif move_check:
        return board_x, board_y
    return None


def run(GameBoard: Board):
    """
    Draw the screen and return any events.
    """
    screen.fill(BACKGROUND)
    build_grid(GameBoard)  # Draw the grid
    # Draw the heal icon
    if GameBoard.player_role == "Government":
        display_image(screen, "Assets/cure.jpeg", CURE_BITE_DIMS, CURE_BITE_COORDS)
    else:
        display_image(screen, "Assets/bite.png", CURE_BITE_DIMS, CURE_BITE_COORDS)
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
    grid_width = GameBoard.columns * CELL_DIMENSIONS[0]
    grid_height = GameBoard.rows * CELL_DIMENSIONS[1]
    # left
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN - LINE_WIDTH,
            MARGIN - LINE_WIDTH,
            LINE_WIDTH,
            grid_height + (2 * LINE_WIDTH),
        ],
    )
    # right
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN + grid_width,
            MARGIN - LINE_WIDTH,
            LINE_WIDTH,
            grid_height + (2 * LINE_WIDTH),
        ],
    )
    # bottom
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN - LINE_WIDTH,
            MARGIN + grid_height,
            grid_width + (2 * LINE_WIDTH),
            LINE_WIDTH,
        ],
    )
    # top
    pygame.draw.rect(
        screen,
        BLACK,
        [
            MARGIN - LINE_WIDTH,
            MARGIN - LINE_WIDTH,
            grid_width + (2 * LINE_WIDTH),
            LINE_WIDTH,
        ],
    )
    # Fill the inside wioth the cell color
    pygame.draw.rect(
        screen,
        CELL_COLOR,
        [MARGIN, MARGIN, grid_width, grid_height],
    )

    # Draw the vertical lines
    i = MARGIN + CELL_DIMENSIONS[0]
    while i < MARGIN + grid_width:
        pygame.draw.rect(screen, BLACK, [i, MARGIN, LINE_WIDTH, grid_height])
        i += CELL_DIMENSIONS[0]
    # Draw the horizontal lines
    i = MARGIN + CELL_DIMENSIONS[1]
    while i < MARGIN + grid_height:
        pygame.draw.rect(screen, BLACK, [MARGIN, i, grid_width, LINE_WIDTH])
        i += CELL_DIMENSIONS[1]


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
                int(x % GameBoard.rows) * CELL_DIMENSIONS[0] + MARGIN + 35,
                int(x / GameBoard.columns) * CELL_DIMENSIONS[1] + MARGIN + 20,
            )
            display_image(screen, char, (35, 60), coords)


def display_cur_move(cur_move: List):
    # Display the current action
    screen.blit(
        font.render("Your move is currently:", True, WHITE),
        CUR_MOVE_COORDS,
    )
    screen.blit(
        font.render(f"{cur_move}", True, WHITE),
        (
            CUR_MOVE_COORDS[0],
            CUR_MOVE_COORDS[1] + font.size("Your move is currently:")[1] * 2,
        ),
    )


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
