# main.py
import pygame
from tetris.settings import WIDTH, HEIGHT, TILE_SIZE, COLS, ROWS, MARGIN
from tetris.core import Tetris
from tetris.assets import load_sounds

def handle_input(event, game):
    key = event.key
    if key == pygame.K_LEFT:
        game.try_move(dx=-1)
    elif key == pygame.K_RIGHT:
        game.try_move(dx=1)
    elif key == pygame.K_DOWN:
        game.update()
    elif key == pygame.K_UP:
        game.try_move(rotate=True)
    elif key == pygame.K_SPACE:
        while game.valid(game.get_future_cells(dy=1)):
            game.piece.pos[1] += 1
        game.freeze_and_check_lines()
    elif key == pygame.K_r:
        game.restart()

pygame.init()
screen = pygame.display.set_mode((WIDTH + 150, HEIGHT))
pygame.display.set_caption("Tetris Python (Pygame)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
sounds = load_sounds()
game = Tetris(sounds)

fall_event = pygame.USEREVENT + 1
pygame.time.set_timer(fall_event, 500)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            handle_input(event, game)
        elif event.type == fall_event:
            game.update()

    game.apply_flash()
    game.draw(screen, font)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
