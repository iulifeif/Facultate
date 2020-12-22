import time
from concurrent.futures.process import ProcessPoolExecutor

import numpy as np


def sigmoid_function(inputs):
    return np.array([1 / (1 + np.math.exp(-elem)) if elem >= 0 else 1 - 1 / (1 + np.math.exp(elem)) for elem in inputs])


def sigmoid_function_d(inputs):
    return np.array([elem * (1 - elem) for elem in inputs])


class NeuralNetwork:
    def __init__(self, function, function_d, lr=0.2):
        self.lr = lr
        self.activation_function = function
        self.activation_function_d = function_d
        self.weights_hidden = np.random.rand(2, 2) - 0.5
        self.weights_output = np.random.rand(2, 1) - 0.5
        # self.bias_hidden = -1
        # self.bias_output = -1

    def feed_forward(self, inputs):
        hidden_layer = self.activation_function(np.dot(inputs, self.weights_hidden))
        output_layer = self.activation_function(np.dot(hidden_layer, self.weights_output))
        return hidden_layer, output_layer

    def back_propagation(self, hidden, output, label):
        output_err = (label - output) * self.activation_function_d(output) * self.lr
        self.weights_output += output_err
        # self.bias_output += output_err
        hidden_err = np.dot(self.weights_output, output_err) * self.activation_function_d(hidden) * self.lr
        self.weights_hidden += hidden_err
        # self.bias_hidden += hidden_err

    def train(self, inputs, output_function):
        indices = np.arange(inputs.shape[0])
        np.random.shuffle(indices)
        inputs = inputs[indices]
        output_function = output_function[indices]
        for index in range(len(inputs)):
            hidden_layer, output_layer = self.feed_forward(inputs[index])
            self.back_propagation(hidden_layer, output_layer, output_function[index])

    def predict(self, elem):
        hidden, output = self.feed_forward(elem)
        return round(output[0])

    def test(self, inputs, output_values):
        count = 0
        for index in range(len(inputs)):
            output = self.predict(inputs[index])
            if output == output_values[index]:
                count += 1
        return count / len(inputs) * 100


if __name__ == '__main__':
    inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    epoch_number = int(input("Number of epochs: "))
    lr = float(input("Learning rate: "))
    output_function = np.array(list(map(int, input("Enter output function: ").split())))
    nn = NeuralNetwork(sigmoid_function, sigmoid_function_d, lr)
    for epoch in range(epoch_number):
        start_time = time.time()
        nn.train(inputs, output_function)
        print(time.time() - start_time, "seconds per epoch")
    print("Train set accuracy: ", nn.test(inputs, output_function))
