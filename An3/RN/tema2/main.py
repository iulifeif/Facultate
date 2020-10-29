import pickle
import gzip
import time
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor

import numpy as np


def activation_function(input):
    return 1 if input > 0 else 0


def dataset_random_slices(dataset_list, slice_size):
    inputs, labels = dataset_list
    indices = np.arange(inputs.shape[0])
    inputs = np.array(inputs)[indices]
    labels = np.array(labels)[indices]
    for index in range(slice_size):
        yield [inputs[index:index+slice_size], labels[index:index+slice_size]]


class Perceptron:
    def __init__(self, inputs_count, perceptron_digit, activation_function, learning_rate=0.5):
        self.weights = np.random.rand(inputs_count)
        self.activation_function = activation_function
        self.lr = learning_rate
        self.digit = perceptron_digit

    def feed_forward(self, inputs):
        return self.activation_function(np.dot(inputs, self.weights))

    def train_minibatch(self, data_set):
        input_batch, label_batch = data_set
        delta = np.zeros(len(input_batch[0]))
        for position in range(len(input_batch)):
            output = self.feed_forward(input_batch[position])
            err = label_batch[position] - output
            delta += self.back_propagation(input_batch[position], err)
        return delta

    def train(self, inputs, labels):
        labels = [int(value == self.digit) for value in labels]
        # for input_batch, label_batch in dataset_random_slices([inputs, labels], 1024):
        #     delta = self.train_minibatch(input_batch, label_batch)
        #     self.weights += delta

        with ProcessPoolExecutor(max_workers=6) as executor:
            for delta in executor.map(self.train_minibatch, list(dataset_random_slices([inputs, labels], 12500))):
                self.weights += delta

    def back_propagation(self, inputs, error):
        return error * inputs * self.lr

    # def test(self, inputs, labels):
    #     counter = 0
    #     labels = [int(value == self.digit) for value in labels]
    #     for position in range(len(inputs)):
    #         self.inputs = inputs[position]
    #         output = self.feed_forward()
    #         if output == labels[position]:
    #             counter += 1
    #     return counter/len(inputs)*100

    def predict(self, input):
        return self.feed_forward(input)


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
    perceptron_list = [Perceptron(input_size, index, activation_function, learning_rate=0.1) for index in range(10)]
    print(test2(test_set, perceptron_list))
    for _ in range(2):
        start_time = time.time()
        for perceptron in perceptron_list:
            perceptron.train(inputs, labels)
        print(time.time()-start_time, "seconds per epoch")
    print(test2(test_set, perceptron_list))

