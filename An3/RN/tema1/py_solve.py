import copy

if __name__ == '__main__':
    functions = []
    leftside = []
    rightside = []
    result = []
    submatrix = []
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
        for col_number in range(len(functions[row_number])):
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
    print("left side creata: ", leftside)
    print("right side creata: ", rightside)
    # calculez determinantul matricei leftside
    det = leftside[0][0] * leftside[1][1] * leftside[2][2] + \
          leftside[0][2] * leftside[1][0] * leftside[2][1] + \
          leftside[0][1] * leftside[1][2] * leftside[2][0] - \
          leftside[0][2] * leftside[1][1] * leftside[2][0] - \
          leftside[0][1] * leftside[1][0] * leftside[2][2] - \
          leftside[0][0] * leftside[1][2] * leftside[2][1]
    print("det: ", det)
    if not det:
        raise Exception("Determinantul este nul, ceea ce inseamna ca matricea nu admite inversa")
    # scriem matricea leftside transpusa
    leftside_tranposed = [[leftside[col_number][row_number] for col_number in range(len(leftside))] for row_number
                          in range(len(leftside[0]))]
    print("leftside transpusa: ", leftside_tranposed)
    # modificam valorile pentru a creea matricea adjuncta A* in leftside_transposed
    leftside_tranposed_adjunct = [[0 for row_number in range(len(leftside))] for col_number in range(len(leftside))]
    for row_number in range(len(leftside_tranposed)):
        for col_number in range(len(leftside_tranposed)):
            # matrix retine submatricile pentru calcularea adjunctei
            submatrix = []
            for row_index_submatrix in range(len(leftside_tranposed)):
                for col_index_submatrix in range(len(leftside_tranposed)):
                    if row_index_submatrix != row_number and col_index_submatrix != col_number:
                        submatrix.append(leftside_tranposed[row_index_submatrix][col_index_submatrix])
            leftside_tranposed_adjunct[row_number][col_number] = submatrix[0] * submatrix[3] - submatrix[1] * submatrix[2]
            if (col_number + row_number) % 2:
                leftside_tranposed_adjunct[row_number][col_number] *= -1
    print("adjuncta: ", leftside_tranposed_adjunct)
    # impatim fiecare element din matricea A* la det
    for row_number in range(len(leftside_tranposed)):
        for col_number in range(len(leftside_tranposed[0])):
            leftside_tranposed_adjunct[row_number][col_number] /= det
    print("adjuncta impartita la det: ", leftside_tranposed_adjunct)
    if leftside_tranposed_adjunct:
        leftside = copy.deepcopy(leftside_tranposed_adjunct)
    # initializam toata matricea result cu 0 pentru a putea accesa si modifica valorile
    result = [0] * len(rightside)
    # numarul de linii de la prima matrice
    for row_number in range(len(leftside)):
        for col_number in range(len(rightside)):
            result[row_number] += leftside[row_number][col_number] * rightside[col_number]
    print("rezultat: ", result)
