import nltk
import numpy as np

nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


class words():
    def __init__(self, data):
        self.data = data
        self.lr = 0.01
        self.words = []
        self.neurons_on_hidden = 50
        self.weights_hidden = np.random.uniform(-0.8, 0.8, (len(self.data), self.neurons_on_hidden))
        self.weights_output = np.random.uniform(-0.8, 0.8, (self.neurons_on_hidden, len(self.data)))

    def feed_forward(self, one_input):
        self.hidden_layer = np.dot(self.weights_hidden.T, one_input).reshape(self.neurons_on_hidden, 1)
        self.output_layer = np.dot(self.weights_output.T, self.hidden_layer)
        self.output = softmax(self.output_layer)
        return self.output

    def backpropagation(self, one_input, label):
        err = self.output - np.asarray(label).reshape(len(self.data), 1)
        # err.shape is V x 1
        err_hidden = np.dot(self.hidden_layer, err.T)
        one_input = np.array(one_input).reshape(len(self.data), 1)
        err_ajust = np.dot(one_input, np.dot(self.weights_output, err).T)
        self.weights_output = self.weights_output - self.lr * err_hidden
        self.weights_hidden = self.weights_hidden - self.lr * err_ajust

    def train(self, epochs, inputs, labels):
        for epoch in range(1, epochs):
            self.loss = 0
            for index in range(len(inputs)):
                self.feed_forward(inputs[index])
                self.backpropagation(inputs[index], labels[index])
                appear = 0
                for poz in range(len(self.data)):
                    if labels[index][poz]:
                        self.loss += -1 * self.output_layer[poz][0]
                        appear += 1
                self.loss += appear * np.log(np.sum(np.exp(self.output_layer)))
            print("epoch ", epoch, " loss = ", self.loss)
            self.lr *= 1 / ((1 + self.lr * epoch))

    def predict(self, word, count):
        encod = [0] * len(self.data)
        encod[self.data.index(word)] = 1
        prediction = self.feed_forward(encod)
        prediction = list(map(lambda x: x[0], prediction))
        output = [(index, prediction[index]) for index in range(len(prediction))]
        sorted_output = sorted(output, reverse=True, key=lambda x: x[1])[:count]
        return list(map(lambda x: self.data[x[0]], sorted_output))


def preprocessing(file_name):
    stop_words = set(stopwords.words("romanian"))
    training_data = []
    with open(file_name, "r") as f:
        sentences = f.read()
    sentences = sentences.split(".")
    for sentence in sentences:
        word_tokens = word_tokenize(sentence)
        words = [w.lower() for w in word_tokens if w not in stop_words]
        training_data.append(words)
    return training_data


def prepare_data_for_training(sentences):
    data = []
    for sentence in sentences:
        for word in sentence:
            if word not in data:
                data.append(word)
    inputs = []
    labels = []
    for sentence in sentences:
        for index in range(len(sentence)):
            one_hot = [0] * len(data)
            one_hot[data.index(sentence[index])] = 1
            inputs.append(one_hot)
            one_hot_label = [0] * len(data)
            for poz in range(index - 2, index + 2):
                if poz != index and 0 <= poz < len(sentence):
                    one_hot_label[data.index(sentence[poz])] = 1
            labels.append(one_hot_label)
    return data, inputs, labels


if __name__ == '__main__':
    training_data = preprocessing("text-lab8")
    data, inputs, labels = prepare_data_for_training(training_data)
    instance = words(data)
    instance.train(100, inputs, labels)
    list_of_words = input("Da lista de cuvinte: ").split()
    for word in list_of_words:
        print(instance.predict(word, 3))
