import sys
import time
from TetrisModel import TetrisModel
from TetrisView import TetrisView
from TetrisController import TetrisController


class TetrisGame:
    def __init__(self, row=18, col=10):
        self.model = TetrisModel(row, col)
        self.view = TetrisView(self.model)
        self.controller = TetrisController(self.model)

    def start(self):
        while not self.model.game_over:
            self.view.display()
            s = input(">")
            if s == ' ':
                self.controller.move_down_all_the_way()
            else:
                for i in range(min(len(s), 5)):
                    if s[i] == 'a':
                        self.controller.move_left()
                    elif s[i] == 's':
                        self.controller.move_down()
                    elif s[i] == 'd':
                        self.controller.move_right()
                    elif s[i] == 'w':
                        self.controller.transform()
                    else:
                        pass


game = TetrisGame()
game.start()