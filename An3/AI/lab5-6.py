import copy


class Table:
    UP = -1, 0
    UP_LEFT = -1, -1
    UP_RIGHT = -1, 1
    LEFT = 0, -1
    RIGHT = 0, 1
    DOWN = 1, 0
    DOWN_LEFT = 1, -1
    DOWN_RIGHT = 1, 1

    dict_moves = {
        "UP": UP,
        "UP_LEFT": UP_LEFT,
        "UP_RIGHT": UP_RIGHT,
        "LEFT": LEFT,
        "RIGHT": RIGHT,
        "DOWN": DOWN,
        "DOWN_LEFT": DOWN_LEFT,
        "DOWN_RIGHT": DOWN_RIGHT
    }

    def __init__(self, table_game=None, to_move=0):
        if table_game is None:
            self.to_move = to_move
            self.table = []
            for line in range(4):
                if line == 0:
                    self.table.append(["c"] * 4)
                elif line == 3:
                    self.table.append(["o"] * 4)
                else:
                    self.table.append([0] * 4)
        else:
            self.table = copy.deepcopy(table_game)
            self.to_move = to_move

    def print_table(self):
        for line in range(4):
            print(self.table[line])

    def final_state(self):
        return self.table[3] == ["c"] * 4 or self.table[0] == ["o"] * 4

    # functia din laborator, doar ca este cea restansa care se calculeaza dupa pozitie nu dupa cat a avansat
    # F = 12 - Suma[y(computer)] - Suma[y(om)]
    def heuristic_function(self):
        result = 12
        for line in range(4):
            for column in range(4):
                if self.table[line][column] == "c" or self.table[line][column] == "o":
                    result -= line
        return result

    def moves(self):
        moves = [self.DOWN, self.DOWN_LEFT, self.DOWN_RIGHT, self.RIGHT, self.LEFT, self.UP, self.UP_LEFT, self.UP_RIGHT]
        for line in range(4):
            for column in range(4):
                if self.table[line][column] == "c":
                    for move in moves:
                        intermediary_state = self.transition([line, column], move)
                        if not intermediary_state:
                            continue
                        yield intermediary_state

    def transition(self, pos_piece, move):
        if 0 <= pos_piece[0] + move[0] < 4 and \
                0 <= pos_piece[1] + move[1] < 4 and \
                self.table[pos_piece[0] + move[0]][pos_piece[1] + move[1]] == 0:
            new_table = copy.deepcopy(self.table)
            new_table[pos_piece[0]][pos_piece[1]] = 0
            new_table[pos_piece[0] + move[0]][pos_piece[1] + move[1]] = "o" if self.to_move == 0 else "c"
            return Table(new_table, 1 - self.to_move)
        return None


def game():
    current_state = Table()
    while not current_state.final_state():
        current_state.print_table()
        line_piece = int(input("Linia la care se afla piesa pe care vrei sa o muti: "))
        column_piece = int(input("Coloana la care se alfa piesa pe care vrei sa o muti: "))
        move_piece = input("Unde vrei sa fie mutata piesa (UP, UP_LEFT, UP_RIGHT, LEFT, RIGHT, DOWN, DOWN_LEFT, DOWN_RIGHT): ")
        if move_piece in Table.dict_moves:
            move_piece = current_state.dict_moves[move_piece]
        new_state = current_state.transition([line_piece, column_piece], move_piece)
        if new_state is None:
            continue
        current_state = new_state
        if current_state.final_state():
            break
        best_state = None
        for state in current_state.moves():
            if best_state is None or best_state.heuristic_function() < state.heuristic_function():
                best_state = state
        # if best_state is None:
        #     print("Best state is None")
        current_state = best_state
    if current_state.to_move:
        print("Ai castigat!")
    else:
        print("Ai pierdut!")


if __name__ == '__main__':
    game()
