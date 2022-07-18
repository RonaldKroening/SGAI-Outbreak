import pygame

image_assets = [
    "person_normal.png",
    "person_vax.png",
    "person_zombie.png",
]
grid_start = (150, 150)
cell_dimensions = (100, 100)
BACKGROUND = "#DDC2A1"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CELL_COLOR = (233, 222, 188)
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Outbreak!")
pygame.font.init()
font = pygame.font.SysFont("Impact", 30)
cell_dimensions = (100, 100)
game_window_dimensions = (1400, 800)
person_dimensions = (20, 60)
grid_start = (150, 150)
pygame.display.set_caption("Outbreak!")
# screen = pygame.display.set_mode(game_window_dimensions)
screen.fill("#DDC2A1")

RESET_MOVE_COORDS = (800, 600)
RESET_MOVE_DIMS = (200, 50)


def get_action(B, pixel_x, pixel_y):
    """
    Get the action that the click represents.
    If the click was on the heal button, returns "heal"
    Else, returns the board coordinates of the click (board_x, board_y)
    """
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
        board_x >= 0 and board_x < B.columns and board_y >= 0 and board_y < B.rows
    )
    board_coords = (int((pixel_x - 150) / 100), int((pixel_y - 150) / 100))

    if heal_check:
        return "heal"
    elif reset_move_check:
        return "reset move"
    elif move_check:
        return board_coords
    return None


def display_people(StateList, board_dimensions):
    for x in range(len(StateList)):
        if StateList[x].person != None:
            p = StateList[x].person
            char = "Assets/" + image_assets[0]
            if p.isVaccinated:
                char = "Assets/" + image_assets[1]
            elif p.isZombie:
                char = "Assets/" + image_assets[2]
            coords = (
                int(x % board_dimensions[0]) * 100 + 185,
                int(x / board_dimensions[1]) * 100 + 170,
            )
            display_image(screen, char, (35, 60), coords)


def run(GameBoard, bd):
    screen.fill(BACKGROUND)
    build_grid(screen, 5, 100, 150)
    display_image(screen, "Assets/cure.jpeg", cell_dimensions, (950, 200))
    # pygame.display.flip()
    display_people(GameBoard.States, bd)
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
        font.render("You lose lol!", True, WHITE),
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
