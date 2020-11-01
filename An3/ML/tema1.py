import math


# entropia unui nod
def entropy(element_list):
    positive_value = element_list[0]
    negative_value = element_list[1]
    first_value = - positive_value / (positive_value + negative_value) * (
                math.log2(positive_value) - math.log2(positive_value + negative_value))
    second_value = - negative_value / (positive_value + negative_value) * (
                math.log2(negative_value) - math.log2(positive_value + negative_value))
    return first_value + second_value


# entropia conditionata medie pentru nodul A -> left -> right

def conditioned_entropy(left_values, right_values):
    all_values = left_values[0] + left_values[1] + right_values[0] + right_values[1]
    return (left_values[0] + left_values[1]) / all_values * entropy(left_values) + \
           (right_values[0] + right_values[1]) / all_values * entropy(right_values)


# castigul de informatie pentru nodul A -> left -> right
def information_gain(all_inputs, left, right):
    return entropy(all_inputs) - \
           (left[0] + left[1]) / (all_inputs[0] + all_inputs[1]) * entropy(left) - \
           (right[0] + right[1]) / (all_inputs[0] + all_inputs[1]) * entropy(right)


if __name__ == '__main__':
    s_left = [3, 2]
    s_right = [2, 2]
    a_left = [5, 1]
    a_right = [0, 3]
    all_inputs = [s_left[0] + s_right[0], s_left[1] + s_right[1]]
    print(entropy([5, 5]))
