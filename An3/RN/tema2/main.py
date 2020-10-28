import pickle
import gzip
import numpy as np


def relu_function(x):
    return 1 if x > 0 else 0


class Perceptron:
    def __init__(self, inputs_count, perceptron_digit, activation_function, learning_rate=0.5):
        self.inputs = np.zeros(inputs_count)
        self.weights = np.random.rand(inputs_count)
        self.activation_function = activation_function
        self.lr = learning_rate
        self.digit = perceptron_digit

    def feed_forward(self):
        return self.activation_function(np.dot(self.inputs, self.weights))

    def train(self, inputs, labels):
        labels = [int(value == self.digit) for value in labels]
        for position in range(len(inputs)):
            self.inputs = inputs[position]
            output = self.feed_forward()
            err = labels[position] - output
            delta = self.back_propagation(err)
            self.weights += delta

    def back_propagation(self, error):
        return error * self.inputs * self.lr

    def test(self, inputs, labels):
        counter = 0
        labels = [int(value == self.digit) for value in labels]
        for position in range(len(inputs)):
            self.inputs = inputs[position]
            output = self.feed_forward()
            if output == labels[position]:
                counter += 1
        return counter/len(inputs)*100

    def predict(self, input):
        self.inputs = input
        return self.feed_forward()


def test2(test_set, perceptron_list):
    count = 0
    inputs, labels = test_set
    for index in range(len(inputs)):
        for perceptron in perceptron_list:
            output = perceptron.predict(inputs[index])
            if output:
                if perceptron.digit == labels[index]:
                    count += 1
                    break
                else:
                    break
    return count / len(inputs) * 100


if __name__ == '__main__':
    f = gzip.open("mnist.pkl.gz", "rb")
    train_set, valid_set, test_set = pickle.load(f, encoding="latin1")
    f.close()
    inputs, labels = train_set
    input_size = len(inputs[0])
    perceptron_list = [Perceptron(input_size, index, relu_function) for index in range(10)]
    print(test2(test_set, perceptron_list))
    for perceptron in perceptron_list:
        perceptron.train(inputs, labels)
    print(test2(test_set, perceptron_list))

