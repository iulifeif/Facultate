import copy


class Table:
    # mutarile pentru om
    UP = -1, 0
    UP_LEFT = -1, -1
    UP_RIGHT = -1, 1
    # mutarile pentru pc
    DOWN = 1, 0
    DOWN_LEFT = 1, -1
    DOWN_RIGHT = 1, 1

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
        if self.table[3] == ["c"] * 4 or self.table[0] == ["o"] * 4:
            return 1
        elif self.table[1] == ["c"] * 4 and self.table[2] == ["o"] * 4:
            return 2
        return 0

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
        return [self.DOWN, self.DOWN_LEFT, self.DOWN_RIGHT]
        # daca trebuie sa mute pc ul, el poate muta doar in jos

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
        line_piece = int(input("Linie la care se afla piesa pe care vrei sa o muti: "))
        column_piece = int(input("Coloana la care se alfa piesa pe care vrei sa o muti: "))
        move_piece = input("Unde vrei sa fie mutata piesa (UP, UP_LEFT, UP_RIGHT): ")
        if move_piece == "UP":
            move_piece = current_state.UP
        elif move_piece == "UP_LEFT":
            move_piece = current_state.UP_LEFT
        elif move_piece == "UP_RIGHT":
            move_piece = current_state.UP_RIGHT
        new_state = current_state.transition([line_piece, column_piece], move_piece)
        if new_state is None:
            continue
        current_state = new_state
        if current_state.final_state():
            break
        best_state = None
        for line in range(4):
            for column in range(4):
                if current_state.table[line][column] == "c":
                    for move in current_state.moves():
                        intermediary_state = current_state.transition([line, column], move)
                        if not intermediary_state:
                            continue
                        if best_state is None or best_state.heuristic_function() < intermediary_state.heuristic_function():
                            best_state = intermediary_state
        if best_state is None:
            print("Best state is None")
        current_state = best_state
    if current_state.final_state() == 2:
        print("Remiza!")
        return
    if current_state.to_move:
        print("Ai pierdut!")
    else:
        print("Ai castigat!")


if __name__ == '__main__':
    game()
