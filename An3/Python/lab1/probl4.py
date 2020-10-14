def convertUppToLow(sentenceInUpper):
    lowercase_with_underscores = sentenceInUpper[0].lower()
    for character in sentenceInUpper[1:]:
        if character.islower():
            lowercase_with_underscores += character
        else:
            lowercase_with_underscores += "_" + character.lower()
    print(lowercase_with_underscores)


if __name__ == '__main__':
    sentenceInUpper = input("Write a sentence in this format UpperCamelCase: ")
    convertUppToLow(sentenceInUpper)
