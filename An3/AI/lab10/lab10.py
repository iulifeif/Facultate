import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json


def read_file(name):
    text = ""
    with open(name, "r") as f:
        text = f.read()
    return text


def remove_stop_words(sentence):
    stop_words = set(stopwords.words("romanian"))
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [w.lower() for w in word_tokens if not w in stop_words]
    return filtered_sentence


def word_counting(filtered_sentence):
    contor_words = {}
    for word in filtered_sentence:
        if word not in contor_words:
            contor_words[word] = 1
        else:
            contor_words[word] += 1
    return contor_words


def calculated_weight(contor_words):
    print("Nr total de cuvinte: {}".format(len(contor_words)))
    for word in contor_words:
        contor_words[word] = (contor_words[word] / len(contor_words)) * 1000000
    return contor_words


def dump_in_file(name_file, contor_words):
    with open(name_file, "w") as f:
        json.dump(contor_words, f, indent=2)


def differences(contor_words1, contor_words2):
    # scor de similitudine
    scor = 0
    duplicate_word = 0
    for word1 in contor_words1:
        if word1 in contor_words2:
            scor += abs(contor_words1[word1] - contor_words2[word1])
            duplicate_word += 1
        else:
            scor += contor_words1[word1]
    for word2 in contor_words2:
        if word2 not in contor_words1:
            scor += contor_words2[word2]
    print("Scorul de similitudine este: {}". format(scor))
    total_words = len(contor_words1) + len(contor_words2) - duplicate_word
    print("Media dif: {}".format(scor / (total_words)))


if __name__ == '__main__':

    with open("lab10/poezie1", "r") as f:
        poetry1 = f.read()

    with open("lab10/poezie2", "r") as f:
        poetry2 = f.read()

    print("poezia1: ", poetry1)
    print("poezia2: ", poetry2)

    poetry1_filtered = remove_stop_words(poetry1)
    poetry2_filtered = remove_stop_words(poetry2)
    print("poezie 1 filtrata: ", poetry1_filtered)
    print("poezie 2 filtrata: ", poetry2_filtered)

    # contorizare cuvinte
    contor_words1 = word_counting(poetry1_filtered)
    contor_words2 = word_counting(poetry2_filtered)
    print("dictionar de frecv1: ", json.dumps(contor_words1, indent=2))
    print("dictionar de frecv2: ", json.dumps(contor_words2, indent=2))

    # calculare pondere
    contor_words1 = calculated_weight(contor_words1)
    contor_words2 = calculated_weight(contor_words2)
    print("dictionar de frecv1: ", contor_words1)
    print("dictionar de frecv2: ", contor_words2)

    # dumpez jsoanele in fisiere
    dump_in_file("lab10/result1", contor_words1)
    dump_in_file("lab10/result2", contor_words2)

    differences(contor_words1, contor_words2)
