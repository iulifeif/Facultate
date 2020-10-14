
def vowels(sentence):
    vowel = "aeiou"
    numbersOfVowels = 0
    for character in sentence:
        if character in vowel:
            numbersOfVowels += 1
    print("In sentence: \"{}\" are {} vowels".format(sentence, numbersOfVowels))


if __name__ == '__main__':
    sentence = input("Write a sentence: ")
    vowels(sentence)
