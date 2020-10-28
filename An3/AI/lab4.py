import copy
import json


class StateArbor:
    def __init__(self, dictionary_adjacency, dictionary_colors):
        self.adjancency = copy.deepcopy(dictionary_adjacency)
        self.colors = copy.deepcopy(dictionary_colors)

    def transition(self, node, color):
        new_state = StateArbor(self.adjancency, self.colors)
        new_state.colors[node].remove(color)
        return new_state

    def __str__(self):
        return "{}".format(json.dumps(self.colors))


def arc_consistency(state: StateArbor):
    queue = []
    # adaug in coada perechile de noduri ce trebuie parcurse
    for node in state.adjancency:
        for node2 in state.adjancency[node]:
            queue.append((node, node2))
    # folosesc un current state pentru a lasa stateul initial neatins
    current_state = state
    # incep parcurgerea perechilor de noduri din coada
    while queue:
        # scot cele doua noduri pentru a le verifica
        node1, node2 = queue.pop(0)
        # verific daca primul nod are cu culoarea1 macar un corespondent spre al doilea nod
        for color1 in current_state.colors[node1]:
            if color1:
                found_match = False
                for color2 in current_state.colors[node2]:
                    if color1 != color2:
                        found_match = True
                # daca nu are niciun corespondent, scot culoarea 1 de la nodul 1
                if not found_match:
                    current_state = current_state.transition(node1, color1)
                    # adaug in coada inversele pentru a verifica daca nu am stricat nicio legatura
                    for node_adjancent in current_state.adjancency[node1]:
                        queue.append((node_adjancent, node1))
    # returnez starea finala
    return current_state


if __name__ == '__main__':
    dictionary_adjancency1 = {
        "WA": ["SA", "NT"],
        "SA": ["WA", "NT"],
        "NT": ["WA", "SA"]
    }
    dictionary_colors1 = {
        "WA": ["red", "green", "blue"],
        "SA": ["red", "green"],
        "NT": ["green"]
    }
    dictionary_adjancency2 = {
        "T": ["V"],
        "WA": ["NT", "SA"],
        "NT": ["WA", "Q", "SA"],
        "SA": ["WA", "NT", "Q", "NSW", "V"],
        "Q": ["NT", "SA", "NSW"],
        "NSW": ["Q", "SA", "V"],
        "V": ["SA", "NSW", "T"]
    }
    dictionary_colors2 = {
        "WA": ["red"],
        "NT": ["red", "blue", "green"],
        "SA": ["red", "blue", "green"],
        "Q": ["green"],
        "NSW": ["red", "blue", "green"],
        "V": ["red", "blue", "green"],
        "T": ["red", "blue", "green"]
    }
    print(" Solutia pentru primul exemplu din tema:")
    initial_state = StateArbor(dictionary_adjancency1, dictionary_colors1)
    print(arc_consistency(initial_state))
    print("\n Solutia pentru al doilea exemplu din tema:")
    initial_state = StateArbor(dictionary_adjancency2, dictionary_colors2)
    print(arc_consistency(initial_state))
