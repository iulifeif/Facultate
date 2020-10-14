def CommonLetter(string):
    dictionarWithLetters = dict()
    maximValue = 0
    maximCharacter = ""
    for character in string:
        if character not in dictionarWithLetters:
            dictionarWithLetters[character] = 0
        dictionarWithLetters[character] += 1
        if maximValue < dictionarWithLetters[character] and character != " ":
            maximValue = dictionarWithLetters[character]
            maximCharacter = character
    print(maximCharacter)


if __name__ == '__main__':
    string = input("Scrie un text: ")
    CommonLetter(string)
