import copy
import math


class kmeans:
    def __init__(self, d):
        self.d = d
        self.centroid_coords = []
        self.x_coords = []
        self.k = int(input("Scrie numarul de centroizi: "))
        self.clusters = [list() for _ in range(self.k)]
        self.iteration = 0

    def read_data(self, file_name):
        for index in range(self.k):
            coord_index = input("Scrie coordonatele pentru centroidul {}: ".format(index + 1))
            self.centroid_coords.append(tuple(map(float, coord_index.split(" "))))
        with open(file_name, "r") as f:
            point = f.read().split("\n")
            for index in point:
                if index and (self.d == 2 or self.d == 3):
                    self.x_coords.append(tuple(map(float, index.split(", "))))
                elif index and self.d == 1:
                    self.x_coords.append(index)

    def algorithm(self):
        while True:
            self.iteration += 1
            print("\n Iteratia {}".format(self.iteration))
            intermediar_cluster = [list() for _ in range(self.k)]
            # creez un cluster intermediar, fiecare linie este un cluster pentru punctul cu nr aferent numarului liniei
            # calculez distanta dintre coord punctului si coord fiecarui centroid si il aleg pe cel cu dist minima
            for index_points in self.x_coords:
                distances = []
                for index_centroid in self.centroid_coords:
                    distances.append(math.dist(index_points, index_centroid))
                line = distances.index(min(distances))
                intermediar_cluster[line].append(index_points)
            # daca clusterul creat este identic cu cel din iteratia trecuta, algoritmul se incheie
            if intermediar_cluster != self.clusters:
                self.clusters = copy.deepcopy(intermediar_cluster)
            else:
                print("Algoritmul a convers!")
                break
            # afisez la fiecare pas centroizii si clusterele aferente lor
            for index_line in range(len(self.centroid_coords)):
                print("Centroidul {} are coord: {}".format(index_line, self.centroid_coords[index_line]))
                print("Si apartine clusterului cu punctele: {}".format(self.clusters[index_line]))

            # recalculez centroizii in functie de spatiul euclidian primit
            if self.d == 1:
                for index_line in range(len(self.clusters)):
                    sum_x = 0
                    for index_col in range(len(self.clusters[index_line])):
                        sum_x += self.clusters[index_line][index_col]
                    if len(self.clusters[index_line]):
                        sum_x /= len(self.clusters[index_line])
                        self.centroid_coords[index_line] = sum_x
            elif self.d == 2:
                for index_line in range(len(self.clusters)):
                    sum_x = 0
                    sum_y = 0
                    for index_col in range(len(self.clusters[index_line])):
                        sum_x += self.clusters[index_line][index_col][0]
                        sum_y += self.clusters[index_line][index_col][1]
                    if len(self.clusters[index_line]):
                        sum_x /= len(self.clusters[index_line])
                        sum_y /= len(self.clusters[index_line])
                        self.centroid_coords[index_line] = (sum_x, sum_y)
            elif self.d == 3:
                for index_line in range(len(self.clusters)):
                    sum_x = 0
                    sum_y = 0
                    sum_z = 0
                    for index_col in range(len(self.clusters[index_line])):
                        sum_x += self.clusters[index_line][index_col][0]
                        sum_y += self.clusters[index_line][index_col][1]
                        sum_z += self.clusters[index_line][index_col][2]
                    if len(self.clusters[index_line]):
                        sum_x /= len(self.clusters[index_line])
                        sum_y /= len(self.clusters[index_line])
                        sum_z /= len(self.clusters[index_line])
                        self.centroid_coords[index_line] = (sum_x, sum_y, sum_z)


if __name__ == '__main__':
    d = int(input("Scrie numarul spatiului euclidian: "))
    k = kmeans(d)
    k.read_data(input("Scrie numele fisierului: "))
    k.algorithm()
