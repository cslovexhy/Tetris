import TetrisModel


class TetrisController:
    def __init__(self, model):
        self.model = model

    def move_down(self):
        self.model.move((1, 0))

    def move_left(self):
        self.model.move((0, -1))

    def move_right(self):
        self.model.move((0, 1))

    def transform(self):
        self.model.transform()

    def move_down_all_the_way(self):
        old_count = self.model.shape_count
        while self.model.shape_count == old_count:
            self.move_down()
