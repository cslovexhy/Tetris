from random import randint as rand
from copy import deepcopy


class TetrisModel:
    def __init__(self, rows, cols):
        if cols < 10:
            print("board is too narrow (col = {})".format(cols))
            exit(1)

        self.game_over = False
        self.shape_count = 0
        self.rows = rows
        self.cols = cols
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.shape_id = None
        self.shape_morph_id = None
        self.next_shape_id = None
        self.shape_start_offset = (0, int(cols/2-2))
        self.shape_curr_offset = None
        self.shape_choices = [
            [
                ["xxxx"],
                [" x",
                 " x",
                 " x",
                 " x",]
            ],
            [
                ["xx",
                 "xx"]
            ],
            [
                [' x',
                 'xxx'],
                ['x',
                 'xx',
                 'x'],
                ['xxx',
                 ' x'],
                [' x',
                 'xx',
                 ' x']
            ]
        ]
        self.get_a_random_shape()

    def get_a_random_shape(self):
        self.shape_count += 1
        if not self.next_shape_id:
            self.shape_id = rand(0, len(self.shape_choices)-1)
        else:
            self.shape_id = self.next_shape_id
        self.shape_morph_id = 0
        self.next_shape_id = rand(0, len(self.shape_choices) - 1)
        self.shape_curr_offset = list(self.shape_start_offset)

    def move(self, dir):
        if len(dir) != 2 or dir[0] not in (0, 1) or dir[1] not in (-1, 0, 1) or abs(dir[0]) + abs(dir[1]) != 1:
            print("move(), wrong dir: {}".format(dir))
            exit(1)
        curr = deepcopy(self.shape_curr_offset)
        self.shape_curr_offset = [curr[0]+dir[0], curr[1]+dir[1]]
        if not self.validate_shape():
            self.shape_curr_offset = curr
        return self.update_board()

    def transform(self):
        if self.shape_id is None:
            print("transform: shape does not exist")
            exit(1)
        curr_shape_morph_id = deepcopy(self.shape_morph_id)
        self.shape_morph_id = (self.shape_morph_id+1) % len(self.shape_choices[self.shape_id])
        if not self.validate_shape():
            self.shape_morph_id = curr_shape_morph_id
        return self.update_board()

    def validate_shape(self):
        x_offset = self.shape_curr_offset[0]
        y_offset = self.shape_curr_offset[1]
        shape = self.shape_choices[self.shape_id][self.shape_morph_id]
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 'x':
                    continue
                x, y = x_offset+i, y_offset+j
                if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
                    return False
                if self.board[x][y] == 'x':
                    return False
        return True

    def update_board(self):
        row_offset = self.shape_curr_offset[0]
        col_offset = self.shape_curr_offset[1]
        shape = self.shape_choices[self.shape_id][self.shape_morph_id]
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 'x':
                    continue
                row, col = row_offset + i, col_offset + j
                if row == self.rows-1 or self.board[row+1][col] == 'x':
                    min_i = self.add_shape_to_board()
                    if min_i < 5:
                        self.game_over = True
                        return False
                    self.try_erase_full_rows()
                    self.get_a_random_shape()
                    return True
        return True

    def add_shape_to_board(self):
        row_offset = self.shape_curr_offset[0]
        col_offset = self.shape_curr_offset[1]
        shape = self.shape_choices[self.shape_id][self.shape_morph_id]
        min_row = self.rows
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 'x':
                    continue
                row, col = row_offset + i, col_offset + j
                min_row = min(min_row, row)
                self.board[row][col] = 'x'
        return min_row

    def try_erase_full_rows(self):
        new_board = []
        for i in range(self.rows-1, -1, -1):
            x_count = 0
            for j in range(self.cols):
                if self.board[i][j] == 'x':
                    x_count += 1
                else:
                    break
            if x_count != self.cols:
                new_board.append(self.board[i])
        for i in range(self.rows-len(new_board)):
            new_board.append([' ' for _ in range(self.cols)])
        self.board = new_board[::-1]
