import json
from copy import deepcopy


class State:
    UP = -1, 0
    RIGHT = 0, 1
    DOWN = 1, 0
    LEFT = 0, -1

    # functie de initializare
    def __init__(self, start_x, start_y, end_x, end_y, matrix, moves_list=None):
        self.pos = (start_x, start_y)
        self.end = (end_x, end_y)
        self.table = deepcopy(matrix)
        # n linia, m coloana
        self.n, self.m = len(matrix), len(matrix[0])
        self.table[self.pos[0]][self.pos[1]] = 2
        if moves_list is None:
            self.moves_list = []
        else:
            self.moves_list = deepcopy(moves_list)

    # functie pentru a retine "denumirile mutarilor"
    def get_move_name(self, move):
        if move == self.UP:
            return "UP"
        elif move == self.RIGHT:
            return "RIGHT"
        elif move == self.DOWN:
            return "DOWN"
        elif move == self.LEFT:
            return "LEFT"

    # functia de trannzitie, verifica daca este valida si face tranzitia
    def transition(self, move):
        next_pos = (self.pos[0] + move[0], self.pos[1] + move[1])
        if 0 <= next_pos[0] < self.n and \
                0 <= next_pos[1] < self.m and \
                not self.table[next_pos[0]][next_pos[1]]:
            return State(next_pos[0], next_pos[1], self.end[0], self.end[1], self.table, self.moves_list+[self.get_move_name(move)])
        return None

    # functia pentru a verifica daca a ajuns pe pozitia finala
    def is_final(self):
        return self.pos == self.end

    # functia pentru a face mutarile dintr o stare
    @property
    def moves(self):
        return [self.UP, self.DOWN, self.RIGHT, self.LEFT]
        # return [move for move in all_moves if self.transition(move)]


# functia BKT pentru laboratorul viitor
def BKT(state: State):
    if state.is_final():
        return state
    for move in state.moves:
        new_state = state.transition(move)
        if new_state:
            result = BKT(new_state)
            if result:
                return result
    return None


def BFS(state: State):
    if state.is_final():
        return state

def HillClimb(state: State):


if __name__ == '__main__':
    initial_state = State(0, 0, 4, 4, [
        [0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ])
    final_state = BKT(initial_state)
    print(final_state.table)
    print(final_state.moves_list)
