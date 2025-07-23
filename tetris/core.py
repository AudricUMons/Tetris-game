# tetris/core.py
import random
import pygame
from .settings import COLS, ROWS, TETROMINOS, TILE_SIZE, MARGIN, WIDTH, HEIGHT

class Piece:
    def __init__(self, id):
        self.id = id
        self.shape = list(TETROMINOS[id]["shape"])
        self.color = TETROMINOS[id]["color"]
        self.pos = [COLS // 2, 0]

    def rotate(self):
        self.shape = [(-y, x) for x, y in self.shape]

    def get_cells(self):
        if not hasattr(self, '_cached_pos') or self._cached_pos != tuple(self.pos) or self._cached_shape != tuple(self.shape):
            self._cached_cells = [(self.pos[0] + x, self.pos[1] + y) for x, y in self.shape]
            self._cached_pos = tuple(self.pos)
            self._cached_shape = tuple(self.shape)
        return self._cached_cells

class Tetris:
    def __init__(self, sounds):
        self.sounds = sounds
        self.block_surfaces = [self._create_surface(t["color"]) for t in TETROMINOS]
        self.reset_game()

    def reset_game(self):
        self.next_piece = self._new_piece()
        self.board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
        self.piece = self._new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.flash_rows = []
        self.flash_timer = 0

    def _new_piece(self):
        return Piece(random.randint(0, 6))

    def valid(self, cells):
        for x, y in cells:
            if x < 0 or x >= COLS or y >= ROWS:
                return False
            if y >= 0 and self.board[y][x] != -1:
                return False
        return True

    def freeze(self):
        for x, y in self.piece.get_cells():
            if y >= 0:
                self.board[y][x] = self.piece.id

    def clear_lines(self):
        new_board = []
        cleared = 0
        for row in self.board:
            if all(cell != -1 for cell in row):
                cleared += 1
            else:
                new_board.append(row)
        self.board = [[-1] * COLS for _ in range(cleared)] + new_board
        self.score += cleared * 100
        if cleared:
            self.lines_cleared += cleared
            self.level = 1 + self.lines_cleared // 10
            pygame.time.set_timer(pygame.USEREVENT + 1, max(50, 500 - (self.level - 1) * 25))

    def spawn(self):
        self.piece = self.next_piece
        self.next_piece = self._new_piece()
        if not self.valid(self.piece.get_cells()):
            self.game_over = True
            self.sounds["gameover"].play()

    def update(self):
        if self.game_over or self.flash_rows:
            return
        self.piece.pos[1] += 1
        if not self.valid(self.piece.get_cells()):
            self.piece.pos[1] -= 1
            self.freeze_and_check_lines()

    def apply_flash(self):
        if self.flash_rows:
            if pygame.time.get_ticks() - self.flash_timer > 200:
                self.sounds["clear"].play()
                self.clear_lines()
                self.flash_rows.clear()
                self.spawn()
            elif pygame.time.get_ticks() - self.flash_timer > 100:
                self.flash_state = not self.flash_state

    def get_future_cells(self, dx=0, dy=0, rotate=False):
        shape = [(-y, x) for x, y in self.piece.shape] if rotate else self.piece.shape
        pos = [self.piece.pos[0] + dx, self.piece.pos[1] + dy]
        return [(pos[0] + x, pos[1] + y) for x, y in shape]

    def try_move(self, dx=0, dy=0, rotate=False):
        if self.game_over or self.flash_rows:
            return
        new_shape = [(-y, x) for x, y in self.piece.shape] if rotate else self.piece.shape
        new_pos = [self.piece.pos[0] + dx, self.piece.pos[1] + dy]
        new_cells = self.get_future_cells(dx, dy, rotate)
        if self.valid(new_cells):
            if rotate:
                self.sounds["rotate"].play()
            self.piece.shape = new_shape if rotate else self.piece.shape
            self.piece.pos = new_pos

    def get_ghost_cells(self):
        ghost_y = self.piece.pos[1]
        while True:
            ghost_y += 1
            test_cells = [(self.piece.pos[0] + x, ghost_y + y) for x, y in self.piece.shape]
            if not self.valid(test_cells):
                ghost_y -= 1
                break
        return [(self.piece.pos[0] + x, ghost_y + y) for x, y in self.piece.shape]

    def draw(self, screen, font):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (30, 30, 30), (WIDTH, 0, 150, HEIGHT))
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH, 0, 150, HEIGHT), 2)

        for x in range(COLS + 1):
            pygame.draw.line(screen, (255, 255, 255), (MARGIN + x * TILE_SIZE, MARGIN), (MARGIN + x * TILE_SIZE, HEIGHT - MARGIN))
        for y in range(ROWS + 1):
            pygame.draw.line(screen, (255, 255, 255), (MARGIN, MARGIN + y * TILE_SIZE), (WIDTH - MARGIN, MARGIN + y * TILE_SIZE))

        for y in range(ROWS):
            for x in range(COLS):
                if self.board[y][x] != -1 and (y not in self.flash_rows or self.flash_state):  # flash_rows is now a set
                    pygame.draw.rect(screen, TETROMINOS[self.board[y][x]]["color"], (MARGIN + x * TILE_SIZE, MARGIN + y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))

        for x, y in self.get_ghost_cells():
            if y >= 0:
                pygame.draw.rect(screen, (255, 255, 255), (MARGIN + x * TILE_SIZE, MARGIN + y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))

        for x, y in self.piece.get_cells():
            if y >= 0:
                pygame.draw.rect(screen, self.piece.color, (MARGIN + x * TILE_SIZE, MARGIN + y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))

        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
        lines_text = font.render(f"Lines: {self.lines_cleared}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH + 10, HEIGHT - 90))
        screen.blit(level_text, (WIDTH + 10, HEIGHT - 60))
        screen.blit(lines_text, (WIDTH + 10, HEIGHT - 30))

        if self.game_over:
            msg = font.render("Game Over - Press R to Restart", True, (255, 0, 0))
            screen.blit(msg, (WIDTH // 2 - 140, HEIGHT // 2 - 10))

        next_text = font.render("Next:", True, (255, 255, 255))
        screen.blit(next_text, (WIDTH + 10, MARGIN))
        next_offset_x = WIDTH + 20
        next_offset_y = MARGIN + 40
        for x, y in self.next_piece.shape:
            nx = next_offset_x + (x + 1) * TILE_SIZE
            ny = next_offset_y + (y + 1) * TILE_SIZE
            pygame.draw.rect(screen, self.next_piece.color, (nx, ny, TILE_SIZE - 1, TILE_SIZE - 1))

    def _create_surface(self, color):
        surf = pygame.Surface((TILE_SIZE - 1, TILE_SIZE - 1))
        surf.fill(color)
        return surf

    def freeze_and_check_lines(self):
        self.sounds["place"].play()
        self.freeze()
        self.flash_rows = set(y for y in range(ROWS) if all(self.board[y][x] != -1 for x in range(COLS)))
        self.flash_timer = pygame.time.get_ticks() if self.flash_rows else 0
        self.flash_state = True
        if not self.flash_rows:
            self.spawn()

    def restart(self):
        self.reset_game()
