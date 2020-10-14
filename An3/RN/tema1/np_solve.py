import numpy as np
import numpy.linalg as la


if __name__ == '__main__':
    functions = []
    leftside = []
    rightside = []
    unknown_variables = ["x", "y", "z"]
    with open("input.txt", "r") as f:
        file_content = f.read()
    file_lines = file_content.split("\n")
    # adaug liniile din fisier in matrix_functions
    for line in file_lines:
        if line:
            functions.append(line.split(" "))
    # creez prima matrice
    for row_number in range(len(functions)):
        # adaug cate o noua linie cu valori pentru a putea fi accesate in matrice
        leftside.append([0, 0, 0])
        for col_number in range(len(functions[0])):
            for var in unknown_variables:
                # daca este un numar cu necunoscuta
                if var in functions[row_number][col_number]:
                    # din acel tuplu, iau numai numarul
                    number = int(functions[row_number][col_number].split(var)[0])
                    # verific daca este negativ sau nu si adaug numarul in matrice
                    if col_number > 0 and functions[row_number][col_number - 1] == "-":
                        number *= -1
                    leftside[row_number][unknown_variables.index(var)] = number
            # creez cea de-a doua matrice
            if functions[row_number][col_number] == "=":
                number = int(functions[row_number][col_number + 1])
                rightside.append(number)
    leftside = np.array(leftside)
    rightside = np.array(rightside)
    print("left side creata: \n", leftside)
    print("right side creata: ", rightside)
    # calc det
    det = la.det(leftside)
    if not det:
        raise Exception("Determinantul este 0, nu se poate calcula rezultatul")
    # calculam transpusa matricei
    # leftside_t = leftside.transpose()
    # calculam inversa
    leftside_inv = la.inv(leftside)
    # inmultirea a doua matrici
    result = leftside_inv.dot(rightside)
    print(result)
    # scurtatura:
    print(la.solve(leftside, rightside))
