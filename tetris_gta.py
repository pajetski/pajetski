import curses
import random
import time

# Configurations
HEIGHT = 20
WIDTH = 10

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
]

def create_board():
    return [[0] * WIDTH for _ in range(HEIGHT)]


def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]


def check_collision(board, shape, offset):
    off_y, off_x = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = x + off_x
                new_y = y + off_y
                if new_x < 0 or new_x >= WIDTH or new_y >= HEIGHT:
                    return True
                if board[new_y][new_x]:
                    return True
    return False


def merge_shape(board, shape, offset):
    off_y, off_x = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[off_y + y][off_x + x] = cell


def clear_lines(board):
    new_board = [row for row in board if any(c == 0 for c in row)]
    cleared = HEIGHT - len(new_board)
    while len(new_board) < HEIGHT:
        new_board.insert(0, [0] * WIDTH)
    return new_board, cleared


def draw_board(stdscr, board, score):
    stdscr.clear()
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            char = "#" if cell else "."
            stdscr.addstr(y, x * 2, char * 2)
    stdscr.addstr(0, WIDTH * 2 + 2, f"Score: {score}")
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    board = create_board()
    current = random.choice(SHAPES)
    offset = [0, WIDTH // 2 - len(current[0]) // 2]
    score = 0
    drop_time = time.time()

    while True:
        draw_board(stdscr, board, score)
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_LEFT:
            new_offset = [offset[0], offset[1] - 1]
            if not check_collision(board, current, new_offset):
                offset = new_offset
        elif key == curses.KEY_RIGHT:
            new_offset = [offset[0], offset[1] + 1]
            if not check_collision(board, current, new_offset):
                offset = new_offset
        elif key == curses.KEY_UP:
            new_shape = rotate(current)
            if not check_collision(board, new_shape, offset):
                current = new_shape
        elif key == curses.KEY_DOWN:
            new_offset = [offset[0] + 1, offset[1]]
            if not check_collision(board, current, new_offset):
                offset = new_offset

        if time.time() - drop_time > 0.5:
            drop_time = time.time()
            new_offset = [offset[0] + 1, offset[1]]
            if not check_collision(board, current, new_offset):
                offset = new_offset
            else:
                merge_shape(board, current, offset)
                board, cleared = clear_lines(board)
                score += cleared * 100
                current = random.choice(SHAPES)
                offset = [0, WIDTH // 2 - len(current[0]) // 2]
                if check_collision(board, current, offset):
                    stdscr.addstr(HEIGHT // 2, WIDTH - 4, "GAME OVER")
                    stdscr.nodelay(False)
                    stdscr.getch()
                    break
        merge_board = [row[:] for row in board]
        for y, row in enumerate(current):
            for x, cell in enumerate(row):
                if cell:
                    merge_board[offset[0]+y][offset[1]+x] = cell
        draw_board(stdscr, merge_board, score)
        time.sleep(0.05)

if __name__ == '__main__':
    curses.wrapper(main)
