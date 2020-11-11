import pickle
import gzip
import time
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor

import numpy as np


def sigmoid_function(x):
    return np.array([1 / (1 + np.math.exp(-elem)) if elem >= 0 else 1 - 1 / (1 + np.math.exp(elem)) for elem in x])
    # return np.array([1 / (1 + np.math.exp(-elem)) for elem in x])


def sigmoid_function_d(x):
    return np.array([elem * (1 - elem) for elem in x])


def relu_function(x):
    return np.array([max(0, elem) for elem in x])


def relu_function_d(x):
    return np.array([1 if elem >= 0 else 0 for elem in x])


def dataset_random_slices(dataset_list, slice_size):
    inputs, labels = dataset_list
    indices = np.arange(inputs.shape[0])
    np.random.shuffle(indices)
    inputs = np.array(inputs)[indices]
    labels = np.array(labels)[indices]
    for index in range(0, len(inputs), slice_size):
        yield [inputs[index:index+slice_size], labels[index:index+slice_size]]


class NeuralNetwork:
    # initializarea retelei neuronale
    def __init__(self, inputs_count, hidden_count, output_count, hidden_activation, output_activation, learning_rate=0.5):
        self.weights = np.random.rand(inputs_count, hidden_count) - 0.5
        self.weights2 = np.random.rand(hidden_count, output_count) - 0.5
        # self.bias = np.random.rand()
        self.hidden_count = hidden_count
        self.output_count = output_count
        self.activation_function = hidden_activation
        self.activation_function_d = output_activation
        self.lr = learning_rate

    # functia de feed forward care inmulteste inputul cu weighturile si le aduna
    def feed_forward(self, inputs):
        hidden_layer = self.activation_function(np.dot(inputs, self.weights))
        return hidden_layer, self.activation_function(np.dot(hidden_layer, self.weights2))

    # functia de train pe minibatch uri (calculeaza eroarea pentru toate si apoi o aduna la delta si bias)
    def train_minibatch(self, data_set):
        input_batch, label_batch = data_set
        delta_hidden = np.zeros(self.hidden_count)
        delta_output = np.zeros(self.output_count)
        # bias = 0.0
        for position in range(len(input_batch)):
            hidden, output = self.feed_forward(input_batch[position])
            # output_err = label_batch[position] - output
            # hidden_err = np.dot(self.weights2, output_err)
            temp_output_delta, temp_hidden_delta = self.back_propagation(input_batch[position], hidden, output, label_batch[position])
            delta_hidden += temp_hidden_delta
            delta_output += temp_output_delta
            # bias += temp_bias
        return delta_hidden, delta_output

    # functia de train in care paralelizeaza minibatch urile pe fiecare perceptron
    def train(self, inputs, labels):
        with ProcessPoolExecutor(max_workers=4) as executor:
            for delta_hidden, delta_output in executor.map(self.train_minibatch, list(dataset_random_slices([inputs, labels], 100))):
                self.weights += delta_hidden
                self.weights2 += delta_output
                # self.bias += bias

    # functia de back propagation care corecteaza eroarea
    def back_propagation(self, input_data, hidden, output, label):
        output_err = (label - output) * self.activation_function_d(output) * self.lr
        hidden_err = np.dot(self.weights2, label - output) * self.activation_function_d(hidden) * self.lr
        return output_err, hidden_err

    # functia de test per perceptron
    def test(self, inputs, labels):
        counter = 0
        for position in range(len(inputs)):
            _, output = self.feed_forward(inputs[position])
            if np.argmax(output) == np.argmax(labels[position]):
                counter += 1
        return counter/len(inputs)*100

    # predict per input
    def predict(self, input_data):
        hidden, output = self.feed_forward(input_data)
        return output


if __name__ == '__main__':
    f = gzip.open("mnist.pkl.gz", "rb")
    train_set, valid_set, test_set = pickle.load(f, encoding="latin1")
    f.close()
    inputs, labels = train_set
    new_labels = []
    for elem in labels:
        new_label = [0] * 10
        new_label[elem] = 1
        new_labels.append(new_label)
    labels = np.array(new_labels)
    test_inputs, test_labels = test_set
    new_labels = []
    for elem in test_labels:
        new_label = [0] * 10
        new_label[elem] = 1
        new_labels.append(new_label)
    test_labels = np.array(new_labels)
    input_size = len(inputs[0])
    nn = NeuralNetwork(input_size, 100, 10, relu_function, relu_function_d, learning_rate=0.0001)
    if False:
        with open("network.bin", "rb") as fd:
            nn = pickle.load(fd)
    for _ in range(5):
        start_time = time.time()
        nn.train(inputs, labels)
        print(time.time()-start_time, "seconds per epoch")
    with open("network.bin", "wb") as fd:
        pickle.dump(nn, fd)
    print("Train set accuracy:", nn.test(inputs, labels))
    print("Test set accuracy:", nn.test(test_inputs, test_labels))


