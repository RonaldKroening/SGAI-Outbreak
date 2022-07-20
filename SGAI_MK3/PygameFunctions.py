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
my_font = pygame.font.SysFont("Impact", 30)
game_window_dimensions = (1400, 800)
person_dimensions = (20, 60)
pygame.display.set_caption("Outbreak!")
# screen = pygame.display.set_mode(game_window_dimensions)
screen.fill(BACKGROUND)


def get_action(B, pixel_x, pixel_y):
    """
    Get the action that the click represents.
    If the click was on the heal button, returns "heal"
    Else, returns the board coordinates of the click (board_x, board_y)
    """

    heal_check = pixel_x >= 900 and pixel_x <= 1100 and pixel_y > 199 and pixel_y < 301
    board_coords = (int((pixel_x - grid_start[0]) / cell_dimensions[0]),
                    int((pixel_y - grid_start[1]) / cell_dimensions[1]))
        
    if heal_check:
        return "heal"
    elif B.rows > board_coords[0] > -1 and -1 < board_coords[1] < B.columns:
        return board_coords


def display_people(PersonList, board_dimensions):
    for Person in PersonList:
        if Person.id == "Human":
            char = "Assets/" + image_assets[0]
        elif Person.id == "Cured":
            char = "Assets/" + image_assets[1]
        else: # only zombies right now
            char = "Assets/" + image_assets[2]
        coords = (
            int(Person.location % board_dimensions[0]) * cell_dimensions[0] + grid_start[0] + 25,
            int(Person.location / board_dimensions[0]) * cell_dimensions[1] + grid_start[1] + 20,
            )
        display_image(screen, char, (35, 60), coords)


def run(GameBoard, bd):
    screen.fill(BACKGROUND)
    build_grid(screen, 5, 100, 150)
    display_image(screen, "Assets/cure.jpeg", cell_dimensions, (950, 200))
    # pygame.display.flip()
    display_people(GameBoard.People, bd)
    pass


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
