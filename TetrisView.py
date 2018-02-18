import TetrisModel
from copy import deepcopy


class TetrisView:
    def __init__(self, model):
        self.model = model

    def display(self):
        board = deepcopy(self.model.board)
        x_offset = self.model.shape_curr_offset[0]
        y_offset = self.model.shape_curr_offset[1]
        shape = self.model.shape_choices[self.model.shape_id][self.model.shape_morph_id]
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] != 'x':
                    continue
                x, y = x_offset + i, y_offset + j
                board[x][y] = '+'

        head_tail = '- ' * (self.model.cols+2)
        print(head_tail)
        for i in range(self.model.rows):
            s = "| " + (" ".join(board[i])) + " |"
            print(s)
        print(head_tail)