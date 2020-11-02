import math


def init_partitions():
    # m numarul de valori posibile ale etichetei
    # n numarul de valori ale atributului
    m = int(input("Adauga o valoare pentru numarul de valori posibile ale etichetei: "))
    n = int(input("Adauga o valoare pentru numarul de valori ale atributului: "))
    partitions = []
    for i in range(n):
        partition_elem = list(map(int, input("Da mi elementele pentru partitia " + str(i+1) + ":").split()))
        partitions.append(partition_elem)
    # returneaza o matrice iar pe fiecare linie este partitia unui nod fiu
    return partitions


# calculeaza partitia pentru nodul parinte in functie de partitiile fiilor
def partition_root_node(partitions):
    partition_root = [0] * len(partitions[0])
    for line in range(len(partitions[0])):
        for column in range(len(partitions)):
            # se salveaza pe coloana pentru ca valorile la "simboluri" sunt unele sub altele
            partition_root[line] += partitions[column][line]
    # returneaza o lista cu partitia nodului radacina care este calculata din suma partitiilor fiilor
    return partition_root


# entropia unui nod, primeste partitia nodului
def entropy(partition_root):
    parition_sum = 0
    entropy_value = 0
    for index_partition in range(len(partition_root)):
         parition_sum += partition_root[index_partition]
    for index_partition in range(len(partition_root)):
        if partition_root[index_partition] == 0:
            entropy_value = 0
        else:
            entropy_value += -1 * (partition_root[index_partition] / parition_sum) * (math.log2(partition_root[index_partition]) - math.log2(parition_sum))
    # returneaza o valoare numerica, entropia este calculata conform formulei
    return entropy_value


# entropia conditionala medie pentru descendenti
def median_conditioned_entropy(partitions):
    total_partitions = sum(partition_root_node(partitions))
    medium_entropy = 0
    for index_partition in range(len(partitions)):
        medium_entropy += sum(partitions[index_partition]) / total_partitions * entropy(partitions[index_partition])
    # returneaza o valoare numerica
    return medium_entropy


# castigul de informatie
def information_gain(partitions):
    total_partitions = sum(partition_root_node(partitions))
    value_ig = entropy(partition_root_node(partitions))
    for index_partition in range(len(partitions)):
        value_ig -= sum(partitions[index_partition]) / total_partitions * entropy(partitions[index_partition])
    # returneaza o valoare numerica
    return value_ig


if __name__ == '__main__':
    partitions = init_partitions()
    print("Partitiile sunt: {}".format(partitions))
    print("Partitia nodului radacina este: {}".format(partition_root_node(partitions)))
    print("Entropia radacinii este: {}".format(entropy(partition_root_node(partitions))))
    for index in range(len(partitions)):
        print("Entropia nodului cu partitia {} este {}".format(partitions[index], entropy(partitions[index])))
    print("Entropia conditionala medie este: {}".format(median_conditioned_entropy(partitions)))
    print("Castigul de informatie pentru nodul radacina este: {}".format(information_gain(partitions)))
