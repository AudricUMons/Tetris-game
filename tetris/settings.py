# Constantes générales
TILE_SIZE = 30
COLS, ROWS = 10, 20
MARGIN = 10
WIDTH = COLS * TILE_SIZE + 2 * MARGIN
HEIGHT = ROWS * TILE_SIZE + 2 * MARGIN
FPS = 60

# Pièces (forme et couleur)
TETROMINOS = [
    {"shape": [(-1, 0), (0, 0), (1, 0), (2, 0)], "color": (0, 255, 255)},
    {"shape": [(0, 0), (1, 0), (0, 1), (1, 1)], "color": (255, 255, 0)},
    {"shape": [(-1, 0), (0, 0), (1, 0), (0, 1)], "color": (160, 32, 240)},
    {"shape": [(-1, 0), (0, 0), (1, 0), (1, 1)], "color": (255, 165, 0)},
    {"shape": [(-1, 0), (0, 0), (1, 0), (-1, 1)], "color": (0, 0, 255)},
    {"shape": [(0, 0), (1, 0), (-1, 1), (0, 1)], "color": (0, 255, 0)},
    {"shape": [(-1, 0), (0, 0), (0, 1), (1, 1)], "color": (255, 0, 0)}
]
